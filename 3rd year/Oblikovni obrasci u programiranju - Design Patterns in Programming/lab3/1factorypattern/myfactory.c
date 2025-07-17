#include "myfactory.h"
#include <stdio.h>
#include <stdlib.h>
#include <dlfcn.h>


void* myfactory(char const* libname, char const* ctorarg) {
    char file[1000];
    snprintf(file, sizeof(file), "./%s.so", libname);

    void* handle = dlopen(file, RTLD_LAZY);
    
    void* (*create)(char const*);
    int (*size)();
    void (*construct)(void*, char const*);

    *(void**)(&create)    = dlsym(handle, "create");
    *(void**)(&size)      = dlsym(handle, "size");
    *(void**)(&construct) = dlsym(handle, "construct");

    
    // alokacija na gomili
    //void* obj = create(ctorarg);
    //return obj;
    
    // alokacija na stogu
    int sz = size();
    void* mem = alloca(sz); 
    construct(mem, ctorarg);
    return mem;

}
