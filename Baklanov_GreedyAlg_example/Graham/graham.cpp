#include <iostream>
#include <vector>
#include <algorithm>
#include <sstream>
#include <cmath>
#include <iomanip>


using namespace std;

struct Point {
    int x, y;
};

int rotate(const Point& A, const Point& B, const Point& C) {
    return (B.x - A.x) * (C.y - B.y) - (B.y - A.y) * (C.x - B.x);
}

double polygon_area(const vector<Point>& vertices) {
    int n = vertices.size();
    double area = 0.0;
    for (int i = 0; i < n; ++i) {
        int j = (i + 1) % n;
        area += vertices[i].x * vertices[j].y;
        area -= vertices[j].x * vertices[i].y;
    }
    area = abs(area) / 2.0;
    return area;
}

vector<Point> grahamscan(vector<Point>& A) {
    int n = A.size();
    vector<int> P(n);
    for (int i = 0; i < n; ++i) {
        P[i] = i;
    }

    for (int i = 1; i < n; ++i) {
        if (A[P[i]].x < A[P[0]].x) {
            swap(P[i], P[0]);
        }
    }

    for (int i = 2; i < n; ++i) {
        int j = i;
        while (j > 1 && rotate(A[P[0]], A[P[j - 1]], A[P[j]]) < 0) {
            swap(P[j], P[j - 1]);
            j--;
        }
    }

    vector<int> S = {P[0], P[1]};
    for (int i = 2; i < n; ++i) {
        while (rotate(A[S[S.size() - 2]], A[S.back()], A[P[i]]) < 0) {
            S.pop_back();
        }
        S.push_back(P[i]);
    }

    vector<Point> res;
    for (int i : S) {
        res.push_back(A[i]);
    }
    return res;
}

int main() {
    int n;
    cin >> n;
    cin.ignore(); // Ignore the newline after the integer input
    vector<Point> points(n);
    for (int i = 0; i < n; ++i) {
        string input;
        getline(cin, input);
        stringstream ss(input);
        char comma; // To consume the comma
        ss >> points[i].x >> comma >> points[i].y;
    }

    vector<Point> g = grahamscan(points);
    double area = polygon_area(g);

    cout << "([";
    for (size_t i = 0; i < g.size(); ++i) {
        cout << "[" << g[i].x << ", " << g[i].y << "]";
        if (i < g.size() - 1) {
            cout << ", ";
        }
    }
    cout << "], " << fixed << setprecision(1) << area << ")" << endl;

    return 0;
}
