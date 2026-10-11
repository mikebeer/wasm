#include <stdio.h>
/* WASI has no tmpfile(); apl only uses it for )COPY of named objects and
   already reports "cannot create a temporary file" when it returns NULL. */
FILE *tmpfile(void) { return NULL; }
/* no shell in WASI */
int system(const char *cmd) { (void)cmd; return -1; }
