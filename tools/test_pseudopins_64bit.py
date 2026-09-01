#!/usr/bin/env python3
from __future__ import annotations
import argparse
import subprocess
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
C_TEST = r'''#include <assert.h>
#include <string.h>
#include <sys/mman.h>
#include <unistd.h>
#include "wiringPi/wiringPi.h"
#include "wiringPi/pseudoPins.h"

static struct wiringPiNodeStruct node;
struct wiringPiNodeStruct *wiringPiNewNode(int pinBase, int numPins) {
  memset(&node, 0, sizeof(node)); node.pinBase=pinBase; node.pinMax=pinBase+numPins-1; return &node;
}
int main(void) {
  shm_unlink("wiringPiPseudoPins");
  assert(pseudoPinsSetup(100)==TRUE);
  assert(node.analogRead!=NULL && node.analogWrite!=NULL);
  node.analogWrite(&node,100,0x12345678);
  node.analogWrite(&node,163,-77);
  assert(node.analogRead(&node,100)==0x12345678);
  assert(node.analogRead(&node,163)==-77);
#if UINTPTR_MAX > UINT32_MAX
  /* On 64-bit the reconstructed address must retain high bits when present. */
  assert(node.data0!=0 || node.data1!=0);
#endif
  close(node.fd); shm_unlink("wiringPiPseudoPins");
  return 0;
}
'''

def main() -> int:
    ap=argparse.ArgumentParser(); ap.add_argument('--wiringop-source',type=Path,default=ROOT/'build/upstream/wiringOP'); ns=ap.parse_args()
    src=ns.wiringop_source.resolve()
    with tempfile.TemporaryDirectory(prefix='pseudopins64-') as td_s:
        td=Path(td_s); c=td/'test.c'; exe=td/'test'; c.write_text(C_TEST)
        cmd=['gcc','-std=gnu11','-D_GNU_SOURCE','-DCONFIG_ORANGEPI','-Wall','-Wextra','-Werror',
             '-I',str(src),'-I',str(src/'wiringPi'),str(c),str(src/'wiringPi/pseudoPins.c'),'-lrt','-o',str(exe)]
        subprocess.run(cmd,check=True); subprocess.run([str(exe)],check=True)
    print('PSEUDOPINS_64BIT_OK'); return 0
if __name__=='__main__': raise SystemExit(main())
