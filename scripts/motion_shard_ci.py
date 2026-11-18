"""Build small upload receipts and independently gate the exact run/attempt's full coverage."""
import argparse,hashlib,json,sys
from pathlib import Path
from motion_shard_contract import *

def read(p):return json.loads(Path(p).read_text())
def receipt(kind,out):
    provenance=identity();pack=read('browser-artifact-parts/manifest.json')
    if kind=='shard':
        report=Path('artifacts/built-motion-browser/report.json')
        result={'manifest':read('artifacts/built-motion-browser/discovery-manifest.json'), 'report':read(report),
                'report_file_sha256':hashlib.sha256(report.read_bytes()).hexdigest(),'pack':pack}
    else:
        result={'identity':provenance,'manifest':read('artifacts/keyboard-scroll-preflight/discovery-manifest.json'),
                'reports':{name:read(f'artifacts/{name}/report.json') for name in [s['id'] for s in support_registry()['suites'] if s['type']!='legacy-lab']},
                'execution':read('artifacts/support-execution/report.json'),'pack':pack}
    out.mkdir(parents=True,exist_ok=True);(out/'receipt.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')

def _gate(directory,inventory,count,out):
    # Gate runs its own strict build first, then independently checks every built mapping.
    from mkdocs.config import load_config
    from test_built_motion_browser import discover_pages,check_built_page,VIEWPORTS
    config=load_config(config_file='mkdocs.yml');pages=discover_pages(config)
    for page in pages:check_built_page(Path(config.site_dir),page,config.site_url)
    expected=manifest(pages,VIEWPORTS,identity());provenance=expected['identity'];metadata=read(inventory)
    expected_receipt_names=validate_run_inventory(metadata,provenance,count)
    receipts=[];support=[];artifacts=metadata['artifacts']
    prefix=f"motion-{provenance['run_id']}-{provenance['run_attempt']}-"
    paths=list(directory.glob('*/receipt.json'));require(len(paths)==count+1,'Missing/extra downloaded receipts')
    for p in paths:
        require(p.parent.name in expected_receipt_names,'Wrong attempt receipt directory')
        r=read(p)
        (support if p.parent.name==prefix+'support-receipt' else receipts).append(r)
    require(len(support)==1,'Missing/duplicate support receipt')
    result=validate_shards(expected,receipts,count,artifacts)
    registry=support_registry();sources={}
    for suite in registry['suites']:
        if suite['type']=='prose':
            entries=read(suite['sources_manifest']) if 'sources_manifest' in suite else suite['sources']
            sources[suite['id']]=[x if isinstance(x,str) else x['source'] for x in entries]
    result['support']=validate_support(expected,support[0],artifacts,sources,registry)
    allowed=expected_receipt_names | {g['artifact'] for receipt in [*receipts,*support] for g in receipt['pack']['groups']}
    require({a['name'] for a in artifacts if a['name'].startswith(prefix)}==allowed,'Unexpected current-attempt artifact producer')
    out.parent.mkdir(parents=True,exist_ok=True);out.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))

def gate(directory,inventory,count,out):
    out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps({'status':'running','identity':identity()},indent=2)+'\n')
    try:
        return _gate(directory,inventory,count,out)
    except Exception as error:
        out.write_text(json.dumps({'status':'failed','identity':identity(),'error':str(error)},indent=2)+'\n')
        raise


def main():
    p=argparse.ArgumentParser();sub=p.add_subparsers(dest='command',required=True)
    r=sub.add_parser('receipt');r.add_argument('--kind',choices=['shard','support'],required=True);r.add_argument('--output',type=Path,default=Path('browser-receipt'))
    g=sub.add_parser('gate');g.add_argument('--receipts',type=Path,required=True);g.add_argument('--inventory',type=Path,required=True);g.add_argument('--shard-count',type=int,default=4);g.add_argument('--output',type=Path,default=Path('coverage-gate.json'))
    a=p.parse_args()
    if a.command=='receipt':receipt(a.kind,a.output)
    else:gate(a.receipts,a.inventory,a.shard_count,a.output)
if __name__=='__main__':main()
