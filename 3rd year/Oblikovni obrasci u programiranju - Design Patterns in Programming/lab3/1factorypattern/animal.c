#include <stdio.h>
#include "animal.h"

typedef char const* (*PTRFUN)();

struct Animal {
  PTRFUN* vtable;
};

void animalPrintGreeting(struct Animal* animal) {
  printf("%s pozdravlja: %s\n", animal->vtable[0](animal), animal->vtable[1]());
}

void animalPrintMenu(struct Animal* animal) {
  printf("%s voli %s\n", animal->vtable[0](animal), animal->vtable[2]());
}
