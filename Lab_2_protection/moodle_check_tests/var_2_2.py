import subprocess, sys, re


def generate():
    # Список своих тестов
    '''
        * Обычный (+)
        * Если два проекта имеют одинаковый средний приоритет (+)
        * Если два проекта имеют одинаковый средний приоритет и суммарную длительность (+).
        * Одиночный проект (+)
    '''
    return ["5\nA 3 45\nA 4 14\nB 2 67\nB 8 11\nA 10 22\n", "6\nA 5 100\nA 5 23\nA 5 16\nB 4 45\nB 6 69\nB 5 23\n",
            "18\nS 5 100\nS 5 23\nS 5 16\nB 4 45\nB 6 69\nB 5 23\nA 5 100\nA 5 23\nA 5 16\nN 4 45\nN 6 69\nN 5 23\nG 5 100\nG 5 23\nG 5 16\nK 4 45\nK 6 69\nK 5 23\n",
            "1\nA 3 45\n"]


def check(reply, clue):
    # Функция проверки идентичности строк (строка-ответ пользователя и корректная строка-ответ)
    return str(reply).strip() == str(clue).strip()


def solve(dataset):
    info = dataset.split('\n')
    info.pop()

    n = int(info.pop(0))
    tasks = [info.pop(0).split() for _ in range(n)]

    # Обработка задач, группировка по проектам
    projects = {}
    for task in tasks:
        project_name, priority, duration = task[0], int(task[1]), int(task[2])
        if project_name not in projects:
            projects[project_name] = {'priorities': [], 'total_duration': 0}
        projects[project_name]['priorities'].append(priority)
        projects[project_name]['total_duration'] += duration

    # Вычисление среднего приоритета и суммарной длительности
    project_stats = []
    for project, data in projects.items():
        average_priority = sum(data['priorities']) / len(data['priorities'])
        total_duration = data['total_duration']
        project_stats.append((project, average_priority, total_duration))

    # Сортировка проектов
    sorted_projects = sorted(
        project_stats,
        key=lambda x: (x[1], x[2], x[0])
    )

    # Вывод названий проектов
    answ = ''.join(project[0] for project in sorted_projects)
    return answ


student_answer = """{{ STUDENT_ANSWER | e('py') }}"""
language = """{{ ANSWER_LANGUAGE | e('py') }}""".lower()
language_extension_map = {'cpp': 'cpp', 'python3': 'py'}

if language not in language_extension_map.keys():
    raise Exception('Error in question. Unknown/unexpected language ({})'.format(language))

filename = '__tester__.' + language_extension_map[language]

if any(s in student_answer for s in ['sort(', 'stable_sort', 'sorted', 'qsort', 'sort (', 'sort(  ']):
    raise Exception("** Пользоваться библиотечными функциями сортировки запрещено **")

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

