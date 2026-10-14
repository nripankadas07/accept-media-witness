"""Exercise the installed CLI from a directory outside the source tree."""
import json,os,sys,tempfile,subprocess
from pathlib import Path
def main():
    python=sys.argv[1] if len(sys.argv)>1 else sys.executable
    fixture=(Path(__file__).parent/'example.json').resolve()
    with tempfile.TemporaryDirectory() as cwd:
        env={k:v for k,v in os.environ.items() if k!='PYTHONPATH'}
        r=subprocess.run([python,'-m','accept_media_witness',str(fixture)],cwd=cwd,env=env,text=True,capture_output=True,timeout=10)
        assert r.returncode==0,(r.stdout,r.stderr)
        result=json.loads(r.stdout)
        assert result['selected']=='text/plain' and result['offers'][0]['quality_millis']==0
        bad=subprocess.run([python,'-m','accept_media_witness','-'],input='[]',cwd=cwd,env=env,text=True,capture_output=True,timeout=10)
        assert bad.returncode==2 and 'error' in json.loads(bad.stderr),(bad.returncode,bad.stdout,bad.stderr)
        duplicate=subprocess.run([python,'-m','accept_media_witness','-'],input='{"x":1,"x":2}',cwd=cwd,env=env,text=True,capture_output=True,timeout=10)
        assert duplicate.returncode==2 and 'duplicate' in json.loads(duplicate.stderr)['error']
    print('Installed example, malformed input and duplicate JSON rejection passed outside checkout')

if __name__=="__main__":main()
