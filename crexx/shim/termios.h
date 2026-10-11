#pragma once
struct termios { unsigned c_iflag,c_oflag,c_cflag,c_lflag; unsigned char c_cc[32]; };
#define ECHO 8
#define ICANON 2
#define TCSANOW 0
static inline int tcgetattr(int fd,struct termios*t){return -1;}
static inline int tcsetattr(int fd,int a,const struct termios*t){return -1;}
