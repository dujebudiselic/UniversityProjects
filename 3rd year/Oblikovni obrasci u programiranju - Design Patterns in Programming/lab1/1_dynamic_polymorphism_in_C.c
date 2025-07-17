#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef char const* (*PTRFUN)();

struct Animal {
    char* name;
    PTRFUN* vtable;
};

char const* dogGreet(void){
    return "vau!";
}
char const* dogMenu(void){
    return "kuhanu govedinu";
}
char const* catGreet(void){
    return "mijau!";
}
char const* catMenu(void){
    return "konzerviranu tunjevinu";
}

PTRFUN dogvtable[2] = { dogGreet, dogMenu };
PTRFUN catvtable[2] = { catGreet, catMenu };

void animalPrintGreeting(struct Animal* animal) {
    printf("%s pozdravlja: %s\n", animal->name, animal->vtable[0]());
}

void animalPrintMenu(struct Animal* animal) {
    printf("%s voli %s\n", animal->name, animal->vtable[1]());
}

void constructDog(struct Animal* animal, char* name) {
    animal->name = name;
    animal->vtable = dogvtable;
}

void constructCat(struct Animal* animal, char* name) {
    animal->name = name;
    animal->vtable = catvtable;
}

struct Animal* createDog(char* name) {
    struct Animal* dog = malloc(sizeof(struct Animal));
    constructDog(dog, name);
    return dog;
}

struct Animal* createCat(char* name) {
    struct Animal* cat = malloc(sizeof(struct Animal));
    constructCat(cat, name);
    return cat;
}

struct Animal* createnDogs(int n, char** names) {
    struct Animal* dogs = malloc(n * sizeof(struct Animal));
    for (int i = 0; i < n; ++i)
        constructDog(&dogs[i], names[i]);
    return dogs;
}

void testAnimals(void) {

    struct Animal* p1=createDog("Hamlet");
    struct Animal* p2=createCat("Ofelija");
    struct Animal* p3=createDog("Polonije");

    animalPrintGreeting(p1);
    animalPrintGreeting(p2);
    animalPrintGreeting(p3);

    animalPrintMenu(p1);
    animalPrintMenu(p2);
    animalPrintMenu(p3);

    printf("\n");

    struct Animal p4;
    constructCat(&p4, "Garfield");
    animalPrintGreeting(&p4);
    animalPrintMenu(&p4);

    printf("\n");

    char* huski[] = { "Luna", "Blue", "Zeus", "Storm"};
    int n = 4;
    struct Animal* huskiekipa = createnDogs(n, huski);
    for (int i = 0; i < n; ++i) {
        animalPrintGreeting(&huskiekipa[i]);
        animalPrintMenu(&huskiekipa[i]);
    }

    free(p1); free(p2); free(p3);
    free(huskiekipa);
}


int main() {
    testAnimals();
    return 0;
}

// objekt -> struct animal (dog, cat)
// metode -> animalPrintMenu, animalPrintGreeting
// virtualne metode -> dogGreet, dogMenu, catGreet, catMenu
// konstruktori -> constructDog, constructCat
// virtualne tablice -> dogvtable, catvtable
