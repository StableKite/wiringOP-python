#!/usr/bin/env python3
from __future__ import annotations
import argparse, shutil, subprocess
from pathlib import Path

PINNED = "a7921ca2f5c124203be10d3418db70a2e15f3c10"

def run(*args: str, cwd: Path | None = None) -> str:
    return subprocess.check_output(args, cwd=cwd, text=True).strip()

def main() -> int:
    ap=argparse.ArgumentParser()
    ap.add_argument('--project-root',type=Path,default=Path(__file__).resolve().parents[1])
    ap.add_argument('--output',type=Path)
    ns=ap.parse_args(); root=ns.project_root.resolve(); upstream=root/'extern/wiringOP'; out=(ns.output or root/'build/upstream/wiringOP').resolve()
    if not upstream.is_dir(): raise SystemExit(f'missing submodule: {upstream}')
    head=run('git','rev-parse','HEAD',cwd=upstream)
    if head!=PINNED: raise SystemExit(f'wiringOP HEAD mismatch: {head} != {PINNED}')
    if run('git','status','--porcelain',cwd=upstream): raise SystemExit('extern/wiringOP must be clean before applying project overlays')
    patches=sorted((root/'patches/wiringOP').glob('*.patch'))
    for patch in patches: subprocess.run(['git','apply','--check',str(patch)],cwd=upstream,check=True)
    if out.exists(): shutil.rmtree(out)
    out.parent.mkdir(parents=True,exist_ok=True); shutil.copytree(upstream,out,ignore=shutil.ignore_patterns('.git'),symlinks=True)
    for patch in patches: subprocess.run(['git','apply','--unsafe-paths','--directory',str(out),str(patch)],cwd=root,check=True)
    print(out); return 0
if __name__=='__main__': raise SystemExit(main())
