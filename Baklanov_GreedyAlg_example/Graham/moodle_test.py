"""The template for a "write a program" question type that accepts answers
    in C, C++, Java or Python3 according to the value in the language select
    dropdown menu.
"""
from functools import cmp_to_key
import random
import subprocess
import re
student_answer = """{{ STUDENT_ANSWER | e('py') }}"""
language = """{{ ANSWER_LANGUAGE | e('py') }}""".lower()
language_extension_map = {'cpp':'cpp', 'python3':'py'}

if re.search(r'^\s*(import|from)\s+\w+', student_answer, re.MULTILINE):
    raise Exception('Imports are not allowed in the student answer.')

if language not in language_extension_map.keys():
    raise Exception('Error in question. Unknown/unexpected language ({})'.format(language))

filename = '__tester__.' + language_extension_map[language]

# Write the student code to a file

with open(filename, "w") as src:
    print(student_answer, file=src)

# C++, Python
if language == 'cpp':
    cppflags = "-Wall -Werror"
    return_code = subprocess.call("g++ {0} -o __tester__ __tester__.cpp".format(cppflags).split())
    if return_code != 0:
        raise Exception("** Compilation failed. Testing aborted **")
    exec_command = ["./__tester__"]
else: # Python doesn't need a compile phase
    exec_command = ["python3", "./__tester__.py"]

# Now run the code. Since this is a per-test template,
# stdin is already set up for the stdin text specified in the test case,
# so we can run the compiled program directly.

def check(reply, clue):
    return str(reply).strip() == str(clue).strip()

def generate():
    dataset = ['6\n3, 1\n6, 8\n1, 7\n9, 3\n9, 6\n9, 0', '49\n7, 1\n4, 2\n8, 10\n2, 6\n5, 3\n9, 6\n9, 9\n9, 5\n4, 7\n9, 4\n9, 2\n9, 9\n4, 4\n8, 3\n8, 10\n3, 9\n8, 1\n5, 2\n10, 2\n7, 4\n10, 1\n5, 2\n7, 3\n6, 4\n5, 10\n6, 1\n4, 5\n5, 5\n8, 8\n2, 3\n10, 10\n2, 10\n9, 5\n2, 9\n3, 4\n6, 8\n1, 8\n5, 3\n3, 10\n9, 9\n2, 10\n3, 3\n1, 1\n6, 4\n1, 7\n7, 8\n7, 1\n4, 5\n10, 7', '88\n81, 48\n73, 70\n5, 32\n73, 91\n18, 57\n52, 37\n62, 33\n33, 35\n99, 29\n59, 54\n55, 92\n46, 37\n78, 65\n75, 44\n15, 10\n18, 93\n60, 56\n69, 52\n36, 34\n10, 46\n95, 27\n65, 39\n6, 87\n51, 85\n70, 15\n11, 37\n100, 96\n48, 62\n96, 1\n68, 30\n7, 27\n8, 34\n38, 24\n55, 73\n21, 13\n55, 44\n5, 85\n66, 32\n72, 8\n54, 42\n41, 4\n70, 95\n76, 93\n63, 76\n9, 12\n82, 28\n23, 29\n81, 29\n6, 5\n6, 84\n58, 100\n11, 87\n23, 70\n20, 2\n49, 99\n7, 73\n76, 56\n5, 31\n2, 92\n53, 66\n27, 15\n62, 99\n57, 89\n46, 29\n62, 32\n98, 2\n11, 12\n49, 19\n40, 35\n39, 41\n5, 9\n10, 74\n91, 94\n36, 76\n2, 34\n32, 6\n2, 55\n64, 28\n17, 95\n74, 68\n38, 23\n42, 10\n10, 96\n78, 0\n67, 56\n3, 50\n3, 92\n10, 75'
]
    return dataset


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
  n = len(A)
  P = [i for i in range(n)] 
  for i in range(1,n):
    if A[P[i]][0]<A[P[0]][0]: 
      P[i], P[0] = P[0], P[i]
  for i in range(2,n): 
    j = i
    while j>1 and (rotate(A[P[0]],A[P[j-1]],A[P[j]])<0):
      P[j], P[j-1] = P[j-1], P[j]
      j -= 1
  S = [P[0],P[1]]
  for i in range(2,n):
    while rotate(A[S[-2]],A[S[-1]],A[P[i]])<0:
      del S[-1] 
    S.append(P[i])
  res = []
  for i in S:
    res.append(A[i])
  return res

def result_func(dataset):
    data = dataset.split("\n")
    n = data[0]
    points = []
    for line in data[1:]:
        points.append(list(map(int, line.split(', '))))
    g = grahamscan(points)
    return g, polygon_area(g)

tests = generate()
len_tests = len(tests)
incorrect_count = 0
correct_count = 0
COUNT_OPEN_TESTS = 3
try:
    for test in tests:
        stud_output = subprocess.check_output(exec_command, input=test, universal_newlines=True)
        expected_output = result_func(test)
        if str(expected_output).strip() != stud_output.strip():
            incorrect_count += 1
            if incorrect_count < 3:
                print('Wrong answer')
        else:
            correct_count += 1
except subprocess.CalledProcessError as e:
    if e.returncode > 0:
        if e.output:
            print(e.output)
    else:
        if e.output:
            print(e.output, file=sys.stderr)
        if e.returncode < 0:
            print("Task failed with signal", -e.returncode, file=sys.stderr)
        print("** Further testing aborted **", file=sys.stderr)

if correct_count == len_tests:
    print('OK')
else:
    print('Failed')
