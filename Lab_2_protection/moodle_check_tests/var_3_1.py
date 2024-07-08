import subprocess, sys, re


def generate():
    # Список своих тестов
    '''
        * Обычный (+)
        * Одинаковые классы в одном флоте по отдельности (+)
        * Одинаковые классы в двух флотах (+)
        * Один корабль в каждом флоту (+)
    '''
    return ["3\n1034 2 213\n1043 2 206\n2067 4 1407\n4\n709 5 2600\n904 4 1389\n1067 2 220\n1455 3 856\n",
            "5\n1034 2 213\n1043 2 206\n1049 2 207\n1036 2 201\n2067 3 877\n5\n709 5 2623\n711 5 2600\n904 4 1389\n1067 6 12367\n1455 3 856\n",
            "5\n1034 2 213\n1043 2 206\n1049 2 207\n1036 2 201\n2067 3 877\n5\n103 2 212\n104 2 208\n109 2 209\n106 2 210\n221 3 944\n",
            "1\n1034 2 213\n1\n103 2 212\n"]


def check(reply, clue):
    # Функция проверки идентичности строк (строка-ответ пользователя и корректная строка-ответ)
    return str(reply).strip() == str(clue).strip()


def solve(dataset):
    # Функция для сортировки
    def sort_key(ship):
        return (ship[1], ship[2])

    def read_fleet(num_ships):
        fleet = []
        for _ in range(num_ships):
            ship_id, ship_class, firepower = map(int, info.pop(0).split())
            fleet.append((ship_id, ship_class, firepower))
        return fleet

    info = dataset.split('\n')
    info.pop()
    answ = ''

    # Чтение данных для флота Роя
    n = int(info.pop(0))
    roy_fleet = read_fleet(n)

    # Чтение данных для флота Унатари
    m = int(info.pop(0))
    unatari_fleet = read_fleet(m)

    # Сортировка флота Роя
    sorted_roy_fleet = sorted(roy_fleet, key=sort_key)

    # Сортировка объединённого флота
    combined_fleet = sorted(roy_fleet + unatari_fleet, key=sort_key)

    # Вывод идентификаторов флота Роя
    roy_ids = " ".join(str(ship[0]) for ship in sorted_roy_fleet)
    answ += roy_ids + '\n'

    # Вывод идентификаторов объединённого флота
    combined_ids = " ".join(str(ship[0]) for ship in combined_fleet)
    answ += combined_ids + '\n'

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

