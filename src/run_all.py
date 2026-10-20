#!/usr/bin/env python3
"""One-command reproduction of all FND Network Capture figures and validation checks.
Run `python src/run_all.py` from the repository root.
"""
from pathlib import Path
import argparse
import subprocess
import sys

ROOT=Path(__file__).resolve().parent.parent
SRC=ROOT/'src'

def execute(script, destination):
    destination.mkdir(parents=True,exist_ok=True)
    proc=subprocess.run([sys.executable,str(SRC/script)],cwd=destination,
                        capture_output=True,text=True,check=False)
    (destination/(script.stem+'.log')).write_text(proc.stdout+proc.stderr,encoding='utf-8')
    print(script.name, 'PASS' if proc.returncode==0 else 'FAIL',flush=True)
    if proc.returncode:
        raise RuntimeError(script.name+' failed\n'+(proc.stdout+proc.stderr)[-3000:])

# Some scripts write their outputs next to their own file (__file__). They are copied into the
# output folder and run there, so that src/ is never modified when results are generated.
def execute_copied(script, destination):
    import shutil
    destination.mkdir(parents=True,exist_ok=True)
    working_script=destination/script.name
    shutil.copy2(SRC/script,working_script)
    proc=subprocess.run([sys.executable,str(working_script)],cwd=destination,
                        capture_output=True,text=True,check=False)
    (destination/(script.stem+'.log')).write_text(proc.stdout+proc.stderr,encoding='utf-8')
    working_script.unlink()
    print(script.name, 'PASS' if proc.returncode==0 else 'FAIL',flush=True)
    if proc.returncode:
        raise RuntimeError(script.name+' failed\n'+(proc.stdout+proc.stderr)[-3000:])

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--suite',choices=['all','figures','validation'],default='all')
    args=parser.parse_args()
    if args.suite in ('all','figures'):
        for idx in range(1,7):
            script=Path(f'make_figure{idx}.py')
            if idx==6: execute_copied(script,ROOT/'outputs'/'figures')
            else: execute(script,ROOT/'outputs'/'figures')
    if args.suite in ('all','validation'):
        for name in ('validate_model.py','validate_defensive_reset.py'):
            execute_copied(Path(name),ROOT/'outputs'/'validation'/Path(name).stem)
    print('Completed:',args.suite)

if __name__=='__main__': main()
