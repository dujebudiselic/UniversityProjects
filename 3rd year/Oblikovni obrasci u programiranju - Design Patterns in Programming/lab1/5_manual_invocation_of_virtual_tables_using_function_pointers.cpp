#include <iostream>
using namespace std;

class B {
public:
    virtual int __cdecl prva() = 0;
    virtual int __cdecl druga(int) = 0;
};

class D : public B {
public:
    virtual int __cdecl prva() { return 42; }
    virtual int __cdecl druga(int x) { return prva() + x; }
};

typedef int(__cdecl *PTRFUN1)(B*);
typedef int(__cdecl *PTRFUN2)(B*, int);

void rucnoprozivanjevirtualnetablice(B* pb){
    
    void** vtable = *(void***)pb;

    PTRFUN1 pfun1 = (PTRFUN1)vtable[0];
    PTRFUN2 pfun2 = (PTRFUN2)vtable[1];

    cout << "Poziv prva(): " << pfun1(pb) << endl;
    cout << "Poziv druga(5): " << pfun2(pb, 11) << endl;

}

int main() {
    D d;
    rucnoprozivanjevirtualnetablice(&d);
    return 0;
}
