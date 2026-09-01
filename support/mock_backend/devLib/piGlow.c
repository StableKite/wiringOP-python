#include <stdint.h>
#include <stddef.h>
#include <stdbool.h>
#include <string.h>
#include "devLib/piGlow.h"
void piGlow1(const int leg, const int ring, const int intensity) { (void)leg;(void)ring;(void)intensity; }
void piGlowLeg(const int leg, const int intensity) { (void)leg;(void)intensity; }
void piGlowRing(const int ring, const int intensity) { (void)ring;(void)intensity; }
void piGlowSetup(int clear) { (void)clear; }
