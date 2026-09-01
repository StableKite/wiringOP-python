#include <stdint.h>
#include <stddef.h>
#include <stdbool.h>
#include <string.h>
#include "wiringPi/wiringSerial.h"
struct serialContext { int fd; int ownFd; int cancelRead[2]; int cancelWrite[2]; };
static serialConfig mock_serial_config={.structSize=sizeof(serialConfig),.version=SERIAL_CONFIG_VERSION,.baud=9600,.dataBits=8,.stopBits=SERIAL_STOP_BITS_ONE};
static serialRS485Config mock_rs485={.structSize=sizeof(serialRS485Config)};
static struct serialContext mock_context={.fd=7};
static int mock_rx_trigger=16;static int mock_wakeup=0;
int serialOpen(const char * device, const int baud) { (void)device;mock_serial_config.baud=(uint32_t)baud;return 7; }
void serialClose(const int fd) { (void)fd; }
void serialFlush(const int fd) { (void)fd; }
void serialPutchar(const int fd, const unsigned char c) { (void)fd;(void)c; }
void serialPuts(const int fd, const char * s) { (void)fd;(void)s; }
void serialPrintf(const int fd, const char * message, ...) { (void)fd;(void)message; }
int serialDataAvail(const int fd) { (void)fd;return 1; }
int serialGetchar(const int fd) { (void)fd;return 1; }
void serialConfigInit(serialConfig * config) { memset(config,0,sizeof(*config));config->structSize=sizeof(*config);config->version=SERIAL_CONFIG_VERSION;config->baud=9600;config->dataBits=8;config->parity=SERIAL_PARITY_NONE;config->stopBits=SERIAL_STOP_BITS_ONE;config->xonChar=0x11;config->xoffChar=0x13; }
int serialOpenConfig(const char * device, const serialConfig * config) { (void)device;if(config)mock_serial_config=*config;return 7; }
int serialGetConfig(const int fd, serialConfig * config) { (void)fd;*config=mock_serial_config;return 0; }
int serialSetConfig(const int fd, const serialConfig * config) { (void)fd;mock_serial_config=*config;return 0; }
int serialGetBaud(const int fd, unsigned int * baud) { (void)fd;*baud=mock_serial_config.baud;return 0; }
int serialSetBaud(const int fd, const unsigned int baud) { (void)fd;mock_serial_config.baud=baud;return 0; }
ssize_t serialRead(const int fd, void * buffer, const size_t count) { (void)fd;for(size_t i=0;i<count;++i)((unsigned char*)buffer)[i]=(unsigned char)(0x30+(i%10));return(ssize_t)count; }
ssize_t serialWrite(const int fd, const void * buffer, const size_t count) { (void)fd;(void)buffer;return(ssize_t)count; }
ssize_t serialReadTimeout(const int fd, void * buffer, const size_t count, const int timeoutMs, const int interByteTimeoutMs) { (void)fd;(void)timeoutMs;(void)interByteTimeoutMs;for(size_t i=0;i<count;++i)((unsigned char*)buffer)[i]=(unsigned char)(0x30+(i%10));return(ssize_t)count; }
ssize_t serialWriteTimeout(const int fd, const void * buffer, const size_t count, const int timeoutMs) { (void)fd;(void)buffer;(void)timeoutMs;return(ssize_t)count; }
int serialDrain(const int fd) { (void)fd;return 1; }
int serialFlushInput(const int fd) { (void)fd;return 1; }
int serialFlushOutput(const int fd) { (void)fd;return 1; }
int serialInputWaiting(const int fd) { (void)fd;return 3; }
int serialOutputWaiting(const int fd) { (void)fd;return 3; }
int serialSendBreak(const int fd, const unsigned int durationMs) { (void)fd;(void)durationMs;return 1; }
int serialSetBreak(const int fd, const int enabled) { (void)fd;(void)enabled;return 1; }
int serialGetModemLines(const int fd, unsigned int * lines) { (void)fd;*lines=SERIAL_MODEM_RTS|SERIAL_MODEM_DTR|SERIAL_MODEM_CTS;return 0; }
int serialSetModemLines(const int fd, const unsigned int setMask, const unsigned int clearMask) { (void)fd;(void)setMask;(void)clearMask;return 1; }
int serialSetRTS(const int fd, const int enabled) { (void)fd;(void)enabled;return 1; }
int serialSetDTR(const int fd, const int enabled) { (void)fd;(void)enabled;return 1; }
int serialGetCTS(const int fd) { (void)fd;return 1; }
int serialGetDSR(const int fd) { (void)fd;return 1; }
int serialGetRI(const int fd) { (void)fd;return 1; }
int serialGetCD(const int fd) { (void)fd;return 1; }
int serialSetInputFlow(const int fd, const int enabled) { (void)fd;(void)enabled;return 1; }
int serialSetOutputFlow(const int fd, const int enabled) { (void)fd;(void)enabled;return 1; }
int serialSetExclusive(const int fd, const int enabled) { (void)fd;(void)enabled;return 1; }
int serialGetLowLatency(const int fd) { (void)fd;return 1; }
int serialSetLowLatency(const int fd, const int enabled) { (void)fd;(void)enabled;return 1; }
int serialGetCounters(const int fd, serialCounters * counters) { (void)fd;memset(counters,0,sizeof(*counters));counters->structSize=sizeof(*counters);counters->rx=12;counters->tx=34;return 0; }
int serialTxEmpty(const int fd) { (void)fd;return 1; }
int serialGetRS485(const int fd, serialRS485Config * config) { (void)fd;*config=mock_rs485;config->structSize=sizeof(*config);return 0; }
int serialSetRS485(const int fd, const serialRS485Config * config) { (void)fd;mock_rs485=*config;return 0; }
int serialGetRxTrigger(const int fd) { (void)fd;return mock_rx_trigger; }
int serialSetRxTrigger(const int fd, const unsigned int bytes) { (void)fd;mock_rx_trigger=(int)bytes;return 0; }
int serialGetWakeup(const int fd) { (void)fd;return mock_wakeup; }
int serialSetWakeup(const int fd, const int enabled) { (void)fd;mock_wakeup=enabled;return 0; }
int serialGetHardwareInfo(const int fd, serialHardwareInfo * info) { (void)fd;memset(info,0,sizeof(*info));info->structSize=sizeof(*info);info->hardwareType=SERIAL_HARDWARE_RK3588_UART;info->fifoSize=64;info->capabilities=SERIAL_CAP_CUSTOM_BAUD|SERIAL_CAP_RTS_CTS|SERIAL_CAP_RK3588_UART|SERIAL_CAP_FIFO|SERIAL_CAP_CANCEL_IO;return 0; }
int serialGetCapabilities(const int fd, uint64_t * capabilities) { (void)fd;*capabilities=SERIAL_CAP_CUSTOM_BAUD|SERIAL_CAP_RTS_CTS|SERIAL_CAP_RK3588_UART|SERIAL_CAP_FIFO|SERIAL_CAP_CANCEL_IO;return 0; }
serialContext * serialContextOpen(const char * device, const serialConfig * config) { (void)device;if(config)mock_serial_config=*config;mock_context.fd=7;return &mock_context; }
serialContext * serialContextFromFd(const int fd, const int takeOwnership) { (void)takeOwnership;mock_context.fd=fd;return &mock_context; }
void serialContextClose(serialContext * context) { (void)context; }
int serialContextGetFd(const serialContext * context) { return context?context->fd:-1; }
ssize_t serialContextRead(serialContext * context, void * buffer, const size_t count, const int timeoutMs, const int interByteTimeoutMs) { (void)timeoutMs;(void)interByteTimeoutMs;if(!context)return-1;for(size_t i=0;i<count;++i)((unsigned char*)buffer)[i]=(unsigned char)(0x30+(i%10));return(ssize_t)count; }
ssize_t serialContextWrite(serialContext * context, const void * buffer, const size_t count, const int timeoutMs) { (void)timeoutMs;if(!context)return-1;(void)buffer;return(ssize_t)count; }
int serialContextCancelRead(serialContext * context) { return context?0:-1; }
int serialContextCancelWrite(serialContext * context) { return context?0:-1; }
