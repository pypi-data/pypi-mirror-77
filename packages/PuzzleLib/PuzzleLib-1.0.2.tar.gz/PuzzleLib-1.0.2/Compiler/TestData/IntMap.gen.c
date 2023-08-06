#include <stdlib.h>
#include "IntMap.gen.h"


inline static size_t hashKey(int key) { return key; }
inline static bool compareKeys(int key1, int key2) { return key1 == key2; }



void IntMap_init(IntMap *self)
{
	self->size = 0;
	self->log2capacity = 4;

	self->ptr = (IntMap_Bucket **)malloc(sizeof(self->ptr[0]) * (1ULL << self->log2capacity));

	for (size_t i = 0; i < (1ULL << self->log2capacity); i += 1)
		self->ptr[i] = NULL;
}


void IntMap_dealloc(IntMap *self)
{
	IntMap_clear(self);
	free(self->ptr);
}


void IntMap_clear(IntMap *self)
{
	for (size_t i = 0; i < (1ULL << self->log2capacity); i += 1)
	{
		IntMap_Bucket *bucket = self->ptr[i];
		self->ptr[i] = NULL;

		while (bucket != NULL)
		{
			IntMap_Bucket *next = bucket->next;

			(void)(bucket->key);
			(void)(bucket->value);

			free(bucket);
			bucket = next;
		}
	}
}


static void IntMap_rehash(IntMap *self)
{
	size_t log2capacity = self->log2capacity + 1;
	IntMap_Bucket **ptr = (IntMap_Bucket **)malloc(sizeof(self->ptr[0]) * (1ULL << log2capacity));

	for (size_t i = 0; i < (1ULL << log2capacity); i += 1)
		ptr[i] = NULL;

	for (size_t i = 0; i < (1ULL << self->log2capacity); i += 1)
	{
		IntMap_Bucket *bucket = self->ptr[i];

		while (bucket != NULL)
		{
			size_t hash = hashKey(bucket->key) & ((1 << log2capacity) - 1);
			IntMap_Bucket **insert = &ptr[hash];

			while (*insert != NULL)
				insert = &(*insert)->next;

			*insert = bucket;

			IntMap_Bucket *next = bucket->next;
			bucket->next = NULL;

			bucket = next;
		}
	}

	free(self->ptr);
	self->ptr = ptr;

	self->log2capacity = log2capacity;
}


bool IntMap_insert(IntMap *self, int key, int value)
{
	size_t hash = hashKey(key) & ((1 << self->log2capacity) - 1);

	IntMap_Bucket **ptr = &self->ptr[hash];
	IntMap_Bucket *bucket = self->ptr[hash];

	while (bucket != NULL)
	{
		if (compareKeys(bucket->key, key))
		{
			bucket->value = value;
			return false;
		}

		ptr = &bucket->next;
		bucket = bucket->next;
	}

	IntMap_Bucket *node = (IntMap_Bucket *)malloc(sizeof(*node));
	node->next = NULL;

	node->key = (int)(key);
	node->value = (int)(value);

	*ptr = node;

	self->size += 1;
	float n = (float)self->size / (1 << self->log2capacity);

	if (n >= 0.75f)
		IntMap_rehash(self);

	return true;
}


bool IntMap_delete(IntMap *self, int key)
{
	size_t hash = hashKey(key) & ((1 << self->log2capacity) - 1);

	IntMap_Bucket **ptr = &self->ptr[hash];
	IntMap_Bucket *bucket = self->ptr[hash];

	while (bucket != NULL)
	{
		if (compareKeys(bucket->key, key))
		{
			*ptr = bucket->next;

			(void)(bucket->key);
			(void)(bucket->value);

			free(bucket);

			self->size -= 1;
			return true;
		}

		ptr = &bucket->next;
		bucket = bucket->next;
	}

	return false;
}


bool IntMap_get(IntMap *self, int key, int *value)
{
	size_t hash = hashKey(key) & ((1 << self->log2capacity) - 1);
	IntMap_Bucket *bucket = self->ptr[hash];

	while (bucket != NULL)
	{
		if (compareKeys(bucket->key, key))
		{
			*value = bucket->value;
			return true;
		}

		bucket = bucket->next;
	}

	return false;
}
