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
    dataset = ['63\n1, 5, 10, 25', '255\n1, 6, 12, 20, 34, 22, 63, 5, 7', '666666\n1, 5, 7, 9, 19, 1, 17, 20, 21, 56, 112']
    return dataset





def coin_change(dataset):
    data = dataset.split('\n')
    amount = int(data[0])
    coins = list(map(int, data[1].split(', ')))
    coins.sort(reverse=True)
    result = []
    for coin in coins:
        while amount >= coin:
            amount -= coin
            result.append(coin)
    return len(result)

tests = generate()
len_tests = len(tests)
incorrect_count = 0
correct_count = 0
COUNT_OPEN_TESTS = 3
try:
    for test in tests:
        stud_output = subprocess.check_output(exec_command, input=test, universal_newlines=True)
        expected_output = coin_change(test)
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
