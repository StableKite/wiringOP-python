#include <stdint.h>
#include <stddef.h>
#include <stdbool.h>
#include <string.h>
#include "wiringPi/softPwm.h"
int softPwmCreate(int pin, int value, int range) { (void)pin;(void)value;(void)range;return 1; }
void softPwmWrite(int pin, int value) { (void)pin;(void)value; }
void softPwmStop(int pin) { (void)pin; }
