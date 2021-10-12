typedef struct {
  uint8_t *array;
  size_t used;
  size_t size;
} Array2;

void initArray2(Array2 *a, size_t initialSize) {
  a->array = (uint8_t *)malloc(initialSize * sizeof(uint8_t));
  a->used = 0;
  a->size = initialSize;
  for (int i=0; i<a->size;i++)
  a->array[i] = 0;
}

void insertArray2(Array2 *a, uint8_t element) {
  // a->used is the number of used entries, because a->array[a->used++] updates a->used only *after* the array has been accessed.
  // Therefore a->used can go up to a->size 
  if (a->used == a->size) {
    a->size *= 2;
    a->array = (uint8_t *)realloc(a->array, a->size * sizeof(uint8_t));
    for (int i=a->used; i<a->size; i++)
    a->array[i]=0;
  }
  a->array[a->used++] = element;
}

void freeArray2(Array2 *a) {
  free(a->array);
  a->array = NULL;
  a->used = a->size = 0;
}
