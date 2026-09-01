#include <stdint.h>
#include <stddef.h>
#include <stdbool.h>
#include <string.h>
#include "wiringPi/drcSerial.h"
int drcSetupSerial(const int pinBase, const int numPins, const char * device, const int baud) { (void)pinBase;(void)numPins;(void)device;(void)baud;return 1; }
