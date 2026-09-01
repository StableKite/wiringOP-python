#include <stdint.h>
#include <stddef.h>
#include <stdbool.h>
#include <string.h>
#include "devLib/maxdetect.h"
int maxDetectRead(const int pin, unsigned char * buffer) { buffer[0]=1;buffer[1]=2;buffer[2]=3;buffer[3]=4;return 1; }
int readRHT03(const int pin, int * temp, int * rh) { *temp=234;*rh=567;return 1; }
