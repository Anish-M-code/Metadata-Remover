#ifndef COMMON_H
#define COMMON_H

#include <errno.h>
#include <stdio.h>
#include <stdlib.h>

// macros for handling errors
#define handle_error_en(en, msg)    do { errno = en; perror(msg); exit(EXIT_FAILURE); } while (0) //if errno is NOT set
#define handle_error(msg)           do { perror(msg); exit(EXIT_FAILURE); } while (0) //if errno is SET

#endif
