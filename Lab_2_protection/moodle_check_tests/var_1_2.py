import subprocess, sys, re


def generate():
    # Список своих тестов
    return ["4\nBrave_New_World 1932\nWuthering_Heights 1847\nThe_Great_Gatsby 1925\nThe_Catcher_in_the_Rye 1951\n",
            "4\nBook_C 1950\nBook_A 1950\nBook_B 1950\nBook_D 1950\n",
            "4\nSame_Title 1960\nSame_Title 1970\nSame_Title 1950\nSame_Title 1980\n",
            "4\nBook_One 2000\nBook_Two 1999\nBook_Three 2000\nBook_Four 1998\n",
            "4\nBook_One 2000\nBook_Two 1999\nBook_Three 2000\nBook_Four 1998\n"]


def check(reply, clue):
    # Функция проверки идентичности строк (строка-ответ пользователя и корректная строка-ответ)
    return str(reply).strip() == str(clue).strip()


def solve(dataset):
    # Исходный список книг
    info = dataset.split('\n')[1:len(dataset) - 1]
    info = [el.split() for el in info][:-1]
    books = [tuple([el[0], int(el[1])]) for el in info]
    answ = ''

    # Сортировка списка книг
    sorted_books = sorted(books, key=lambda book: (book[1], book[0]))

    # Вывод результата
    for title, year in sorted_books:
        answ = answ + f"{title} {year}" + '\n'

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

