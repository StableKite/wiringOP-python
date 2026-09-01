#!/usr/bin/env python3
from __future__ import annotations
import argparse, json, re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

def paths_for(header:str):
    p=Path(header).with_suffix('')
    return ROOT/'src'/p.with_suffix('.cpp'), ROOT/'tests'/p.with_suffix('.py'), ROOT/'docs'/p.with_suffix('.md'), ROOT/'stubs'/p.with_suffix('.pyi')

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--allow-missing-stubs',action='store_true'); ns=ap.parse_args()
    m=json.loads((ROOT/'api_manifest.json').read_text())
    hs=[h['path'] for h in m['headers']]
    errors=[]
    if len(hs)!=54: errors.append(f'expected 54 headers, got {len(hs)}')
    expected={d:set() for d in ('src','tests','docs','stubs')}
    for h in hs:
        for key,p in zip(expected,paths_for(h)):
            expected[key].add(p.relative_to(ROOT).as_posix())
            if key=='stubs' and ns.allow_missing_stubs: continue
            if not p.is_file(): errors.append(f'missing {key}: {p.relative_to(ROOT)}')
    for key,ext in [('src','.cpp'),('tests','.py'),('docs','.md')]:
        actual={p.relative_to(ROOT).as_posix() for p in (ROOT/key).rglob(f'*{ext}') if p.is_file() and '__pycache__' not in p.parts}
        extra=sorted(actual-expected[key]); missing=sorted(expected[key]-actual)
        if extra: errors.append(f'extra {key}: {extra[:10]}')
        if missing: errors.append(f'missing mirrored {key}: {missing[:10]}')
    bad=[p for p in (ROOT/'tests').rglob('test_*.py')]
    if bad: errors.append('test_ prefix files: '+', '.join(str(p.relative_to(ROOT)) for p in bad))
    pp=(ROOT/'pyproject.toml').read_text()
    if 'python_files = ["*.py"]' not in pp: errors.append('pytest python_files must be ["*.py"]')
    if '--import-mode=importlib' not in pp: errors.append('pytest must use --import-mode=importlib')
    # gitlink exact commit
    try:
        import subprocess
        mode=subprocess.check_output(['git','ls-files','-s','extern/wiringOP'],cwd=ROOT,text=True).split()[0]
        if mode!='160000': errors.append(f'extern/wiringOP not gitlink: mode={mode}')
        head=subprocess.check_output(['git','-C',str(ROOT/'extern/wiringOP'),'rev-parse','HEAD'],text=True).strip()
        if head!='a7921ca2f5c124203be10d3418db70a2e15f3c10': errors.append(f'wrong wiringOP commit {head}')
        dirty=subprocess.check_output(['git','-C',str(ROOT/'extern/wiringOP'),'status','--porcelain'],text=True)
        if dirty: errors.append('extern/wiringOP dirty')
    except Exception as e: errors.append(f'gitlink audit failed: {e}')
    if errors: raise SystemExit('LAYOUT AUDIT FAILED\n- '+'\n- '.join(errors))
    print(f'LAYOUT_AUDIT_OK headers={len(hs)} src=54 tests=54 docs=54 stubs={"optional" if ns.allow_missing_stubs else 54}')
if __name__=='__main__': main()
