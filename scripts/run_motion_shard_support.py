"""Run every existing support suite; keep a fail-closed execution receipt even on failure."""
import json,os,subprocess,sys,time
from pathlib import Path
from motion_shard_contract import identity
from motion_shard_contract import support_registry,sha

def commands():
    return [(s['id'],s['command']) for s in support_registry()['suites']]

def main():
    out=Path('artifacts/support-execution');out.mkdir(parents=True,exist_ok=True)
    registry=support_registry();report={'identity':identity(),'registry_sha256':sha(registry),'status':'running','suites':[]}
    try:
        for entry in registry['suites']:
            suite,args=entry['id'],entry['command'];env={**os.environ,**entry.get('env',{})}
            item={'suite':suite,'command':[sys.executable,*args],'status':'running'};report['suites'].append(item);start=time.monotonic()
            print(f'Running entire support suite {suite}',flush=True)
            result=subprocess.run([sys.executable,*args],env=env)
            item.update(returncode=result.returncode,status='passed' if result.returncode==0 else 'failed',seconds=time.monotonic()-start)
        report['status']='passed' if all(x['status']=='passed' for x in report['suites']) else 'failed'
    finally:(out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    return 0 if report['status']=='passed' else 1
if __name__=='__main__':
    if '--roots' in sys.argv:print(' '.join([*dict(commands()),'support-execution']))
    else:sys.exit(main())
