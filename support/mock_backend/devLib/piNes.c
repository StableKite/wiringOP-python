#include <stdint.h>
#include <stddef.h>
#include <stdbool.h>
#include <string.h>
#include "devLib/piNes.h"
int setupNesJoystick(int dPin, int cPin, int lPin) { (void)dPin;(void)cPin;(void)lPin;return 1; }
unsigned int readNesJoystick(int joystick) { (void)joystick;return 1; }
