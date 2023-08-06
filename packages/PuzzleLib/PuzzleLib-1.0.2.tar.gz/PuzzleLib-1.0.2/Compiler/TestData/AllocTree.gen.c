#include <stdlib.h>
#include "AllocTree.gen.h"


inline static int AllocTree_compareKeys(VoidPtr lhs, VoidPtr rhs)
{
	return (lhs > rhs) - (lhs < rhs);
}


inline static AllocTree_Node *AllocTree_createNode(VoidPtr key, Allocation value)
{
	AllocTree_Node *node = (AllocTree_Node *)malloc(sizeof(AllocTree_Node));

	node->key = key;
	node->value = value;

	node->links[0] = node->links[1] = NULL;
	node->red = true;

	return node;
}


inline static void AllocTree_releaseNode(AllocTree_Node *node)
{
	free(node);
}


inline static bool AllocTree_nodeIsRed(AllocTree_Node *node)
{
	return (node != NULL) ? node->red : false;
}


inline static AllocTree_Node *AllocTree_rotate(AllocTree_Node *node, size_t dir)
{
	AllocTree_Node *upnode = node->links[!dir];

	node->links[!dir] = upnode->links[dir];
	upnode->links[dir] = node;

	upnode->red = false;
	node->red = true;

	return upnode;
}


inline static AllocTree_Node *AllocTree_rotate2(AllocTree_Node *node, size_t dir)
{
	AllocTree_Node *subnode = node->links[!dir];
	AllocTree_Node *upnode = subnode->links[dir];

	subnode->links[dir] = upnode->links[!dir];
	upnode->links[!dir] = subnode;

	node->links[!dir] = upnode->links[dir];
	upnode->links[dir] = node;

	upnode->red = false;
	node->red = true;

	return upnode;
}


void AllocTree_init(AllocTree *self)
{
	self->root = NULL;
	self->size = 0;
}


void AllocTree_dealloc(AllocTree *self)
{
	AllocTree_clear(self);
}


void AllocTree_clear(AllocTree *self)
{
	AllocTree_Node *node = self->root;

	while (node != NULL)
	{
		AllocTree_Node *save = NULL;

		if (node->links[0] != NULL)
		{
			save = node->links[0];
			node->links[0] = save->links[1];
			save->links[1] = node;
		}
		else
		{
			save = node->links[1];
			AllocTree_releaseNode(node);
		}

		node = save;
	}

	self->size = 0;
	self->root = NULL;
}


inline static void AllocTree_repairDoubleRed(AllocTree_Node *node, AllocTree_Node *parent, AllocTree_Node *grand,
										   AllocTree_Node *temp, size_t lastdir)
{
	size_t dir2 = (temp->links[1] == grand);
	bool aligned = (node == parent->links[lastdir]);

	temp->links[dir2] = aligned ? AllocTree_rotate(grand, !lastdir) : AllocTree_rotate2(grand, !lastdir);
}


bool AllocTree_insert(AllocTree *self, VoidPtr key, Allocation value)
{
	bool inserted = false;

	if (self->root != NULL)
	{
		AllocTree_Node head;

		head.red = false;
		head.links[0] = NULL;
		head.links[1] = self->root;

		AllocTree_Node *temp = &head;
		AllocTree_Node *parent = NULL, *grand = NULL;
		AllocTree_Node *node = self->root;

		size_t dir = 0, lastdir = 0;

		while (true)
		{
			if (node == NULL)
			{
				parent->links[dir] = node = AllocTree_createNode(key, value);

				self->size += 1;
				inserted = true;
			}
			else if (AllocTree_nodeIsRed(node->links[0]) && AllocTree_nodeIsRed(node->links[1]))
			{
				node->red = true;
				node->links[0]->red = node->links[1]->red = false;
			}

			if (AllocTree_nodeIsRed(node) && AllocTree_nodeIsRed(parent))
				AllocTree_repairDoubleRed(node, parent, grand, temp, lastdir);

			int cmp = AllocTree_compareKeys(key, node->key);
			if (cmp == 0)
				break;

			lastdir = dir;
			dir = cmp > 0;

			temp = (grand != NULL) ? grand : temp;

			grand = parent, parent = node;
			node = node->links[dir];
		}

		self->root = head.links[1];
	}
	else
	{
		self->root = AllocTree_createNode(key, value);

		self->size = 1;
		inserted = true;
	}

	self->root->red = false;
	return inserted;
}


inline static AllocTree_Node *AllocTree_repairDoubleBlack(AllocTree_Node *node, AllocTree_Node *parent, AllocTree_Node *grand,
													  size_t dir, size_t lastdir)
{
	if (AllocTree_nodeIsRed(node->links[!dir]))
	{
		parent = parent->links[lastdir] = AllocTree_rotate(node, dir);
		return parent;
	}

	AllocTree_Node *sibling = parent->links[!lastdir];

	if (sibling != NULL)
	{
		if (!AllocTree_nodeIsRed(sibling->links[0]) && !AllocTree_nodeIsRed(sibling->links[1]))
		{
			parent->red = false;
			node->red = sibling->red = true;
		}
		else
		{
			size_t dir2 = (grand->links[1] == parent);

			if (AllocTree_nodeIsRed(sibling->links[lastdir]))
				grand->links[dir2] = AllocTree_rotate2(parent, lastdir);

			else if (AllocTree_nodeIsRed(sibling->links[!lastdir]))
				grand->links[dir2] = AllocTree_rotate(parent, lastdir);

			node->red = grand->links[dir2]->red = true;
			grand->links[dir2]->links[0]->red = grand->links[dir2]->links[1]->red = false;
		}
	}

	return parent;
}


bool AllocTree_delete(AllocTree *self, VoidPtr key)
{
	if (self->root == NULL)
		return false;

	bool deleted = false;
	AllocTree_Node head;

	head.red = false;
	head.links[0] = NULL;
	head.links[1] = self->root;

	AllocTree_Node *found = NULL;
	AllocTree_Node *parent = NULL, *grand = NULL;
	AllocTree_Node *node = &head;

	size_t dir = 1;

	do
	{
		size_t lastdir = dir;

		grand = parent, parent = node;
		node = node->links[dir];

		int cmp = AllocTree_compareKeys(key, node->key);

		dir = cmp > 0;
		found = (cmp == 0) ? node : found;

		if (!AllocTree_nodeIsRed(node) && !AllocTree_nodeIsRed(node->links[dir]))
			parent = AllocTree_repairDoubleBlack(node, parent, grand, dir, lastdir);
	}
	while (node->links[dir] != NULL);

	if (found != NULL)
	{
		found->key = node->key;
		found->value = node->value;

		parent->links[parent->links[1] == node] = node->links[node->links[0] == NULL];

		AllocTree_releaseNode(node);

		self->size -= 1;
		deleted = true;
	}

	self->root = head.links[1];

	if (self->root != NULL)
		self->root->red = false;

	return deleted;
}


bool AllocTree_get(AllocTree *self, VoidPtr key, Allocation *value)
{
	AllocTree_Node *node = self->root;

	while (node != NULL)
	{
		int cmp = AllocTree_compareKeys(key, node->key);
		if (cmp == 0)
		{
			*value = node->value;
			return true;
		}
		else
			node = node->links[cmp > 0];
	}

	return false;
}


inline static bool AllocTree_Iterator_start(AllocTree_Iterator *self, bool atLeft)
{
	size_t dir = atLeft ? 0 : 1;

	self->node = self->map->root;
	self->top = 0;

	if (self->node == NULL)
		return false;

	while (self->node->links[dir] != NULL)
	{
		self->path[self->top] = self->node;
		self->top += 1;

		self->node = self->node->links[dir];
	}

	return true;
}


bool AllocTree_Iterator_init(AllocTree_Iterator *self, AllocTree *map, bool atLeft)
{
	self->map = map;
	return AllocTree_Iterator_start(self, atLeft);
}


void AllocTree_Iterator_dealloc(AllocTree_Iterator *self)
{
	(void)self;
}


bool AllocTree_Iterator_move(AllocTree_Iterator *self, bool toRight)
{
	size_t dir = toRight ? 1 : 0;

	if (self->node->links[dir] != NULL)
	{
		self->path[self->top] = self->node;
		self->top += 1;

		self->node = self->node->links[dir];

		while (self->node->links[!dir] != NULL)
		{
			self->path[self->top] = self->node;
			self->top += 1;

			self->node = self->node->links[!dir];
		}
	}
	else
	{
		AllocTree_Node *lastnode = NULL;
		do
		{
			if (self->top == 0)
			{
				self->node = NULL;
				break;
			}

			lastnode = self->node;

			self->top -= 1;
			self->node = self->path[self->top];
		}
		while (lastnode == self->node->links[dir]);
	}

	return self->node != NULL;
}


void AllocTree_Iterator_item(AllocTree_Iterator *self, VoidPtr *key, Allocation *value)
{
	*key = self->node->key;
	*value = self->node->value;
}


static bool AllocTree_validateNode(AllocTree_Node *node, size_t *nblack)
{
	size_t subblack[2] = {0, 0};

	for (size_t i = 0; i < 2; i += 1)
	{
		AllocTree_Node *subnode = node->links[i];
		if (subnode == NULL) continue;

		if (node->red && subnode->red)
			return false;

		if (!AllocTree_validateNode(subnode, &subblack[i]))
			return false;
	}

	if (subblack[0] != subblack[1])
		return false;

	size_t totalblack = subblack[0];
	if (!node->red) totalblack += 1;

	*nblack += totalblack;
	return true;
}


bool AllocTree_validate(AllocTree *self)
{
	if (self->root == NULL)
		return true;

	size_t nblack = 0;
	return AllocTree_validateNode(self->root, &nblack);
}
