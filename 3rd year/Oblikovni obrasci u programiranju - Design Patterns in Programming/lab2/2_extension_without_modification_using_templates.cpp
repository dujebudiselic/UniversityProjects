#include <iostream>
#include <vector>
#include <set>
using namespace std;

template <typename Iterator, typename Predicate>
Iterator mymax(Iterator first, Iterator last, Predicate pred) {

    if (first == last) {
        return last;
    }

    Iterator max = first;  

    while (first!=last) {

        if (pred(*first, *max)) {
            max = first;  
        }
        ++first;
    }

    return max;
}

bool gt_int(int arg1, int arg2) {
    if (arg1 > arg2) {
        return true;
    }
    return false;
}

bool gt_char(char arg1, char arg2) {
    if (arg1 > arg2) {
        return true;
    }
    return false;
}

bool gt_str(const string& arg1, const string& arg2) {
    if (arg1 > arg2) {
        return true;
    }
    return false; 
}

int main() {
    int arr_int[] = { 1, 3, 5, 7, 4, 6, 9, 2, 0 };
    char arr_char[] = "Suncana strana ulice";
    const char* arr_str[] = {"Gle", "malu", "vocku", "poslije", "kise", "Puna", "je", "kapi", "pa", "ih", "njise"};

    const int* maxint = mymax(&arr_int[0], &arr_int[sizeof(arr_int)/sizeof(*arr_int)], gt_int); 
    cout << *maxint << "\n";

    const char *maxchar = mymax(&arr_char[0], &arr_char[sizeof(arr_char)/sizeof(*arr_char)], gt_char);
    cout << *maxchar << "\n";

    const char * const *maxstr = mymax(&arr_str[0], &arr_str[sizeof(arr_str)/sizeof(*arr_str)], gt_str);
    cout << *maxstr << "\n";

    vector<int> vec_int = {1, 3, 5, 7, 4, 6, 9, 2, 0};
    auto maxvecint = mymax(vec_int.begin(), vec_int.end(), gt_int);
    cout << *maxvecint << "\n";

    set<int> set_int = {1, 3, 5, 7, 4, 6, 9, 2, 0};
    auto maxsetint = mymax(set_int.begin(), set_int.end(), gt_int);
    cout << *maxsetint << "\n";

    int arr_prazno[] = {};
    const int* maxprazno = mymax(arr_prazno, arr_prazno, gt_int); 
    if (maxprazno == arr_prazno) {
        cout << "Prazno\n";
    }
    return 0;
}

// Prednosti ove implementacije:
// - radi s bilo kojim iteratorom
// - ne treba se kao parametar primat veličina elementa
// - ne treba se računati di treba pokazivat pokazivač da se dobije vrijednost idućeg elementa
// Nedostaci implementacije:
// - generira se zasebna instanca funkcije ako npr. promjenimo iterator ili predicate
