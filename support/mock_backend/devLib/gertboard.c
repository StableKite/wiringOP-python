#include <stdint.h>
#include <stddef.h>
#include <stdbool.h>
#include <string.h>
#include "devLib/gertboard.h"
void gertboardAnalogWrite(const int chan, const int value) { (void)chan;(void)value; }
int gertboardAnalogRead(const int chan) { (void)chan;return 1; }
int gertboardSPISetup(void) { return 1; }
int gertboardAnalogSetup(const int pinBase) { (void)pinBase;return 1; }
