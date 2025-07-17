#include <stdlib.h>
#include <string.h>

typedef char const* (*PTRFUN)();

struct Parrot {
    PTRFUN* vtable;
    char const* name;
};

char const* parrotName(void* this) {
    return ((struct Parrot*)this)->name;
}

char const* parrotGreet(void) {
    return "Sto mu gromova!";
}

char const* parrotMenu(void) {
    return "brazilske orahe";
}

PTRFUN parrotvtable[3] = {parrotName, parrotGreet, parrotMenu};

int size() {
    return sizeof(struct Parrot);
}

void construct(void* memorija, char const* name) {
    struct Parrot* parrot = (struct Parrot*)memorija;
    parrot->name = name;
    parrot->vtable = parrotvtable;
}

void* create(char const* name) {
    void* mem = malloc(sizeof(struct Parrot));
    construct(mem, name);
    return mem;
}
