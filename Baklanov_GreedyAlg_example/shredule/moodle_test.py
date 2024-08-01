"""The template for a "write a program" question type that accepts answers
    in C, C++, Java or Python3 according to the value in the language select
    dropdown menu.
"""
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
    dataset = ['7\n8, 11\n12, 14\n8, 13\n13, 15\n15, 17\n15, 16\n16, 17', '15\n11, 13\n12, 13\n14, 16\n16, 17\n10, 16\n14, 15\n17, 20\n8, 20\n1, 12\n9, 12\n8, 10\n10, 12\n13, 15\n15, 16\n16, 17', '50\n11, 13\n12, 13\n14, 16\n16, 17\n10, 16\n14, 15\n17, 20\n8, 20\n1, 12\n9, 12\n8, 10\n10, 12\n13, 15\n15, 16\n16, 17\n8, 9\n9, 11\n10, 11\n11, 12\n12, 14\n13, 14\n14, 15\n15, 17\n8, 11\n9, 10\n10, 14\n11, 15\n12, 16\n13, 17\n8, 12\n9, 13\n10, 15\n11, 16\n12, 17\n8, 13\n9, 14\n10, 16\n11, 17\n8, 14\n9, 15\n10, 17\n8, 15\n9, 16\n8, 16\n9, 17\n8, 17\n10, 13\n11, 14\n12, 15\n13, 16'
]
    return dataset





def shredule(dataset):
    lines = dataset.split('\n')
    counts = int(lines[0])
    tasks = []
    for line in lines[1:]:
        tasks.append(list(map(int, line.split(', '))))
    sorted_tasks = sorted(tasks, key=lambda x: x[1])
    res = []
    begin = 8
    end = 17
    for task in sorted_tasks:
        if (task[1] > end) or (task[0] >= end):
            continue
        if task[0] >= begin:
            res.append(task)
            begin = task[1]
    return res, len(res)

tests = generate()
len_tests = len(tests)
incorrect_count = 0
correct_count = 0
COUNT_OPEN_TESTS = 3
try:
    for test in tests:
        stud_output = subprocess.check_output(exec_command, input=test, universal_newlines=True)
        expected_output_1, expected_output_2 = shredule(test)
        expected_output = str(expected_output_1) + ' ' + str(expected_output_2)
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
