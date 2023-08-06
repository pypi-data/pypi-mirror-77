#pragma once

#include <stddef.h>
#include <stdbool.h>


typedef void *VoidPtr;


typedef struct Allocation
{
	size_t size;
	const char *file;
	int line;
}
Allocation;



struct AllocTree_Node;


typedef struct AllocTree_Node
{
	bool red;
	struct AllocTree_Node *links[2];

	VoidPtr key;
	Allocation value;
}
AllocTree_Node;


typedef struct AllocTree
{
	AllocTree_Node *root;
	size_t size;
}
AllocTree;


void AllocTree_init(AllocTree *self);
void AllocTree_dealloc(AllocTree *self);
bool AllocTree_validate(AllocTree *self);

bool AllocTree_insert(AllocTree *self, VoidPtr key, Allocation value);
bool AllocTree_delete(AllocTree *self, VoidPtr key);
bool AllocTree_get(AllocTree *self, VoidPtr key, Allocation *value);
void AllocTree_clear(AllocTree *self);


typedef struct AllocTree_Iterator
{
	AllocTree *map;
	AllocTree_Node *node;

	AllocTree_Node *path[16 * sizeof(size_t)];
	size_t top;
}
AllocTree_Iterator;


bool AllocTree_Iterator_init(AllocTree_Iterator *self, AllocTree *map, bool atLeft);
void AllocTree_Iterator_dealloc(AllocTree_Iterator *self);

bool AllocTree_Iterator_move(AllocTree_Iterator *self, bool toRight);
void AllocTree_Iterator_item(AllocTree_Iterator *self, VoidPtr *key, Allocation *value);
