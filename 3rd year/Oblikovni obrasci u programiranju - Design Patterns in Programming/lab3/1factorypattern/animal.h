#ifndef ANIMAL_H
#define ANIMAL_H

#ifdef __cplusplus
extern "C" {
#endif

struct Animal;

void animalPrintGreeting(struct Animal* animal);
void animalPrintMenu(struct Animal* animal);

#ifdef __cplusplus
}
#endif

#endif
