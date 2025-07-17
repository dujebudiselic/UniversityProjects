#include <iostream>
using namespace std;

struct Point {
    int x, y;
};

struct Shape {
    virtual void drawShape() = 0;  
    virtual void moveShape(int translation_x, int translation_y) = 0;  
    virtual ~Shape() = default; 
};

struct Circle : public Shape {
    double radius_;
    Point center_;

    Circle(double radius = 5, int x = 0, int y = 0)
        : radius_(radius), center_{x, y} {}

    void drawShape() override {
        std::cerr << "in drawCircle\n";
    }

    void moveShape(int translation_x , int translation_y) override {
        cout << center_.x << ',' << center_.y << '\n';
        center_.x = center_.x + translation_x ;
        center_.y = center_.y + translation_x ;
        cout << center_.x << ',' << center_.y << '\n';
    }
};

struct Square : public Shape {
    double side_;
    Point center_;

    Square(double side = 5, int x = 0, int y = 0)
        : side_(side), center_{x, y} {}

    void drawShape() override {
        std::cerr << "in drawSquare\n";
    }

    void moveShape(int translation_x, int translation_y) override {
        cout << center_.x << ',' << center_.y << '\n';
        center_.x = center_.x + translation_x;
        center_.y = center_.y + translation_y;
        cout << center_.x << ',' << center_.y << '\n';
    }
};

struct Rhomb : public Shape {
    double side_;
    Point center_;

    Rhomb(double side = 5, int x = 0, int y = 0)
        : side_(side), center_{x, y} {}

    void drawShape() override {
        std::cerr << "in drawRhomb\n";
    }

    void moveShape(int translation_x, int translation_y) override {
        cout << center_.x << ',' << center_.y << '\n';
        center_.x = center_.x + translation_x;
        center_.y = center_.y + translation_y;
        cout << center_.x << ',' << center_.y << '\n';
    }
};

void drawShapes(Shape* shapes[], int n) {
    for (int i = 0; i < n; ++i) {
        shapes[i]->drawShape();
    }
}

void moveShapes(Shape* shapes[], int n, int translation_x, int translation_y) {
    for (int i = 0; i < n; ++i) {
        shapes[i]->moveShape(translation_x, translation_y);
    }
}

int main() {
    Shape* shapes[5];
    shapes[0] = new Circle;
    shapes[1] = new Square;
    shapes[2] = new Square;
    shapes[3] = new Circle;
    shapes[4] = new Rhomb;

    drawShapes(shapes, 5);
    moveShapes(shapes, 5, 10, -5);

    return 0;
}

// Svojstva:
// - open-closed principle
// - ne koristi se switch nego virtualna tablica 