import subprocess, sys, re


# Тут предлагаю написание Родительского класса и двух его наследников, в которых будут реализованы методы
# для работы с парсингом кода: ИНТЕРФЕЙС, словом
def methods(user_code_file):
    return ''


# Функция для проверки корректного завершения всех тестов (py / cpp)
def run_tests(lang, exec_comm):

    if lang is 'py':
        res = subprocess.run(["pytest", exec_comm[1][2:]], capture_output=True, text=True)
    else:
        res = subprocess.run([exec_comm], capture_output=True, text=True)

    return res


# Эту часть кода пока не трогаем (она нам даёт код в текстовом формате и понимание, с каким языком работаем)
'''
student_answer = """{{ STUDENT_ANSWER | e('py') }}"""
language = """{{ ANSWER_LANGUAGE | e('py') }}""".lower()
language_extension_map = {'cpp': 'cpp', 'python3': 'py'}
print(student_answer, language)

if language not in language_extension_map.keys():
    raise Exception('Error in question. Unknown/unexpected language ({})'.format(language))
'''
language_extension_map = {'cpp': 'cpp', 'python3': 'py'}  #
language = 'py'  #
filename = '__tester__.' + language_extension_map[language]

'''
with open(filename, "w") as src:
    print(student_answer, file=src)
'''

# Компиляция остаётся для того, чтобы выявлять ошибки в самой программе пользователя (не относится к заданиям)

# Compile C++
if language == 'cpp':
    return_code = subprocess.call("g++ -o __tester__ __tester__.cpp".split())
    if return_code != 0:
        raise Exception("** Compilation failed. Testing aborted **")
    exec_command = ["./__tester__"]

else:  # Python doesn't need a compile phase
    exec_command = ["python3", "./__tester__.py"]


# В генерации тестов отпадает необходимость, т.к. мы будем парсить сам код.

correct_count = 0

# В ходе переделки изменения внесены лишь в try модуль, не трогая except модуль.

try:
    # Запускаем программу пользователя для проверки тестов
    output = run_tests(language_extension_map[language], exec_command)
    if not output.returncode == 0:
        raise Exception("** Error: mistake in user tests **")

    # Здесь будет объект с вызовом метода класса, который пропарсит код и вернёт некий ответ (True / False)
    correctness = methods(filename)

    if not correctness:  # Если не все тесты проверены студентом, то сохраняем прежний вывод с небольшим упрощением
        result = 'Test: {}\n'.format('1')
        result += 'Your answer: {}\n'.format('Incorrect set of tests.')
        result += 'Correct: {}\n'.format('Correct set of tests.')
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
if correct_count == 1:
    print('OK')
else:
    print('Wrong answer')
