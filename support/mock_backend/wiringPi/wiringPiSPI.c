#include <stdint.h>
#include <stddef.h>
#include <stdbool.h>
#include <string.h>
#include "wiringPi/wiringPiSPI.h"
int wiringPiSPIGetFd(int channel) { (void)channel;return 1; }
int wiringPiSPIDataRW(int channel, unsigned char * data, int len) { for(int i=0;i<len;++i)data[i]^=0xA5;return len; }
int wiringPiSPISetupMode(int channel, int port, int speed, int mode) { (void)channel;(void)port;(void)speed;(void)mode;return 1; }
int wiringPiSPISetup(int channel, int speed) { (void)channel;(void)speed;return 1; }
