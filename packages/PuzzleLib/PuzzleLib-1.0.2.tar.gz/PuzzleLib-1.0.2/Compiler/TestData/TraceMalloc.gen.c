#undef NDEBUG
#include <assert.h>

#include "AllocTree.gen.h"
#include "TraceMalloc.gen.h"


static AllocTree allocTree;
static AllocTree_Iterator allocIterator;


void *TraceMalloc_malloc(size_t size, const char *file, int line)
{
	void *ptr = malloc(size);

	Allocation alloc;
	alloc.size = size;
	alloc.file = file;
	alloc.line = line;

	bool inserted = AllocTree_insert(&allocTree, ptr, alloc);
	assert(inserted);

	return ptr;
}


void TraceMalloc_free(void *ptr)
{
	if (ptr != NULL)
	{
		Allocation alloc;

		bool found = AllocTree_get(&allocTree, ptr, &alloc);
		assert(found);

		bool deleted = AllocTree_delete(&allocTree, ptr);
		assert(deleted);
	}

	free(ptr);
}


size_t TraceMalloc_traceLeaks(void)
{
	return allocTree.size;
}


bool TraceMalloc_Iterator_init(void)
{
	return AllocTree_Iterator_init(&allocIterator, &allocTree, true);
}


void TraceMalloc_Iterator_dealloc(void)
{
	AllocTree_Iterator_dealloc(&allocIterator);
}


bool TraceMalloc_Iterator_move(void)
{
	return AllocTree_Iterator_move(&allocIterator, true);
}


void TraceMalloc_Iterator_item(size_t *size, const char **file, int *line)
{
	void *ptr;
	Allocation alloc;

	AllocTree_Iterator_item(&allocIterator, &ptr, &alloc);

	*size = alloc.size;
	*file = alloc.file;
	*line = alloc.line;
}
