#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>

struct Unary_Function {
    struct Unary_Function_vtable* vtable;
    int lower_bound;
    int upper_bound;
};

struct Unary_Function_vtable {
    double (*value_at)(struct Unary_Function*, double);
    double (*negative_value_at)(struct Unary_Function*, double);
};

double negative_value_at(struct Unary_Function* unary_function, double x) {
    return -unary_function->vtable->value_at(unary_function, x);
}

void tabulate(struct Unary_Function* unary_function) {
    for (int x = unary_function->lower_bound; x <= unary_function->upper_bound; x++) {
        printf("f(%d)=%lf\n", x, unary_function->vtable->value_at(unary_function, x));
    }
}

bool same_functions_for_ints(struct Unary_Function* f1, struct Unary_Function* f2, double tolerance) {
    if (f1->lower_bound != f2->lower_bound) return false;
    if (f1->upper_bound != f2->upper_bound) return false;
    for (int x = f1->lower_bound; x <= f1->upper_bound; x++) {
        double delta = f1->vtable->value_at(f1, x) - f2->vtable->value_at(f2, x);
        if (delta < 0) delta = -delta;
        if (delta > tolerance) return false;
    }
    return true;
}

struct Square{
    struct Unary_Function Unary_Function;
};

double Square_value_at(struct Unary_Function* unary_function, double x) {
    return x * x;
}

struct Unary_Function_vtable squarevtable = {
    .value_at = Square_value_at,
    .negative_value_at = negative_value_at
};

void constructSquare(struct Square* square, int lower_bound, int upper_bound) {
    square->Unary_Function.vtable = &squarevtable;
    square->Unary_Function.lower_bound = lower_bound;
    square->Unary_Function.upper_bound = upper_bound;
}

struct Linear{
    struct Unary_Function Unary_Function;
    double a;
    double b;
};

double Linear_value_at(struct Unary_Function* Unary_Function, double x) {
    struct Linear* Linear = (struct Linear*)Unary_Function;
    return Linear->a * x + Linear->b;
}

struct Unary_Function_vtable linearvtable = {
    .value_at = Linear_value_at,
    .negative_value_at = negative_value_at
};

void constructLinear(struct Linear* linear, int lower_bound, int upper_bound, double a, double b) {
    linear->Unary_Function.vtable = &linearvtable;
    linear->Unary_Function.lower_bound = lower_bound;
    linear->Unary_Function.upper_bound = upper_bound;
    linear->a = a;
    linear->b = b;
}

struct Square* createSquare(int lower_bound, int upper_bound) {
    struct Square* square = malloc(sizeof(struct Square));
    constructSquare(square, lower_bound, upper_bound);
    return square;
}

struct Linear* createLinear(int lower_bound, int upper_bound, double a, double b) {
    struct Linear* linear = malloc(sizeof(struct Linear));
    constructLinear(linear, lower_bound, upper_bound, a, b);
    return linear;
}


int main() {
    struct Square* s = createSquare(-2, 2);
    struct Unary_Function* f1 = (struct Unary_Function*)s;
    tabulate(f1);

    struct Linear l;
    constructLinear(&l, -2, 2, 5, -2);
    struct Unary_Function* f2 = (struct Unary_Function*)&l;
    tabulate(f2);

    printf("f1==f2: %s\n", same_functions_for_ints(f1, f2, 1E-6) ? "DA" : "NE");
    printf("neg_val f2(1) = %lf\n", f2->vtable->negative_value_at(f2, 1.0));

    free(s);

    return 0;
}
