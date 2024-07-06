import subprocess, sys, re
from datetime import datetime


def generate():
    # Список своих тестов
    '''
        * Обычный (+)
        * Одинаковые оценки, разные даты рождения (+)
        * Одинаковые оценки, одинаковые даты рождения (+)
        * Один человек (+)
        * Второй и третий случаи вместе (+)
    '''
    return ["4\nJake 14.4.2000 87\nMike 1.12.2004 90\nSamson 15.4.2001 84\nLucy 30.8.2004 78\n",
            "4\nJake 14.4.2000 87\nMike 1.12.2004 90\nSamson 15.4.2001 87\nLucy 30.8.2004 78\n",
            "4\nSamson 15.4.2001 87\nJake 15.4.2001 87\nMike 1.12.2004 90\nLucy 30.8.2004 78\n",
            "1\nJake 14.4.2000 87\n",
            "6\nSamson 15.4.2001 86\nJake 15.4.2001 87\nMike 1.12.2004 90\nLucy 30.8.2004 78\nAnn 15.4.2001 86\nBecky 30.12.2004 78\n"]


def check(reply, clue):
    # Функция проверки идентичности строк (строка-ответ пользователя и корректная строка-ответ)
    return str(reply).strip() == str(clue).strip()


def solve(dataset):
    # Функция для чтения и парсинга даты
    def parse_date(date_str):
        return datetime.strptime(date_str, '%d.%m.%Y')

    # Чтение данных
    info = dataset.split('\n')
    info.pop()

    n = int(info.pop(0))
    students = []
    for _ in range(n):
        data = info.pop(0).split()
        name = data[0]
        birth_date = parse_date(data[1])
        grade = int(data[2])
        students.append((name, birth_date, grade))

    # Сортировка студентов
    sorted_students = sorted(students, key=lambda x: (x[2], -x[1].timestamp(), x[0]))

    # Вывод имен студентов
    result = " ".join(student[0] for student in sorted_students)
    return result


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