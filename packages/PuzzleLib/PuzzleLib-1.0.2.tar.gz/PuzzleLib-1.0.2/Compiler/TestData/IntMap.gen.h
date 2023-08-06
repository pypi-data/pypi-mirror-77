#pragma once

#include <stddef.h>
#include <stdbool.h>


struct IntMap_Bucket;


typedef struct IntMap_Bucket
{
	int key;
	int value;

	struct IntMap_Bucket *next;
}
IntMap_Bucket;


typedef struct IntMap
{
	IntMap_Bucket **ptr;
	size_t size, log2capacity;
}
IntMap;


void IntMap_init(IntMap *self);
void IntMap_dealloc(IntMap *self);

bool IntMap_insert(IntMap *self, int key, int value);
bool IntMap_delete(IntMap *self, int key);
bool IntMap_get(IntMap *self, int key, int *value);
void IntMap_clear(IntMap *self);
