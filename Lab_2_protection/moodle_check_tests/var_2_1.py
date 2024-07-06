import subprocess, sys, re


def generate():
    # Список своих тестов
    '''
        * Обычный (+)
        * Одинаковый средний балл студентов одной группы (+)
        * Одинаковый средний балл в массиве всех студентов (в разных группах по человеку) (+)
        * По одному ученику с одинаковыми баллом и номером (+)
    '''
    return ["4\n1 3\n4 4\n4 5\n2 4\n2\n5 5\n7 4\n", "4\n3 4\n5 4\n6 5\n4 3\n4\n2 5\n2 2\n8 2\n8 1\n",
            "4\n3 4\n5 4\n6 5\n4 3\n4\n2 4\n2 4\n8 5\n8 3\n", "1\n4 5\n1\n4 5\n"]


def check(reply, clue):
    # Функция проверки идентичности строк (строка-ответ пользователя и корректная строка-ответ)
    return str(reply).strip() == str(clue).strip()


def solve(dataset):
    def calculate_average_grades(grades):
        # Средний балл для каждого ученика.

        from collections import defaultdict
        students = defaultdict(list)

        for student_id, grade in grades:
            students[student_id].append(grade)

        # Рассчитываем средний балл для каждого ученика
        average_grades = {student: sum(grades) / len(grades) for student, grades in students.items()}
        return average_grades

    parse = dataset.split('\n')
    answ = ''

    n = int(parse.pop(0))
    grades_11A = [tuple(map(int, parse.pop(0).split())) for _ in range(n)]

    m = int(parse.pop(0))
    grades_11B = [tuple(map(int, parse.pop(0).split())) for _ in range(m)]

    # Вычисление среднего балла для каждого ученика в 11А и 11Б
    average_grades_11A = calculate_average_grades(grades_11A)
    average_grades_11B = calculate_average_grades(grades_11B)

    # Сортировка учеников по убыванию среднего балла
    sorted_11A = sorted(average_grades_11A.items(), key=lambda x: (x[1], x[0]), reverse=True)
    sorted_11B = sorted(average_grades_11B.items(), key=lambda x: (x[1], x[0]), reverse=True)

    # Вывод номеров учеников 11А в порядке убывания среднего балла
    answ += " ".join(str(student_id) for student_id, _ in sorted_11A) + '\n'

    # Вывод номеров учеников 11Б в порядке убывания среднего балла
    answ += " ".join(str(student_id) for student_id, _ in sorted_11B) + '\n'

    # Объединение списков и сортировка по возрастанию среднего балла
    all_students = list(average_grades_11A.items()) + list(average_grades_11B.items())
    sorted_all_students = sorted(all_students, key=lambda x: (x[1], x[0]))

    # Вывод общего списка учеников
    answ += " ".join(str(student_id) for student_id, _ in sorted_all_students) + '\n'

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

