#include <stdint.h>
#include <stddef.h>
#include <stdbool.h>
#include <string.h>
#include "wiringPi/sr595.h"
int sr595Setup(const int pinBase, const int numPins, const int dataPin, const int clockPin, const int latchPin) { (void)pinBase;(void)numPins;(void)dataPin;(void)clockPin;(void)latchPin;return 1; }
