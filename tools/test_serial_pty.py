#!/usr/bin/env python3
from __future__ import annotations
import argparse
import subprocess
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
C_TEST = r'''#include <assert.h>
#include <dirent.h>
#include <errno.h>
#include <stdlib.h>
#include <time.h>
#include <pty.h>
#include <pthread.h>
#include <stdint.h>
#include <stdio.h>
#include <string.h>
#include <unistd.h>
#include <fcntl.h>
#include "wiringPi/wiringSerial.h"

typedef struct { serialContext *ctx; ssize_t result; } read_job;
typedef struct { serialContext *ctx; const unsigned char *data; size_t count; ssize_t result; } write_job;
static void *reader(void *arg) {
  read_job *j=(read_job*)arg; unsigned char b[16];
  j->result=serialContextRead(j->ctx,b,sizeof(b),-1,-1);
  return NULL;
}
static void *writer(void *arg) {
  write_job *j=(write_job*)arg;
  j->result=serialContextWrite(j->ctx,j->data,j->count,1000);
  return NULL;
}
static int fd_count(void) {
  DIR *d=opendir("/proc/self/fd"); struct dirent *de; int n=0;
  assert(d!=NULL); while((de=readdir(d))!=NULL) if(de->d_name[0]!='.') ++n; closedir(d); return n;
}
static void drain_nonblocking(int fd, char *buf, size_t size) {
  int fl=fcntl(fd,F_GETFL); assert(fl>=0); assert(fcntl(fd,F_SETFL,fl|O_NONBLOCK)==0);
  while(read(fd,buf,size)>0){} assert(errno==EAGAIN || errno==EWOULDBLOCK); assert(fcntl(fd,F_SETFL,fl)==0);
}
int main(void) {
  int master, slave, fd; char name[128], buf[64];
  serialConfig cfg, got; unsigned int baud=0; const char payload[]="hello-uart"; ssize_t n;
  serialContext *ctx, *ownedCtx; pthread_t th; read_job job; write_job wjob;
  int beforeFds, afterFds, ownedFd, badPipe[2]; unsigned char *bigWrite; size_t bigCount=8u*1024u*1024u;
  assert(openpty(&master,&slave,name,NULL,NULL)==0); close(slave);
  serialConfigInit(&cfg); cfg.baud=115200; cfg.dataBits=8; cfg.parity=SERIAL_PARITY_NONE; cfg.stopBits=SERIAL_STOP_BITS_ONE;
  fd=serialOpenConfig(name,&cfg); assert(fd>=0); assert(serialGetConfig(fd,&got)==0); assert(got.baud==115200);
  assert(serialGetBaud(fd,&baud)==0 && baud==115200); assert(serialSetBaud(fd,123456)==0); assert(serialGetBaud(fd,&baud)==0 && baud==123456);
  assert(write(master,payload,sizeof(payload)-1)==(ssize_t)(sizeof(payload)-1));
  memset(buf,0,sizeof(buf)); n=serialReadTimeout(fd,buf,sizeof(payload)-1,1000,100); assert(n==(ssize_t)(sizeof(payload)-1)); assert(memcmp(buf,payload,sizeof(payload)-1)==0);
  n=serialWriteTimeout(fd,payload,sizeof(payload)-1,1000); assert(n==(ssize_t)(sizeof(payload)-1)); memset(buf,0,sizeof(buf)); assert(read(master,buf,sizeof(payload)-1)==(ssize_t)(sizeof(payload)-1)); assert(memcmp(buf,payload,sizeof(payload)-1)==0);
  assert(serialFlushInput(fd)==0); assert(serialFlushOutput(fd)==0); assert(serialDrain(fd)==0); assert(serialSetInputFlow(fd,1)==0); assert(serialSetOutputFlow(fd,1)==0); assert(serialSetExclusive(fd,1)==0); assert(serialSetExclusive(fd,0)==0);
  { uint64_t caps=0; serialHardwareInfo hw; assert(serialGetCapabilities(fd,&caps)==0); assert(serialGetHardwareInfo(fd,&hw)==0); assert((caps&SERIAL_CAP_XON_XOFF)!=0); assert((caps&SERIAL_CAP_CANCEL_IO)!=0); }
  while (serialInputWaiting(fd)>0) (void)serialGetchar(fd);
  drain_nonblocking(master,buf,sizeof(buf));

  /* A context created without ownership gets a private tty fd and must not close the caller fd. */
  ctx=serialContextFromFd(fd,0); assert(ctx!=NULL); assert(serialContextGetFd(ctx)>=0); assert(serialContextGetFd(ctx)!=fd);
  assert(write(master,"ctx",3)==3); memset(buf,0,sizeof(buf)); assert(serialContextRead(ctx,buf,3,1000,100)==3); assert(memcmp(buf,"ctx",3)==0);
  assert(serialContextWrite(ctx,"out",3,1000)==3); memset(buf,0,sizeof(buf)); assert(read(master,buf,3)==3); assert(memcmp(buf,"out",3)==0);

  /* A stale pre-cancel is consumed at operation start and must not poison later I/O. */
  assert(serialContextCancelRead(ctx)==0); assert(serialContextCancelRead(ctx)==0);
  assert(serialContextRead(ctx,buf,1,20,-1)==0);
  assert(write(master,"p",1)==1); assert(serialContextRead(ctx,buf,1,1000,100)==1 && buf[0]=='p');

  /* During-poll cancellation is prompt; repeated signals are drained together. */
  job.ctx=ctx; job.result=-99; assert(pthread_create(&th,NULL,reader,&job)==0); usleep(50000);
  assert(serialContextCancelRead(ctx)==0); assert(serialContextCancelRead(ctx)==0);
  assert(pthread_join(th,NULL)==0); assert(job.result==0);
  assert(write(master,"r",1)==1); assert(serialContextRead(ctx,buf,1,1000,100)==1 && buf[0]=='r');

  /* Fill the pty output queue with a bulk write and cancel the POLLOUT wait. */
  bigWrite=(unsigned char*)malloc(bigCount); assert(bigWrite!=NULL); memset(bigWrite,0x5a,bigCount);
  wjob.ctx=ctx; wjob.data=bigWrite; wjob.count=bigCount; wjob.result=-99;
  assert(pthread_create(&th,NULL,writer,&wjob)==0); usleep(100000);
  assert(serialContextCancelWrite(ctx)==0); assert(serialContextCancelWrite(ctx)==0);
  assert(pthread_join(th,NULL)==0); assert(wjob.result>=0 && (size_t)wjob.result<bigCount); free(bigWrite);
  drain_nonblocking(master,buf,sizeof(buf));
  assert(serialContextWrite(ctx,"z",1,1000)==1); assert(read(master,buf,1)==1 && buf[0]=='z');
  serialContextClose(ctx); assert(fcntl(fd,F_GETFD)>=0);

  /* Repeated create/close must not leak any pipe or tty descriptors. */
  beforeFds=fd_count();
  for(int i=0;i<64;++i){ctx=serialContextFromFd(fd,0);assert(ctx!=NULL);serialContextClose(ctx);}
  afterFds=fd_count(); assert(afterFds==beforeFds);

  /* takeOwnership=1 closes the supplied fd only after a valid context exists. */
  ownedFd=serialOpenConfig(name,&cfg); assert(ownedFd>=0);
  ownedCtx=serialContextFromFd(ownedFd,1); assert(ownedCtx!=NULL);
  errno=0; assert(fcntl(ownedFd,F_GETFD)==-1 && errno==EBADF);
  assert(serialContextWrite(ownedCtx,"o",1,1000)==1); assert(read(master,buf,1)==1 && buf[0]=='o');
  serialContextClose(ownedCtx);

  /* Failed ownership transfer must leave the caller's non-tty fd untouched. */
  assert(pipe(badPipe)==0); errno=0; assert(serialContextFromFd(badPipe[0],1)==NULL); assert(errno==ENOTTY);
  assert(fcntl(badPipe[0],F_GETFD)>=0); close(badPipe[0]); close(badPipe[1]);

  serialClose(fd); close(master); puts("WIRING_SERIAL_EXT_PTY_OK"); return 0;
}
'''

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument('--wiringop-source', type=Path, default=ROOT / 'build/upstream/wiringOP')
    ns = ap.parse_args()
    src = ns.wiringop_source.resolve()
    serial_c = src / 'wiringPi/wiringSerial.c'
    if not serial_c.is_file():
        raise SystemExit(f'missing patched wiringSerial.c: {serial_c}')
    with tempfile.TemporaryDirectory(prefix='wiringserial-pty-') as td_s:
        td = Path(td_s)
        test_c = td / 'test.c'
        exe = td / 'test'
        test_c.write_text(C_TEST)
        cmd = [
            'gcc','-std=gnu11','-D_GNU_SOURCE','-Wall','-Wextra','-Werror','-pthread',
            '-I',str(src),'-I',str(src/'wiringPi'),str(test_c),str(serial_c),'-lutil','-o',str(exe),
        ]
        subprocess.run(cmd, check=True)
        cp = subprocess.run([str(exe)], check=True, text=True, capture_output=True)
        print(cp.stdout.strip())
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
