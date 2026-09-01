#include <stdint.h>
#include <stddef.h>
#include <stdbool.h>
#include <string.h>
#include "devLib/lcd.h"
void lcdHome(const int fd) { (void)fd; }
void lcdClear(const int fd) { (void)fd; }
void lcdDisplay(const int fd, int state) { (void)fd;(void)state; }
void lcdCursor(const int fd, int state) { (void)fd;(void)state; }
void lcdCursorBlink(const int fd, int state) { (void)fd;(void)state; }
void lcdSendCommand(const int fd, unsigned char command) { (void)fd;(void)command; }
void lcdPosition(const int fd, int x, int y) { (void)fd;(void)x;(void)y; }
void lcdCharDef(const int fd, int index, unsigned char * data) { (void)fd;(void)index;(void)data; }
void lcdPutchar(const int fd, unsigned char data) { (void)fd;(void)data; }
void lcdPuts(const int fd, const char * string) { (void)fd;(void)string; }
void lcdPrintf(const int fd, const char * message, ...) { (void)fd;(void)message; }
int lcdInit(const int rows, const int cols, const int bits, const int rs, const int strb, const int d0, const int d1, const int d2, const int d3, const int d4, const int d5, const int d6, const int d7) { (void)rows;(void)cols;(void)bits;(void)rs;(void)strb;(void)d0;(void)d1;(void)d2;(void)d3;(void)d4;(void)d5;(void)d6;(void)d7;return 1; }
