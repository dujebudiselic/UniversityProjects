#include <stdlib.h>
#include <string.h>

typedef char const* (*PTRFUN)();

struct Tiger {
    PTRFUN* vtable;
    char const* name;
};

char const* tigerName(void* this) {
    return ((struct Tiger*)this)->name;
}

char const* tigerGreet() {
    return "Mijau!";
}

char const* tigerMenu() {
    return "mlako mlijeko";
}

PTRFUN tigervtable[3] = {tigerName, tigerGreet, tigerMenu};

int size() {
    return sizeof(struct Tiger);
}

void construct(void* memorija, char const* name) {
    struct Tiger* tiger = (struct Tiger*)memorija;
    tiger->name = name;
    tiger->vtable = tigervtable;
}

void* create(char const* name) {
    void* mem = malloc(sizeof(struct Tiger));
    construct(mem, name);
    return mem;
}
