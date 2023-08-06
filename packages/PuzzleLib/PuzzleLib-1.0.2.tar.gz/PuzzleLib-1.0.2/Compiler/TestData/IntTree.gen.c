#include <stdlib.h>
#include "IntTree.gen.h"


inline static int IntTree_compareKeys(int lhs, int rhs)
{
	return (lhs > rhs) - (lhs < rhs);
}


inline static IntTree_Node *IntTree_createNode(int key, int value)
{
	IntTree_Node *node = (IntTree_Node *)malloc(sizeof(IntTree_Node));

	node->key = key;
	node->value = value;

	node->links[0] = node->links[1] = NULL;
	node->red = true;

	return node;
}


inline static void IntTree_releaseNode(IntTree_Node *node)
{
	free(node);
}


inline static bool IntTree_nodeIsRed(IntTree_Node *node)
{
	return (node != NULL) ? node->red : false;
}


inline static IntTree_Node *IntTree_rotate(IntTree_Node *node, size_t dir)
{
	IntTree_Node *upnode = node->links[!dir];

	node->links[!dir] = upnode->links[dir];
	upnode->links[dir] = node;

	upnode->red = false;
	node->red = true;

	return upnode;
}


inline static IntTree_Node *IntTree_rotate2(IntTree_Node *node, size_t dir)
{
	IntTree_Node *subnode = node->links[!dir];
	IntTree_Node *upnode = subnode->links[dir];

	subnode->links[dir] = upnode->links[!dir];
	upnode->links[!dir] = subnode;

	node->links[!dir] = upnode->links[dir];
	upnode->links[dir] = node;

	upnode->red = false;
	node->red = true;

	return upnode;
}


void IntTree_init(IntTree *self)
{
	self->root = NULL;
	self->size = 0;
}


void IntTree_dealloc(IntTree *self)
{
	IntTree_clear(self);
}


void IntTree_clear(IntTree *self)
{
	IntTree_Node *node = self->root;

	while (node != NULL)
	{
		IntTree_Node *save = NULL;

		if (node->links[0] != NULL)
		{
			save = node->links[0];
			node->links[0] = save->links[1];
			save->links[1] = node;
		}
		else
		{
			save = node->links[1];
			IntTree_releaseNode(node);
		}

		node = save;
	}

	self->size = 0;
	self->root = NULL;
}


inline static void IntTree_repairDoubleRed(IntTree_Node *node, IntTree_Node *parent, IntTree_Node *grand,
										   IntTree_Node *temp, size_t lastdir)
{
	size_t dir2 = (temp->links[1] == grand);
	bool aligned = (node == parent->links[lastdir]);

	temp->links[dir2] = aligned ? IntTree_rotate(grand, !lastdir) : IntTree_rotate2(grand, !lastdir);
}


bool IntTree_insert(IntTree *self, int key, int value)
{
	bool inserted = false;

	if (self->root != NULL)
	{
		IntTree_Node head;

		head.red = false;
		head.links[0] = NULL;
		head.links[1] = self->root;

		IntTree_Node *temp = &head;
		IntTree_Node *parent = NULL, *grand = NULL;
		IntTree_Node *node = self->root;

		size_t dir = 0, lastdir = 0;

		while (true)
		{
			if (node == NULL)
			{
				parent->links[dir] = node = IntTree_createNode(key, value);

				self->size += 1;
				inserted = true;
			}
			else if (IntTree_nodeIsRed(node->links[0]) && IntTree_nodeIsRed(node->links[1]))
			{
				node->red = true;
				node->links[0]->red = node->links[1]->red = false;
			}

			if (IntTree_nodeIsRed(node) && IntTree_nodeIsRed(parent))
				IntTree_repairDoubleRed(node, parent, grand, temp, lastdir);

			int cmp = IntTree_compareKeys(key, node->key);
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
		self->root = IntTree_createNode(key, value);

		self->size = 1;
		inserted = true;
	}

	self->root->red = false;
	return inserted;
}


inline static IntTree_Node *IntTree_repairDoubleBlack(IntTree_Node *node, IntTree_Node *parent, IntTree_Node *grand,
													  size_t dir, size_t lastdir)
{
	if (IntTree_nodeIsRed(node->links[!dir]))
	{
		parent = parent->links[lastdir] = IntTree_rotate(node, dir);
		return parent;
	}

	IntTree_Node *sibling = parent->links[!lastdir];

	if (sibling != NULL)
	{
		if (!IntTree_nodeIsRed(sibling->links[0]) && !IntTree_nodeIsRed(sibling->links[1]))
		{
			parent->red = false;
			node->red = sibling->red = true;
		}
		else
		{
			size_t dir2 = (grand->links[1] == parent);

			if (IntTree_nodeIsRed(sibling->links[lastdir]))
				grand->links[dir2] = IntTree_rotate2(parent, lastdir);

			else if (IntTree_nodeIsRed(sibling->links[!lastdir]))
				grand->links[dir2] = IntTree_rotate(parent, lastdir);

			node->red = grand->links[dir2]->red = true;
			grand->links[dir2]->links[0]->red = grand->links[dir2]->links[1]->red = false;
		}
	}

	return parent;
}


bool IntTree_delete(IntTree *self, int key)
{
	if (self->root == NULL)
		return false;

	bool deleted = false;
	IntTree_Node head;

	head.red = false;
	head.links[0] = NULL;
	head.links[1] = self->root;

	IntTree_Node *found = NULL;
	IntTree_Node *parent = NULL, *grand = NULL;
	IntTree_Node *node = &head;

	size_t dir = 1;

	do
	{
		size_t lastdir = dir;

		grand = parent, parent = node;
		node = node->links[dir];

		int cmp = IntTree_compareKeys(key, node->key);

		dir = cmp > 0;
		found = (cmp == 0) ? node : found;

		if (!IntTree_nodeIsRed(node) && !IntTree_nodeIsRed(node->links[dir]))
			parent = IntTree_repairDoubleBlack(node, parent, grand, dir, lastdir);
	}
	while (node->links[dir] != NULL);

	if (found != NULL)
	{
		found->key = node->key;
		found->value = node->value;

		parent->links[parent->links[1] == node] = node->links[node->links[0] == NULL];

		IntTree_releaseNode(node);

		self->size -= 1;
		deleted = true;
	}

	self->root = head.links[1];

	if (self->root != NULL)
		self->root->red = false;

	return deleted;
}


bool IntTree_get(IntTree *self, int key, int *value)
{
	IntTree_Node *node = self->root;

	while (node != NULL)
	{
		int cmp = IntTree_compareKeys(key, node->key);
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


inline static bool IntTree_Iterator_start(IntTree_Iterator *self, bool atLeft)
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


bool IntTree_Iterator_init(IntTree_Iterator *self, IntTree *map, bool atLeft)
{
	self->map = map;
	return IntTree_Iterator_start(self, atLeft);
}


void IntTree_Iterator_dealloc(IntTree_Iterator *self)
{
	(void)self;
}


bool IntTree_Iterator_move(IntTree_Iterator *self, bool toRight)
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
		IntTree_Node *lastnode = NULL;
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


void IntTree_Iterator_item(IntTree_Iterator *self, int *key, int *value)
{
	*key = self->node->key;
	*value = self->node->value;
}


static bool IntTree_validateNode(IntTree_Node *node, size_t *nblack)
{
	size_t subblack[2] = {0, 0};

	for (size_t i = 0; i < 2; i += 1)
	{
		IntTree_Node *subnode = node->links[i];
		if (subnode == NULL) continue;

		if (node->red && subnode->red)
			return false;

		if (!IntTree_validateNode(subnode, &subblack[i]))
			return false;
	}

	if (subblack[0] != subblack[1])
		return false;

	size_t totalblack = subblack[0];
	if (!node->red) totalblack += 1;

	*nblack += totalblack;
	return true;
}


bool IntTree_validate(IntTree *self)
{
	if (self->root == NULL)
		return true;

	size_t nblack = 0;
	return IntTree_validateNode(self->root, &nblack);
}
