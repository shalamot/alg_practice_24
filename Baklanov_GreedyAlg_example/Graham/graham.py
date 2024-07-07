def rotate(A,B,C):
  return (B[0]-A[0])*(C[1]-B[1])-(B[1]-A[1])*(C[0]-B[0])

def polygon_area(vertices):
  n = len(vertices)
  area = 0.0
  for i in range(n):
    j = (i + 1) % n
    area += vertices[i][0] * vertices[j][1]
    area -= vertices[j][0] * vertices[i][1]
  area = abs(area) / 2.0
  return area
def grahamscan(A):
  n = len(A) # число точек
  P = [i for i in range(n)] # список номеров точек
  for i in range(1,n):
    if A[P[i]][0]<A[P[0]][0]: # если P[i]-ая точка лежит левее P[0]-ой точки
      P[i], P[0] = P[0], P[i] # меняем местами номера этих точек
  for i in range(2,n): # сортировка вставкой
    j = i
    while j>1 and (rotate(A[P[0]],A[P[j-1]],A[P[j]])<0):
      P[j], P[j-1] = P[j-1], P[j]
      j -= 1
  S = [P[0],P[1]] # создаем стек
  for i in range(2,n):
    while rotate(A[S[-2]],A[S[-1]],A[P[i]])<0:
      del S[-1] # pop(S)
    S.append(P[i])
  res = []
  for i in S:
    res.append(A[i])
  return res

if __name__ == "__main__":
  n = int(input())
  points = []
  for i in range(n):
    points.append(list(map(int, input().split(', '))))
  g = grahamscan(points)
  print((g, polygon_area(g)))