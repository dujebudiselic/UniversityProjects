#include "myfactory.h"
#include <stdio.h>
#include <stdlib.h>
#include "animal.h"

int main(int argc, char *argv[]) {
    for (int i = 0; i < argc / 2; ++i) {
        struct Animal* p = (struct Animal*)myfactory(argv[1 + 2 * i], argv[1 + 2 * i + 1]);
        if (!p) {
            printf("Creation of plug-in object %s failed.\n", argv[1 + 2 * i]);
            continue;
        }

        animalPrintGreeting(p);
        animalPrintMenu(p);
        //free(p);
    }
}
