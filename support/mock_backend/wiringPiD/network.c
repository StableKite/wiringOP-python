#include <stdint.h>
#include <stddef.h>
#include <stdbool.h>
#include <string.h>
#include "wiringPiD/network.h"
char * getClientIP(void) { return "127.0.0.1"; }
int setupServer(int serverPort) { (void)serverPort;return 1; }
int sendGreeting(int clientFd) { (void)clientFd;return 1; }
int sendChallenge(int clientFd) { (void)clientFd;return 1; }
int getResponse(int clientFd) { return clientFd+100; }
int passwordMatch(const char * password) { (void)password;return 1; }
void closeServer(int clientFd) { (void)clientFd; }
