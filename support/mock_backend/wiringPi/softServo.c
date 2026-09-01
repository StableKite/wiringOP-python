#include <stdint.h>
#include <stddef.h>
#include <stdbool.h>
#include <string.h>
#include "wiringPi/softServo.h"
void softServoWrite(int pin, int value) { (void)pin;(void)value; }
int softServoSetup(int p0, int p1, int p2, int p3, int p4, int p5, int p6, int p7) { (void)p0;(void)p1;(void)p2;(void)p3;(void)p4;(void)p5;(void)p6;(void)p7;return 1; }
