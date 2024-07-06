from functools import cmp_to_key
class Point:
    def __init__(self, x=None, y=None):
        self.x = x
        self.y = y
p0 = Point(0, 0)

def polygon_area(vertices):
    n = len(vertices)
    area = 0.0
    for i in range(n):
        j = (i + 1) % n
        area += vertices[i].x * vertices[j].y
        area -= vertices[j].x * vertices[i].y
    area = abs(area) / 2.0
    return area
def nextToTop(S):
    return S[-2]
def distSq(p1, p2):
    return ((p1.x - p2.x) * (p1.x - p2.x) +
            (p1.y - p2.y) * (p1.y - p2.y))
def orientation(p, q, r):
    val = ((q.y - p.y) * (r.x - q.x) -
           (q.x - p.x) * (r.y - q.y))
    if val == 0:
        return 0
    elif val > 0:
        return 1
    else:
        return 2
def compare(p1, p2):
    # Find orientation
    o = orientation(p0, p1, p2)
    if o == 0:
        if distSq(p0, p2) >= distSq(p0, p1):
            return -1
        else:
            return 1
    else:
        if o == 2:
            return -1
        else:
            return 1
def convexHull(points, n):
    ymin = points[0].y
    min = 0
    for i in range(1, n):
        y = points[i].y
        if ((y < ymin) or
                (ymin == y and points[i].x < points[min].x)):
            ymin = points[i].y
            min = i
    points[0], points[min] = points[min], points[0]
    p0 = points[0]
    points = sorted(points, key=cmp_to_key(compare))
    m = 1
    for i in range(1, n):
        while ((i < n - 1) and
               (orientation(p0, points[i], points[i + 1]) == 0)):
            i += 1
        points[m] = points[i]
        m += 1
    if m < 3:
        return
    S = []
    S.append(points[0])
    S.append(points[1])
    S.append(points[2])
    for i in range(3, m):
        while ((len(S) > 1) and
               (orientation(nextToTop(S), S[-1], points[i]) != 2)):
            S.pop()
        S.append(points[i])

    hull_vert = list(S)
    area = polygon_area(hull_vert)
    result = []
    while S:
        p = S[-1]
        result.append((p.x, p.y))
        S.pop()
    return result, area

n = int(input())
points = []
for i in range(n):
    inp = input().split(', ')
    points.append(Point(int(inp[0]), int(inp[1])))
result, area = convexHull(points, n)
print((result, area))
