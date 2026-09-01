#include <stdint.h>
#include <stddef.h>
#include <stdbool.h>
#include <string.h>
#include "devLib/ds1302.h"
unsigned int ds1302rtcRead(const int reg) { (void)reg;return 1; }
void ds1302rtcWrite(const int reg, const unsigned int data) { (void)reg;(void)data; }
unsigned int ds1302ramRead(const int addr) { (void)addr;return 1; }
void ds1302ramWrite(const int addr, const unsigned int data) { (void)addr;(void)data; }
void ds1302clockRead(int * clockData) { for(int i=0;i<8;++i)clockData[i]=10+i; }
void ds1302clockWrite(const int * clockData) { (void)clockData; }
void ds1302trickleCharge(const int diodes, const int resistors) { (void)diodes;(void)resistors; }
void ds1302setup(const int clockPin, const int dataPin, const int csPin) { (void)clockPin;(void)dataPin;(void)csPin; }
