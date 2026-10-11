#pragma once
#include <stddef.h>
struct addrinfo { int ai_flags, ai_family, ai_socktype, ai_protocol; unsigned ai_addrlen; void *ai_addr; char *ai_canonname; struct addrinfo *ai_next; };
#define AI_PASSIVE 1
#define EAI_FAIL -4
static inline int getaddrinfo(const char*a,const char*b,const struct addrinfo*c,struct addrinfo**d){return EAI_FAIL;}
static inline void freeaddrinfo(struct addrinfo*a){}
static inline const char* gai_strerror(int e){return "no network in WASI";}
