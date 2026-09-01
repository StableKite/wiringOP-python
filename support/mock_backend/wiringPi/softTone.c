#include <stdint.h>
#include <stddef.h>
#include <stdbool.h>
#include <string.h>
#include "wiringPi/softTone.h"
int softToneCreate(int pin) { (void)pin;return 1; }
void softToneStop(int pin) { (void)pin; }
void softToneWrite(int pin, int freq) { (void)pin;(void)freq; }
