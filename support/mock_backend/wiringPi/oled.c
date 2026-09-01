#include <stdint.h>
#include <stddef.h>
#include <stdbool.h>
#include <string.h>
#include "wiringPi/oled.h"
int oled_close(struct display_info * disp) { (void)disp;return 1; }
int oled_open(struct display_info * disp, char * filename) { disp->file=42;disp->address=0x3c;(void)filename;return 0; }
int oled_send(struct display_info * disp, struct sized_array * payload) { (void)disp;return payload?payload->size:-1; }
int oled_init(struct display_info * disp) { (void)disp;return 1; }
int oled_send_buffer(struct display_info * disp) { (void)disp;return 1; }
void oled_clear(struct display_info * disp) { (void)disp; }
void oled_putstr(struct display_info * disp, uint8_t line, uint8_t * str) { (void)disp;(void)line;(void)str; }
void oled_putpixel(struct display_info * disp, uint8_t x, uint8_t y, uint8_t on) { (void)disp;(void)x;(void)y;(void)on; }
void oled_putstrto(struct display_info * disp, uint8_t x, uint8_t y, char * str) { (void)disp;(void)x;(void)y;(void)str; }
