#pragma once

#include <stdbool.h>
#include <stdlib.h>


#if defined(ENABLE_TRACE_MALLOC)
	#define TRACE_MALLOC(size) TraceMalloc_malloc(size, __FILE__, __LINE__)
	#define TRACE_FREE(ptr) TraceMalloc_free(ptr)

#else
	#define TRACE_MALLOC(size) malloc(size)
	#define TRACE_FREE(ptr) free(ptr)

#endif


void *TraceMalloc_malloc(size_t size, const char *file, int line);
void TraceMalloc_free(void *ptr);

size_t TraceMalloc_traceLeaks(void);

bool TraceMalloc_Iterator_init(void);
void TraceMalloc_Iterator_dealloc(void);

bool TraceMalloc_Iterator_move(void);
void TraceMalloc_Iterator_item(size_t *size, const char **file, int *line);
