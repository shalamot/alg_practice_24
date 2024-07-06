import subprocess, sys, re


def generate():
    # Список своих тестов
    return ["3\n4 2 3\n34 86 75 90\n98 54\n84 68 70\n", "3\n4 4 4\n70 70 70 70\n56 37 49 54\n84 68 70 24\n",
            "4\n4 2 3 1\n70 70 70 70\n70 70\n70 70 70\n70\n", "5\n1 1 3 1 1\n78\n35\n78 82 74\n90\n43\n"]


def check(reply, clue):
    # Функция проверки идентичности строк (строка-ответ пользователя и корректная строка-ответ)
    return str(reply).strip() == str(clue).strip()


def solve(dataset):
    data = dataset.split('\n')
    needed_data = data[2:len(data) - 1]
    all_classes = [list(map(int, needed_data[i].split())) for i in range(len(needed_data))]
    answ = ''

    all_stud_mas = []
    for i in range(len(all_classes)):
        all_classes[i].sort()
        all_stud_mas.extend(all_classes[i])

    all_classes.sort(key=lambda x: (sum(x) / len(x), -len(x)))
    for el in all_classes:
        answ = answ + ' '.join(list(map(str, el))) + '\n'

    answ += ' '.join(list(map(str, sorted(all_stud_mas))))

    return answ


student_answer = """{{ STUDENT_ANSWER | e('py') }}"""
language = """{{ ANSWER_LANGUAGE | e('py') }}""".lower()
language_extension_map = {'cpp': 'cpp', 'python3': 'py'}

if language not in language_extension_map.keys():
    raise Exception('Error in question. Unknown/unexpected language ({})'.format(language))

filename = '__tester__.' + language_extension_map[language]

# Write the student code to a file

with open(filename, "w") as src:
    print(student_answer, file=src)

# Compile C++
if language == 'cpp':
    return_code = subprocess.call("g++ -o __tester__ __tester__.cpp".split())
    if return_code != 0:
        raise Exception("** Compilation failed. Testing aborted **")
    exec_command = ["./__tester__"]

else:  # Python doesn't need a compile phase
    exec_command = ["python3", "./__tester__.py"]

tests = generate()  # Генерация тестов
len_tests = len(tests)
incorrect_count = 0
correct_count = 0
COUNT_OPEN_TESTS = 1

try:
    for test in tests:  # Пробегаемся по нашим тестам
        # Запускаем программу пользователя с нашим тестом
        output = subprocess.check_output(exec_command, input=test, universal_newlines=True)
        correct_output = solve(test)  # Получаем верный ответ из нашей программы
        if not check(output, correct_output):  # Сравнение ответов
            incorrect_count += 1
            if incorrect_count < COUNT_OPEN_TESTS:
                result = 'Test: {}\n'.format(test)
                result += 'Your answer: {}\n'.format(output)
                result += 'Correct: {}\n'.format(correct_output)
                print(result)
        else:
            correct_count += 1
except subprocess.CalledProcessError as e:
    if e.returncode > 0:
        # Ignore non-zero positive return codes
        if e.output:
            print(e.output)
    else:
        # But negative return codes are signals - abort
        if e.output:
            print(e.output, file=sys.stderr)
        if e.returncode < 0:
            print("Task failed with signal", -e.returncode, file=sys.stderr)
        print("** Further testing aborted **", file=sys.stderr)
if correct_count == len(tests):
    print('OK')
else:
    print('Wrong answer')

