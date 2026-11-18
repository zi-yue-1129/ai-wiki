#!/usr/bin/env python3
"""Lossless deterministic packaging only; does not change browser-test coverage.

Each uploaded group retains paths relative to the original artifacts directory.
The separately uploaded manifest maps every file to its group and SHA256. Groups
are published only after source/output inventories and all bytes are verified.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import shutil
import stat
import tempfile

DEFAULT_ROOTS = ('keyboard-scroll-preflight', 'built-motion-browser',
                 'sharpness-labs', 'adaptive-optimiser-labs', 'vi-prose', 'embedding-pages')
LIMIT = 100 * 1024 * 1024
MAX_GROUPS = 24


def digest(path):
    h = hashlib.sha256()
    with path.open('rb') as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b''):
            h.update(chunk)
    return h.hexdigest()


def inventory(source, roots, allow_missing=False):
    """Reject ambiguous roots, links and non-regular entries; include hidden files."""
    source = Path(source)
    if source.is_symlink():
        raise ValueError('Source directory is a symlink')
    if len(set(roots)) != len(roots):
        raise ValueError('Duplicate root')
    normalized = []
    for root in roots:
        p = PurePosixPath(root)
        if not root or p.is_absolute() or '..' in p.parts or str(p) != root:
            raise ValueError(f'Unsafe or noncanonical root: {root}')
        for old in normalized:
            if p == old or p in old.parents or old in p.parents:
                raise ValueError('Duplicate/overlapping root')
        normalized.append(p)
    files = {}; missing = []
    for root in roots:
        directory = source / root
        for parent in [directory, *directory.parents]:
            if parent.is_symlink():
                raise ValueError(f'Symlink directory: {parent}')
            if parent == source:
                break
        if not directory.exists():
            if not allow_missing:
                raise ValueError(f'Missing root: {root}')
            missing.append(root); continue
        if not directory.is_dir():
            raise ValueError(f'Root is not a directory: {root}')
        for path in sorted(directory.rglob('*')):
            mode = path.lstat().st_mode
            if stat.S_ISLNK(mode):
                raise ValueError(f'Symlink entry: {path}')
            if stat.S_ISDIR(mode):
                continue
            if not stat.S_ISREG(mode):
                raise ValueError(f'Nonregular entry: {path}')
            rel = path.relative_to(source).as_posix()
            if rel in files:
                raise ValueError(f'Duplicate file path: {rel}')
            files[rel] = {'size': path.stat().st_size, 'sha256': digest(path)}
    return dict(sorted(files.items())), sorted(missing)


def plan(files, limit=LIMIT, max_groups=MAX_GROUPS):
    if limit <= 0 or max_groups <= 0:
        raise ValueError('Limits must be positive')
    groups = []; current = []; total = 0
    for path, meta in sorted(files.items()):
        size = meta['size']
        if size > limit:
            raise ValueError(f'Single file exceeds group limit: {path}')
        if current and total + size > limit:
            groups.append(current); current = []; total = 0
        current.append(path); total += size
    if current:
        groups.append(current)
    if len(groups) > max_groups:
        raise ValueError(f'Artifact groups exceed {max_groups} slots: {len(groups)}')
    return groups


def verify_outputs(directory, files, groups):
    expected = {}; seen = set()
    for index, paths in enumerate(groups, 1):
        for path in paths:
            if path in seen:
                raise ValueError(f'Duplicate output mapping: {path}')
            if path not in files:
                raise ValueError(f'Unknown output mapping: {path}')
            seen.add(path); expected[f'group-{index:02d}/{path}'] = files[path]
    if seen != set(files):
        raise ValueError('Output mapping omitted source files')
    actual = {}
    for path in directory.rglob('*'):
        if path.is_symlink():
            raise ValueError('Output symlink')
        if path.is_dir():
            continue
        if not path.is_file():
            raise ValueError('Nonregular output')
        actual[path.relative_to(directory).as_posix()] = {'size': path.stat().st_size, 'sha256': digest(path)}
    if actual != expected:
        raise ValueError('Output inventory/size/SHA mismatch (missing, duplicate, extra or corrupt file)')


def prepare(source, output, roots=DEFAULT_ROOTS, limit=LIMIT, max_groups=MAX_GROUPS,
            allow_missing=False, copy_file=shutil.copyfile):
    source = Path(source).absolute(); output = Path(output).absolute()
    if output.exists():
        raise ValueError('Output directory already exists; refusing to mix runs')
    if source == output or source in output.parents or output in source.parents:
        raise ValueError('Source/output must not overlap')
    output.mkdir(parents=True)
    manifest = {'schema': 1, 'status': 'preparing', 'source_roots': list(roots),
                'max_group_bytes': limit, 'max_groups': max_groups,
                'artifact_prefix': 'built-motion-browser-review', 'groups': [], 'files': []}
    try:
        files, missing = inventory(source, roots, allow_missing)
        groups = plan(files, limit, max_groups)
        manifest['missing_roots'] = missing
        # Copy rather than hardlink: output bytes cannot change if a source is rewritten.
        with tempfile.TemporaryDirectory(prefix='.pack-', dir=output) as temporary:
            staging = Path(temporary)
            for index, paths in enumerate(groups, 1):
                for path in paths:
                    target = staging / f'group-{index:02d}' / path
                    target.parent.mkdir(parents=True, exist_ok=True)
                    copy_file(source / path, target)
            verify_outputs(staging, files, groups)
            after, after_missing = inventory(source, roots, allow_missing)
            if after != files or after_missing != missing:
                raise ValueError('Source inventory or bytes changed during packaging')
            for index, paths in enumerate(groups, 1):
                name = f'group-{index:02d}'
                artifact = f'built-motion-browser-review-{index:02d}'
                (staging / name).rename(output / name)
                manifest['groups'].append({'directory': name, 'artifact': artifact,
                    'raw_bytes': sum(files[p]['size'] for p in paths), 'file_count': len(paths)})
                for path in paths:
                    manifest['files'].append({'path': path, 'artifact': artifact,
                        'artifact_path': path, **files[path]})
        manifest.update(status='passed', file_count=len(files),
                        raw_bytes=sum(m['size'] for m in files.values()))
    except Exception as error:
        manifest.update(status='failed', error=str(error))
        raise
    finally:
        (output / 'manifest.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n')
    return manifest


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', type=Path, default=Path('artifacts'))
    parser.add_argument('--output', type=Path, default=Path('browser-artifact-parts'))
    parser.add_argument('--roots', nargs='+', default=list(DEFAULT_ROOTS))
    parser.add_argument('--allow-missing-roots', action='store_true',
                        help='Record skipped suites explicitly; does not turn failed tests green')
    parser.add_argument('--group-bytes', type=int, default=LIMIT)
    parser.add_argument('--max-groups', type=int, default=MAX_GROUPS)
    args = parser.parse_args()
    report = prepare(args.source, args.output, args.roots, args.group_bytes,
                     args.max_groups, args.allow_missing_roots)
    print(f"Verified {report['file_count']} files in {len(report['groups'])} lossless artifact groups")


if __name__ == '__main__':
    main()
