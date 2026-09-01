#include <stdint.h>
#include <stddef.h>
#include <stdbool.h>
#include <string.h>
#include "wiringPi/w25q64.h"
void W25Q64_begin(uint8_t cs) { (void)cs; }
uint8_t W25Q64_readStatusReg1(void) { return 1; }
uint8_t W25Q64_readStatusReg2(void) { return 1; }
void W25Q64_readManufacturer(uint8_t * d) { d[0]=0xEF;d[1]=0x40;d[2]=0x17; }
void W25Q64_readUniqieID(uint8_t * d) { for(int i=0;i<7;++i)d[i]=(uint8_t)(0x10+i); }
bool W25Q64_IsBusy(void) { return true; }
void W25Q64_powerDown(void) {  }
void W25Q64_WriteEnable(void) {  }
void W25Q64_WriteDisable(void) {  }
uint16_t W25Q64_read(uint32_t addr, uint8_t * buf, uint16_t n) { for(uint16_t i=0;i<n;++i)buf[i]=(uint8_t)(addr+i);return n; }
uint16_t W25Q64_fastread(uint32_t addr, uint8_t * buf, uint16_t n) { for(uint16_t i=0;i<n;++i)buf[i]=(uint8_t)(addr+i);return n; }
bool W25Q64_eraseSector(uint16_t sect_no, bool flgwait) { (void)sect_no;(void)flgwait;return true; }
bool W25Q64_erase64Block(uint16_t blk_no, bool flgwait) { (void)blk_no;(void)flgwait;return true; }
bool W25Q64_erase32Block(uint16_t blk_no, bool flgwait) { (void)blk_no;(void)flgwait;return true; }
bool W25Q64_eraseAll(bool flgwait) { (void)flgwait;return true; }
uint16_t W25Q64_pageWrite(uint16_t sect_no, uint16_t inaddr, uint8_t * data, uint8_t n) { (void)sect_no;(void)inaddr;(void)data;return n; }
