#ifndef MYFACTORY_H
#define MYFACTORY_H

#ifdef __cplusplus
extern "C" {
#endif

void* myfactory(char const* libname, char const* ctorarg);

#ifdef __cplusplus
}
#endif

#endif
