#include <iostream>
#include <assert.h>
#include <stdlib.h>
using namespace std;

struct Point {
  int x; int y;
};

struct Shape {
  enum EType { circle, square, rhomb };
  EType type_;
};

struct Circle {
  Shape::EType type_;
  double radius_;
  Point center_;
};

struct Square {
  Shape::EType type_;
  double side_;
  Point center_;
};

struct Rhomb {
  Shape::EType type_;
  double side_;
  Point center_;
};

void drawSquare(struct Square*) {
  std::cerr << "in drawSquare\n";
}

void drawCircle(struct Circle*) {
  std::cerr << "in drawCircle\n";
}

void drawRhomb(struct Rhomb*) {
  std::cerr << "in drawRhomb\n";
}

void drawShapes(Shape** shapes, int n) {
  for (int i = 0; i < n; ++i) {
    struct Shape* s = shapes[i];
    switch (s->type_) {
      case Shape::square:
        drawSquare((struct Square*)s);
        break;
      case Shape::circle:
        drawCircle((struct Circle*)s);
        break;
      case Shape::rhomb:
        drawRhomb((struct Rhomb*)s);
        break;
      default:
        assert(0);
        exit(0);
    }
  }
}

void moveShapes(Shape** shapes, int n, int translation_x, int translation_y) {
  for (int i = 0; i < n; ++i) {
    struct Shape* s = shapes[i];
    switch (s->type_) {
      case Shape::square: {
        struct Square* sq = (struct Square*)s;
        cout << sq->center_.x << ',' << sq->center_.y << '\n';
        sq->center_.x = sq->center_.x + translation_x;
        sq->center_.y = sq->center_.y + translation_y;
        cout << sq->center_.x << ',' << sq->center_.y << '\n';
        break;
      }
      case Shape::circle: {
        struct Circle* c = (struct Circle*)s;
        cout << c->center_.x << ',' << c->center_.y << '\n';
        c->center_.x = c->center_.x + translation_x;
        c->center_.y = c->center_.y + translation_y;
        cout << c->center_.x << ',' << c->center_.y << '\n';
        break;
      }
      default:
        assert(0);
        exit(0);
    }
  }
}


int main() {
  Shape* shapes[5];

  Circle* circle1 = new Circle;
  circle1->type_ = Shape::circle;
  circle1->radius_ = 5;
  circle1->center_ = {0, 0};
  shapes[0] = (Shape*)circle1;
  Square* square1 = new Square;
  square1->type_ = Shape::square;
  square1->side_ = 5;
  square1->center_ = {0, 0}; 
  shapes[1] = (Shape*)square1;
  Square* square2 = new Square;
  square2->type_ = Shape::square;
  square2->side_ = 5;
  square2->center_ = {0, 0};
  shapes[2] = (Shape*)square2;
  Circle* circle2 = new Circle;
  circle2->type_ = Shape::circle;
  circle2->radius_ = 5;
  circle2->center_ = {0, 0};
  shapes[3] = (Shape*)circle2;
  Rhomb* rhomb1 = new Rhomb;
  rhomb1->type_ = Shape::rhomb;
  rhomb1->side_ = 5;
  rhomb1->center_ = {4, 4};
  shapes[4] = (Shape*)rhomb1;

  drawShapes(shapes, 5);
  moveShapes(shapes, 5, 10, -5); 

  return 0;
}
