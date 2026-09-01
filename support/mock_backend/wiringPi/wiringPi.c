#include <stdint.h>
#include <stddef.h>
#include <stdbool.h>
#include <string.h>
#include "wiringPi/wiringPi.h"
int wiringPiDebug=0;
const char * piModelNames[16]={0};
const char * piRevisionNames[16]={0};
const char * piMakerNames[16]={0};
const int piMemorySize[8]={0};
struct wiringPiNodeStruct * wiringPiNodes=0;
volatile unsigned int * _wiringPiGpio=0;
volatile unsigned int * _wiringPiPwm=0;
volatile unsigned int * _wiringPiClk=0;
volatile unsigned int * _wiringPiPads=0;
volatile unsigned int * _wiringPiTimer=0;
volatile unsigned int * _wiringPiTimerIrqRaw=0;
void piGpioLayoutOops(const char * why) { (void)why; }
int wiringPiFailure(int fatal, const char * message, ...) { (void)fatal;(void)message;return 1; }
struct wiringPiNodeStruct * wiringPiFindNode(int pin) { (void)pin;return NULL; }
struct wiringPiNodeStruct * wiringPiNewNode(int pinBase, int numPins) { (void)pinBase;(void)numPins;return NULL; }
void wiringPiVersion(int * major, int * minor) { *major=2;*minor=61; }
int wiringPiSetup(void) { return 1; }
int wiringPiSetupSys(void) { return 1; }
int wiringPiSetupGpio(void) { return 1; }
int wiringPiSetupPhys(void) { return 1; }
void pinModeAlt(int pin, int mode) { (void)pin;(void)mode; }
void pinMode(int pin, int mode) { (void)pin;(void)mode; }
void pullUpDnControl(int pin, int pud) { (void)pin;(void)pud; }
int digitalRead(int pin) { (void)pin;return 1; }
void digitalWrite(int pin, int value) { (void)pin;(void)value; }
void pwmWrite(int pin, int value) { (void)pin;(void)value; }
int analogRead(int pin) { (void)pin;return 1; }
void analogWrite(int pin, int value) { (void)pin;(void)value; }
void piBoardId(int * model) { *model=17; }
int wpiPinToGpio(int wpiPin) { (void)wpiPin;return 1; }
int physPinToGpio(int physPin) { (void)physPin;return 1; }
void setPadDrive(int group, int value) { (void)group;(void)value; }
int getAlt(int pin) { (void)pin;return 1; }
void H618_set_pwm_reg(int pin, sunxi_gpio_info * sunxi_gpio_info_ptr) { (void)pin;(void)sunxi_gpio_info_ptr; }
void s905d3_set_gpio_reg(int pin, s905d3_gpio_info * s905d3_gpio_info_ptr) { (void)pin;(void)s905d3_gpio_info_ptr; }
void rk3588_set_pwm_reg(int pin, rk3588_soc_info * rk3588_soc_info_ptr) { (void)pin;(void)rk3588_soc_info_ptr; }
void rk3566_set_pwm_reg(int pin, rk3566_soc_info * rk3566_soc_info_ptr) { (void)pin;(void)rk3566_soc_info_ptr; }
void sunxi_pwm_set_enable(int en) { (void)en; }
void pwmToneWrite(int pin, int freq) { (void)pin;(void)freq; }
void pwmSetMode(int pin, int mode) { (void)pin;(void)mode; }
void pwmSetRange(int pin, unsigned int range) { (void)pin;(void)range; }
void pwmSetClock(int pin, int divisor) { (void)pin;(void)divisor; }
void gpioClockSet(int pin, int freq) { (void)pin;(void)freq; }
unsigned int digitalReadByte(void) { return 1; }
unsigned int digitalReadByte2(void) { return 1; }
void digitalWriteByte(int value) { (void)value; }
void digitalWriteByte2(int value) { (void)value; }
int waitForInterrupt(int pin, int mS) { (void)pin;(void)mS;return 1; }
int wiringPiISR(int pin, int mode, void (*function)(void)) { if(function)function();return 0; }
int piThreadCreate(void *(*fn)(void *)) { if(fn)fn(NULL);return 0; }
void piLock(int key) { (void)key; }
void piUnlock(int key) { (void)key; }
int piHiPri(const int pri) { (void)pri;return 1; }
void delay(unsigned int howLong) { (void)howLong; }
void delayMicroseconds(unsigned int howLong) { (void)howLong; }
unsigned int millis(void) { return 1; }
unsigned int micros(void) { return 1; }
unsigned int readR(unsigned int addr) { (void)addr;return 1; }
void writeR(unsigned int val, unsigned int addr) { (void)val;(void)addr; }
int orangepi_get_gpio_mode(int pin) { (void)pin;return 1; }
int orangepi_set_gpio_mode(int pin, int mode) { (void)pin;(void)mode;return 1; }
int orangepi_digitalRead(int pin) { (void)pin;return 1; }
int orangepi_digitalWrite(int pin, int value) { (void)pin;(void)value;return 1; }
int orangepi_set_gpio_alt(int pin, int mode) { (void)pin;(void)mode;return 1; }
void OrangePi_set_gpio_pullUpDnControl(int pin, int pud) { (void)pin;(void)pud; }
void orangepi_pwm_set_act(int pin, int act_cys) { (void)pin;(void)act_cys; }
void orangepi_pwm_set_period(int pin, unsigned int period_cys) { (void)pin;(void)period_cys; }
void orangepi_pwm_set_clk(int pin, int clk) { (void)pin;(void)clk; }
void orangepi_pwm_set_tone(int pin, int freq) { (void)pin;(void)freq; }
void set_soc_info(void) {  }
