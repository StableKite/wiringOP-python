#include <stdint.h>
#include <stddef.h>
#include <stdbool.h>
#include <string.h>
#include "devLib/scrollPhat.h"
void scrollPhatPoint(int x, int y, int colour) { (void)x;(void)y;(void)colour; }
void scrollPhatLine(int x0, int y0, int x1, int y1, int colour) { (void)x0;(void)y0;(void)x1;(void)y1;(void)colour; }
void scrollPhatLineTo(int x, int y, int colour) { (void)x;(void)y;(void)colour; }
void scrollPhatRectangle(int x1, int y1, int x2, int y2, int colour, int filled) { (void)x1;(void)y1;(void)x2;(void)y2;(void)colour;(void)filled; }
void scrollPhatUpdate(void) {  }
void scrollPhatClear(void) {  }
int scrollPhatPutchar(int c) { (void)c;return 1; }
void scrollPhatPuts(const char * str) { (void)str; }
void scrollPhatPrintf(const char * message, ...) { (void)message; }
void scrollPhatPrintSpeed(const int cps10) { (void)cps10; }
void scrollPhatIntensity(const int percent) { (void)percent; }
int scrollPhatSetup(void) { return 1; }
