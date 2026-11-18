#!/usr/bin/env python3
"""Cache only authenticated Ubuntu font download bytes, never installed state.

Run with the runner's system Python, after a successful fresh apt-get update.
Cache bytes are untrusted until checked against the current APT candidate.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import stat
import subprocess
import tempfile
import time

PACKAGE = 'fonts-noto-cjk'
PAYLOAD = 'font.deb'


def run(*args, **kwargs):
    return subprocess.run(args, check=True, text=True, **kwargs)


def metadata():
    import apt  # Runner system Python, not setup-python's virtual environment.
    release = dict(line.split('=', 1) for line in Path('/etc/os-release').read_text().splitlines() if '=' in line)
    if release.get('ID', '').strip('"') != 'ubuntu' or release.get('VERSION_ID', '').strip('"') != '24.04':
        raise RuntimeError('Font cache supports Ubuntu 24.04 only')
    candidate = apt.Cache()[PACKAGE].candidate
    if candidate is None:
        raise RuntimeError('No font candidate')
    return candidate_metadata(candidate)


def candidate_metadata(candidate):
    # A duplicate version from another origin must not lend trust to its record.
    origins = [o for o in candidate.origins if o.archive != 'now']
    if not origins or any(not o.trusted or o.origin != 'Ubuntu' for o in origins):
        raise RuntimeError('Font metadata is not exclusively trusted Ubuntu metadata')
    sha = candidate.record.get('SHA256', '')
    size = int(candidate.record.get('Size', '0'))
    if not re.fullmatch('[0-9a-f]{64}', sha) or size <= 0:
        raise RuntimeError('Missing authoritative SHA256 or Size')
    return {'package': PACKAGE, 'version': candidate.version,
            'architecture': candidate.architecture, 'size': size, 'sha256': sha,
            'origins': sorted({o.site for o in origins})}


def copy_verified(source, destination, meta):
    """Open no symlinks; validate while copying to a private newly-created file.

    Rejects same-size corruption; APT's existing archive fast path alone does not.
    Caller owns destination's parent; no untrusted paths are installed recursively.
    """
    fd = os.open(source, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK)
    created = False
    try:
        info = os.fstat(fd)
        if not stat.S_ISREG(info.st_mode) or info.st_nlink != 1 or info.st_size != meta['size']:
            raise ValueError('Cache payload must be one regular file of the expected size')
        digest = hashlib.sha256()
        count = 0
        with os.fdopen(fd, 'rb', closefd=False) as incoming, open(destination, 'xb') as outgoing:
            created = True
            while block := incoming.read(1024 * 1024):
                count += len(block)
                if count > meta['size']:
                    raise ValueError('Payload grew while reading')
                digest.update(block)
                outgoing.write(block)
        if count != meta['size'] or digest.hexdigest() != meta['sha256']:
            raise ValueError('Cache SHA256 mismatch')
    except BaseException:
        if created:
            Path(destination).unlink(missing_ok=True)
        raise
    finally:
        os.close(fd)


def validate_cache_directory(cache):
    if not stat.S_ISDIR(cache.lstat().st_mode):
        raise ValueError('Cache directory must not be a symlink')
    if {p.name for p in cache.iterdir()} != {PAYLOAD}:
        raise ValueError('Missing or unexpected cache entries')


def install(cache, export, report, disabled=False):
    start = time.monotonic()
    meta = metadata()  # NEVER read metadata supplied by the cache.
    result = dict(meta, cache='disabled' if disabled else 'miss')
    # Private root-owned tree: restored files can never modify promoted bytes.
    with tempfile.TemporaryDirectory(prefix='verified-font-') as directory:
        root = Path(directory)
        root.chmod(0o755)
        archives = root / 'archives'
        archives.mkdir(mode=0o755)
        (archives / 'partial').mkdir(mode=0o755)
        options = ('-o', f'Dir::Cache::archives={archives}', '-o', 'APT::Keep-Downloaded-Packages=true')
        # Ask APT for its exact encoded archive filename (including epoch handling).
        import shlex
        printed = run('apt-get', *options, '--print-uris', '--download-only', '--reinstall', '-y',
                      '--no-install-recommends', 'install', f"{PACKAGE}={meta['version']}",
                      stdout=subprocess.PIPE).stdout
        names = []
        for line in printed.splitlines():
            if line.startswith("'"):
                fields = shlex.split(line)
                if len(fields) >= 3 and fields[1].startswith(PACKAGE + '_'):
                    names.append(fields[1])
        if len(names) != 1 or Path(names[0]).name != names[0] or not names[0].endswith('.deb'):
            raise RuntimeError('Cannot determine authoritative font archive name')
        target = archives / names[0]
        if not disabled:
            try:
                validate_cache_directory(cache)
                copy_verified(cache / PAYLOAD, target, meta)
                result['cache'] = 'verified-hit'
            except (OSError, ValueError) as exc:
                result['cache'] = 'rejected' if (cache / PAYLOAD).exists() else 'miss'
                result['cache_detail'] = str(exc)
        # Download-only first: permits an independent hash check even on cold runs.
        command = ('apt-get', *options, '-y', '--no-install-recommends', '--reinstall')
        run(*command, '--download-only', 'install', f"{PACKAGE}={meta['version']}")
        verified = root / PAYLOAD
        copy_verified(target, verified, meta)
        # Install by package name through APT, never dpkg -i a cache payload.
        run(*command, 'install', f"{PACKAGE}={meta['version']}")
        installed = run('dpkg-query', '-W', '-f=${Version}', PACKAGE, stdout=subprocess.PIPE).stdout
        if installed != meta['version']:
            raise RuntimeError('Installed font version differs from authenticated candidate')
        family = run('fc-match', '-f', '%{family}\n', 'sans:lang=zh-tw', stdout=subprocess.PIPE).stdout
        if 'Noto Sans CJK' not in family:
            raise RuntimeError('Traditional Chinese font match failed')
        font_file = run('fc-match', '-f', '%{file}\n', 'sans:lang=zh-tw', stdout=subprocess.PIPE).stdout.strip()
        result['font_file_sha256'] = hashlib.sha256(Path(font_file).read_bytes()).hexdigest()
        # Export is a distinct fresh directory, never the restored directory.
        export.mkdir(parents=True, exist_ok=False)
        shutil.copyfile(verified, export / PAYLOAD)
        result.update(installed_version=installed, font_family=family.strip(),
                      elapsed_seconds=round(time.monotonic() - start, 3))
        report.parent.mkdir(parents=True, exist_ok=True)
        report.write_text(json.dumps(result, indent=2) + '\n')
        print(json.dumps(result))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', choices=['key', 'install'])
    parser.add_argument('--cache', type=Path)
    parser.add_argument('--export', type=Path)
    parser.add_argument('--report', type=Path)
    parser.add_argument('--disabled', action='store_true')
    args = parser.parse_args()
    if args.command == 'key':
        meta = metadata()
        architecture = run('dpkg', '--print-architecture', stdout=subprocess.PIPE).stdout.strip()
        print(f'font-archive-v1-ubuntu24.04-{architecture}-{meta["sha256"]}')
    else:
        if not all([args.cache, args.export, args.report]):
            parser.error('install requires --cache, --export and --report')
        install(args.cache, args.export, args.report, args.disabled)


if __name__ == '__main__':
    main()
