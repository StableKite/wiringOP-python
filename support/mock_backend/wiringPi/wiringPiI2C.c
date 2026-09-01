#include <stdint.h>
#include <stddef.h>
#include <stdbool.h>
#include <string.h>
#include "wiringPi/wiringPiI2C.h"
int wiringPiI2CRead(int fd) { (void)fd;return 1; }
int wiringPiI2CReadReg8(int fd, int reg) { (void)fd;(void)reg;return 1; }
int wiringPiI2CReadReg16(int fd, int reg) { (void)fd;(void)reg;return 1; }
int wiringPiI2CWrite(int fd, int data) { (void)fd;(void)data;return 1; }
int wiringPiI2CWriteReg8(int fd, int reg, int data) { (void)fd;(void)reg;(void)data;return 1; }
int wiringPiI2CWriteReg16(int fd, int reg, int data) { (void)fd;(void)reg;(void)data;return 1; }
int wiringPiI2CSetupInterface(const char * device, int devId) { (void)device;(void)devId;return 1; }
int wiringPiI2CSetup(const int devId) { (void)devId;return 1; }
