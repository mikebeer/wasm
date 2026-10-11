#pragma once
#include <sys/types.h>
#define WNOHANG 1
#define WIFEXITED(s) 1
#define WEXITSTATUS(s) (s)
#define WIFSIGNALED(s) 0
#define WTERMSIG(s) 0
static inline pid_t waitpid(pid_t p,int*s,int o){return -1;}
