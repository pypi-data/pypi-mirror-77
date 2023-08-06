#pragma once

#include <stddef.h>
#include <stdbool.h>


struct IntTree_Node;


typedef struct IntTree_Node
{
	bool red;
	struct IntTree_Node *links[2];

	int key;
	int value;
}
IntTree_Node;


typedef struct IntTree
{
	IntTree_Node *root;
	size_t size;
}
IntTree;


void IntTree_init(IntTree *self);
void IntTree_dealloc(IntTree *self);
bool IntTree_validate(IntTree *self);

bool IntTree_insert(IntTree *self, int key, int value);
bool IntTree_delete(IntTree *self, int key);
bool IntTree_get(IntTree *self, int key, int *value);
void IntTree_clear(IntTree *self);


typedef struct IntTree_Iterator
{
	IntTree *map;
	IntTree_Node *node;

	IntTree_Node *path[16 * sizeof(size_t)];
	size_t top;
}
IntTree_Iterator;


bool IntTree_Iterator_init(IntTree_Iterator *self, IntTree *map, bool atLeft);
void IntTree_Iterator_dealloc(IntTree_Iterator *self);

bool IntTree_Iterator_move(IntTree_Iterator *self, bool toRight);
void IntTree_Iterator_item(IntTree_Iterator *self, int *key, int *value);
