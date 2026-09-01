#include <stdint.h>
#include <stddef.h>
#include <stdbool.h>
#include <string.h>
#include "wiringPi/wiringShift.h"
uint8_t shiftIn(uint8_t dPin, uint8_t cPin, uint8_t order) { (void)dPin;(void)cPin;(void)order;return 1; }
void shiftOut(uint8_t dPin, uint8_t cPin, uint8_t order, uint8_t val) { (void)dPin;(void)cPin;(void)order;(void)val; }
