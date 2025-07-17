#include <stdio.h>
#include <string.h>

const void* mymax(const void *base, size_t nmemb, size_t size, int (*compar)(const void *, const void *)) {

    const char *basec = (const char *)base;  
    const void *max = basec;           

    for (int i = 1; i < nmemb; ++i) {
        const void *current = basec + i * size; 
        if (compar(current, max)) {
            max = current; 
        }
    }

    return max;
}

int gt_int(const void *arg1, const void *arg2) {
    int a = *(const int*)arg1;
    int b = *(const int*)arg2;
    if (a > b) {
        return 1;
    }
    return 0;
}

int gt_char(const void *arg1, const void *arg2) {
    char a = *(const char*)arg1;
    char b = *(const char*)arg2;
    if (a > b) {
        return 1;
    }
    return 0;
}

int gt_str(const void *arg1, const void *arg2) {
    const char *a = *(const char **)arg1;
    const char *b = *(const char **)arg2;
    if (strcmp(a, b) > 0){
        return 1;
    }
    return 0;
}

int main() {
    int arr_int[] = { 1, 3, 5, 7, 4, 6, 9, 2, 0 };
    char arr_char[] = "Suncana strana ulice";
    const char* arr_str[] = {"Gle", "malu", "vocku", "poslije", "kise", "Puna", "je", "kapi", "pa", "ih", "njise"};

    const int *maxint = mymax(arr_int, sizeof(arr_int) / sizeof(arr_int[0]), sizeof(arr_int[0]), gt_int);
    printf("%d\n", *maxint);

    const char *maxchar = mymax(arr_char, sizeof(arr_char) - 1, sizeof(arr_char[0]), gt_char);
    printf("%c\n", *maxchar);

    const char * const *maxstr = mymax(arr_str, sizeof(arr_str) / sizeof(arr_str[0]), sizeof(arr_str[0]), gt_str); 
    printf("%s\n", *maxstr);

    return 0;
}

