#include <stdint.h>
#include <stddef.h>
#include <stdbool.h>
#include <string.h>
#include "devLib/lcd128x64.h"
void lcd128x64setOrigin(int x, int y) { (void)x;(void)y; }
void lcd128x64setOrientation(int orientation) { (void)orientation; }
void lcd128x64orientCoordinates(int * x, int * y) { *x+=1;*y+=2; }
void lcd128x64getScreenSize(int * x, int * y) { *x=128;*y=64; }
void lcd128x64point(int x, int y, int colour) { (void)x;(void)y;(void)colour; }
void lcd128x64line(int x0, int y0, int x1, int y1, int colour) { (void)x0;(void)y0;(void)x1;(void)y1;(void)colour; }
void lcd128x64lineTo(int x, int y, int colour) { (void)x;(void)y;(void)colour; }
void lcd128x64rectangle(int x1, int y1, int x2, int y2, int colour, int filled) { (void)x1;(void)y1;(void)x2;(void)y2;(void)colour;(void)filled; }
void lcd128x64circle(int x, int y, int r, int colour, int filled) { (void)x;(void)y;(void)r;(void)colour;(void)filled; }
void lcd128x64ellipse(int cx, int cy, int xRadius, int yRadius, int colour, int filled) { (void)cx;(void)cy;(void)xRadius;(void)yRadius;(void)colour;(void)filled; }
void lcd128x64putchar(int x, int y, int c, int bgCol, int fgCol) { (void)x;(void)y;(void)c;(void)bgCol;(void)fgCol; }
void lcd128x64puts(int x, int y, const char * str, int bgCol, int fgCol) { (void)x;(void)y;(void)str;(void)bgCol;(void)fgCol; }
void lcd128x64update(void) {  }
void lcd128x64clear(int colour) { (void)colour; }
int lcd128x64setup(void) { return 1; }
