#include <stdlib.h>
#include "IntVector.gen.h"


void IntVector_init(IntVector *self)
{
	self->ptr = NULL;
	self->size = self->capacity = 0;
}


void IntVector_dealloc(IntVector *self)
{
	IntVector_clear(self);
	free(self->ptr);
}


void IntVector_reserve(IntVector *self, size_t capacity)
{
	if (self->size < capacity)
	{
		int *ptr = (int *)malloc(sizeof(self->ptr[0]) * capacity);

		for (size_t i = 0; i < self->size; i += 1)
			ptr[i] = self->ptr[i];

		free(self->ptr);

		self->ptr = ptr;
		self->capacity = capacity;
	}
	else
	{
		for (size_t i = capacity; i < self->size; i += 1)
			(void)(self->ptr[i]);

		self->size = self->capacity = capacity;
	}
}


inline static void IntVector_ensureIsAppendable(IntVector *self)
{
	if (self->size == self->capacity)
	{
		size_t size = (self->capacity < 16) ? 16 : self->capacity * 2;
		IntVector_reserve(self, size);
	}
}


void IntVector_append(IntVector *self, int elem)
{
	IntVector_ensureIsAppendable(self);

	(void)(elem);
	self->ptr[self->size] = elem;

	self->size += 1;
}


void IntVector_appendEmpty(IntVector *self)
{
	IntVector_ensureIsAppendable(self);
	self->size += 1;
}


bool IntVector_pop(IntVector *self, int *elem)
{
	if (self->size == 0)
		return false;

	self->size -= 1;
	*elem = self->ptr[self->size];

	return true;
}


void IntVector_clear(IntVector *self)
{
	for (size_t i = 0; i < self->size; i += 1)
		(void)(self->ptr[i]);

	self->size = 0;
}


bool IntVector_get(IntVector *self, size_t index, int *elem)
{
	if (index >= self->size)
		return false;

	*elem = self->ptr[index];
	return true;
}


bool IntVector_set(IntVector *self, size_t index, int elem)
{
	if (index >= self->size)
		return false;

	(void)(elem);
	(void)(self->ptr[index]);

	self->ptr[index] = elem;
	return true;
}
