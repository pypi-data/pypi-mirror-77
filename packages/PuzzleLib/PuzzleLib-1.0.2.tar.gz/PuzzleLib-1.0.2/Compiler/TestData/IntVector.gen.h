#pragma once

#include <stddef.h>
#include <stdbool.h>


typedef struct IntVector
{
	int *ptr;
	size_t size, capacity;
}
IntVector;


void IntVector_init(IntVector *self);
void IntVector_dealloc(IntVector *self);

void IntVector_reserve(IntVector *self, size_t capacity);
void IntVector_append(IntVector *self, int elem);
void IntVector_appendEmpty(IntVector *self);
bool IntVector_pop(IntVector *self, int *elem);
void IntVector_clear(IntVector *self);
bool IntVector_get(IntVector *self, size_t index, int *elem);
bool IntVector_set(IntVector *self, size_t index, int elem);
