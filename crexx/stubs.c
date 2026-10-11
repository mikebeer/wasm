#include <stddef.h>
#include <stdio.h>
#include <errno.h>
/* single threaded WASI: locks are no-ops, threads and dlopen are unavailable */
int pthread_mutex_lock(void*m){return 0;}
int pthread_mutex_unlock(void*m){return 0;}
int pthread_once(int*o,void(*f)(void)){ if(!*o){*o=1;f();} return 0;}
int pthread_mutexattr_init(void*a){return 0;}
int pthread_mutexattr_settype(void*a,int t){return 0;}
int pthread_mutexattr_destroy(void*a){return 0;}
int pthread_mutex_init(void*m,const void*a){return 0;}
int pthread_mutex_destroy(void*m){return 0;}
int pthread_cond_init(void*c,const void*a){return 0;}
int pthread_cond_destroy(void*c){return 0;}
int pthread_cond_wait(void*c,void*m){return 0;}
int pthread_cond_timedwait(void*c,void*m,const void*t){return 110;}
int pthread_cond_broadcast(void*c){return 0;}
int pthread_create(void*t,const void*a,void*(*f)(void*),void*g){return EAGAIN;}
int pthread_join(unsigned long t,void**r){return ESRCH;}
int getpid(void){return 1;}
void *dlopen(const char*f,int m){return 0;}
char *dlerror(void){return "dynamic loading is not available in WebAssembly";}
void *dlsym(void*h,const char*s){return 0;}
int dlclose(void*h){return 0;}
long crexx_host_write_stderr(const char*b,size_t n){ return (long)fwrite(b,1,n,stderr); }
void decnumber_register_rxvm_plugin(void){}
