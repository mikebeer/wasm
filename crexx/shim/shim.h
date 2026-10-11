#pragma once
/* POSIX bits that WASI does not provide: declared as stubs that fail with ENOSYS */
#include <errno.h>
#include <stddef.h>
#include <stdlib.h>
#include <time.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <unistd.h>
#define SHIM static inline __attribute__((unused))
/* signals */
#include <signal.h>
#ifndef SA_RESTART
struct sigaction { void (*sa_handler)(int); sigset_t sa_mask; int sa_flags; };
#define SA_RESTART 0
#define SIG_BLOCK 0
#define SIG_SETMASK 2
#endif
SHIM int sigaction(int s,const struct sigaction*a,struct sigaction*o){ if(a&&a->sa_handler) signal(s,a->sa_handler); return 0; }
SHIM int sigemptyset(sigset_t*s){return 0;}
SHIM int sigaddset(sigset_t*s,int n){return 0;}
SHIM int pthread_sigmask(int h,const sigset_t*a,sigset_t*b){return 0;}
SHIM int kill(pid_t p,int s){errno=ENOSYS;return -1;}
SHIM pid_t getppid(void){return 1;}
SHIM pid_t getpgrp(void){return 1;}
SHIM pid_t tcgetpgrp(int fd){return -1;}
SHIM int dup(int fd){errno=ENOSYS;return -1;}
#ifndef F_DUPFD
#define F_DUPFD 0
#endif
SHIM int mkstemps(char*t,int n){errno=ENOSYS;return -1;}
/* time zone */
SHIM void tzset(void){}
static long timezone = 0;
static char *tzname[2] = {"UTC","UTC"};
/* process waiting */
typedef struct { int si_pid, si_status, si_code; } siginfo_t;
#define P_PID 1
#define WEXITED 4
SHIM int waitid(int t,int id,siginfo_t*i,int o){errno=ENOSYS;return -1;}
/* sockets */
#define NI_MAXHOST 1025
#define NI_NUMERICHOST 1
SHIM int getnameinfo(const void*a,unsigned l,char*h,unsigned hl,char*s,unsigned sl,int f){return -1;}
SHIM int setsockopt(int s,int l,int o,const void*v,unsigned n){errno=ENOSYS;return -1;}
SHIM int socket(int d,int t,int p){errno=ENOSYS;return -1;}
#define SO_RCVTIMEO 20
#define SO_SNDTIMEO 21
#define SO_REUSEADDR 2
#define SOL_SOCKET 1
SHIM int connect(int s,const void*a,unsigned l){errno=ENOSYS;return -1;}
#define WNOWAIT 0x01000000
#define CLD_EXITED 1
#define CLD_KILLED 2
#define CLD_DUMPED 3
#include <pthread.h>
SHIM int pipe(int f[2]){errno=ENOSYS;return -1;}
SHIM int dup2(int a,int b){errno=ENOSYS;return -1;}
#define F_DUPFD_CLOEXEC 1030
#define WUNTRACED 2
#define WCONTINUED 8
#define WIFSTOPPED(s) 0
#define WSTOPSIG(s) 0
#define WIFCONTINUED(s) 0
SHIM int bind(int s,const void*a,unsigned l){errno=ENOSYS;return -1;}
SHIM int listen(int s,int b){errno=ENOSYS;return -1;}
SHIM int getpeername(int s,void*a,unsigned*l){errno=ENOSYS;return -1;}
SHIM int getsockname(int s,void*a,unsigned*l){errno=ENOSYS;return -1;}
#define SO_KEEPALIVE 9
SHIM pid_t fork(void){errno=ENOSYS;return -1;}
SHIM int setpgid(pid_t a,pid_t b){errno=ENOSYS;return -1;}
SHIM int execve(const char*p,char*const a[],char*const e[]){errno=ENOSYS;return -1;}
SHIM int execv(const char*p,char*const a[]){errno=ENOSYS;return -1;}
#define NI_NUMERICSERV 2
