#include <iostream>
using namespace std;

class CoolClass{
  public:
    virtual void set(int x){x_=x;};
    virtual int get(){return x_;};
  private:
    int x_;
};

class PlainOldClass{
  public:
    void set(int x){x_=x;};
    int get(){return x_;};
  private:
    int x_;
};

int main() {
  cout << "sizeof(CoolClass) = " << sizeof(CoolClass) << endl;
  cout << "sizeof(PlainOldClass) = " << sizeof(PlainOldClass) << endl;
  //sizeof(CoolClass) = 8 ima jedan član koji zauzima 4 bajta, 
  //ali ima virtualne funkcije tako da se stvori pokazivač na virtualnu tablicu koji također zauzima 4 bajta.
  //sizeof(PlainOldClass) = 4 jedan član koji zauzima 4 bajta.
  return 0;
}