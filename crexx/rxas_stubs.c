#include <stdio.h>
#include <stddef.h>
ptrdiff_t crexx_host_write_stderr(const char*b,size_t n){ return (ptrdiff_t)fwrite(b,1,n,stderr); }
