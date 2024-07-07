from abc import ABC, abstractmethod
import clang.cindex  # Импорт модуля clang для работы с AST
import ast
import pytest
import subprocess, sys, re

TRUE_TEST_AMOUNT = 5


def run_tests(lang, exec_comm):
    if lang == 'py':
        res = subprocess.run(["pytest", exec_comm[1][2:]], capture_output=True, text=True)
    else:
        res = subprocess.run(exec_comm, capture_output=True, text=True)

    return res


class TestParser(ABC):
    def __init__(self, filepath):
        self.filepath = filepath
        self.func_key = False
        self.test_cases = {
            "incorrect_day": False,
            "incorrect_month": False,
            "incorrect_year": False,
            "king_death": False,
            "leap_year": False,
        }

    @abstractmethod
    def analyze_tests(self):
        pass

    def fill_test_cases(self, date_str):
        if not re.match(r'^\d{1,2}\.\d{1,2}\.\d{4}$', date_str):
            return

        parts = date_str.split('.')

        try:
            day = int(parts[0])
            month = int(parts[1])
            year = int(parts[2])

            # Check day, month, year ranges
            if not (1 <= day <= 30):
                self.test_cases["incorrect_day"] = True
                return
            if not (1 <= month <= 12):
                self.test_cases["incorrect_month"] = True
                return
            if not (2001 <= year <= 2100):
                self.test_cases["incorrect_year"] = True
                return

            # Check for leap year
            if year % 4 == 0 and (year % 100 != 0 or year % 400 == 0):
                self.test_cases["leap_year"] = True
                return

            # Check for the specific date (13th July)
            if day == 13 and month == 7:
                self.test_cases["king_death"] = True
                return

        except ValueError:
            return


class PythonTestParser(TestParser):

    def walk_ast(self, node, depth=0):

        if isinstance(node, ast.Call):
            self.check_func(node)

        # Рекурсивно вызываем walk_ast для детей текущего узла
        for child in ast.iter_child_nodes(node):
            self.walk_ast(child, depth + 1)

    def check_func(self, sub_node):

        # Проверяем, является ли вызов функции вызовом функции 'foo'
        if isinstance(sub_node.func, ast.Name) and sub_node.func.id == "foo":

            # Проверяем, что в функцию передается один аргумент
            if len(sub_node.args) != 1:
                raise Exception("Функция foo должна принимать ровно один аргумент.")

            # Проверяем, что второй аргумент - это константа -- В AST может быть и строковой переменной

            _arg = sub_node.args[0]

            # Условия для присвоения значения переменной value, необходимой
            # для проставления наличия определённых типов проверок

            if isinstance(_arg, ast.Constant):
                value = _arg.value
            else:
                raise Exception("Аргумент функции foo должен быть строкой.")

            self.fill_test_cases(value)

    def analyze_tests(self):

        # Чтение и парсинг исходного кода тестового файла
        with open(self.filepath, "r") as file:
            tree = ast.parse(file.read())

        # Проход по узлам дерева AST
        for _node in ast.walk(tree):
            # Ищем функции, начинающиеся с 'test_'
            if isinstance(_node, ast.FunctionDef) and _node.name.startswith("test_"):
                # Проход по узлам внутри функции теста
                self.walk_ast(_node)

        return self.test_cases


class CTestParser(TestParser):

    def walk_ast(self, node, depth=0):

        # print("    " * depth + f"{node.kind.name} - {node.spelling}")  # ---- для демонстрации вложенности (ВАЖНО)

        # Проверяем, является ли узел вызовом функции foo
        # func_key нужен, чтобы проверить, что после вызова функции стоит строковая переменнаяя -- особенность структуры, иначе никак не проверить,
        # что стоит следующим значением. Если был вызов функции, мы делаем её True, а если она встретилась следующей по итерации
        if (node.kind == clang.cindex.CursorKind.CALL_EXPR or node.kind == clang.cindex.CursorKind.OVERLOADED_DECL_REF) and node.spelling == 'foo' or self.func_key:
            # Если это вызов функции foo, проверяем её аргументы
            if self.func_key:
                self.check_func(node)
            else:
                self.func_key = True
            '''
            # Возможная альтернатива
            if self.func_key:
                self.check_func(node)
            elif (node.kind == clang.cindex.CursorKind.CALL_EXPR or node.kind == clang.cindex.CursorKind.OVERLOADED_DECL_REF) and node.spelling == 'foo':
                self.func_key = True
            else:
                self.func_key = False
            '''

        # Рекурсивно вызываем walk_ast для детей текущего узла
        for child in node.get_children():
            self.walk_ast(child, depth + 1)

    def check_func(self, node):

        if node.kind not in [clang.cindex.CursorKind.STRING_LITERAL]:
            raise Exception("Аргумент функции foo должен быть строкой.")
        else:

            # Получаем строковую переменную
            value = list(node.get_tokens())[0].spelling
            self.func_key = False
            
            # Убираем скобки по бокам -- так строка хранится в структуре
            self.fill_test_cases(value.strip('"'))

    def analyze_tests(self):

        # Создаем индекс для парсинга исходного кода
        clang.cindex.Config.set_library_file("/usr/lib/llvm-17/lib/libclang.so")
        index = clang.cindex.Index.create()
        # Парсим исходный код и создаем единицу трансляции (translation unit)
        translation_unit = index.parse(self.filepath)

        # Проходим по всем узлам верхнего уровня (глобальные декларации)
        for _node in translation_unit.cursor.get_children():
            # Ищем функции, начинающиеся с "TEST", что обычно указывает на тестовые функции
            if _node.kind == clang.cindex.CursorKind.FUNCTION_DECL and _node.spelling.startswith("TEST"):
                # Анализируем содержимое тестовой функции
                self.walk_ast(_node)

        # Возвращаем результаты анализа
        return self.test_cases


if __name__ == "__main__":
    student_answer = """{{ STUDENT_ANSWER | e('py') }}"""
    language = """{{ ANSWER_LANGUAGE | e('py') }}""".lower()
    language_extension_map = {'cpp': 'cpp', 'python3': 'py'}

    if language not in language_extension_map.keys():
        raise Exception('Error in question. Unknown/unexpected language ({})'.format(language))

    filename = '__tester__.' + language_extension_map[language]

    if language == 'cpp':
        student_answer = """\n
#include <iostream>
#include <sstream>
#include <string>
#include <vector>


bool foo(const std::string& date_str) {
    // Проверка длины строки
    if (date_str.length() < 8 || date_str.length() > 10) {
        return false;
    }

    // Разделение строки на части
    std::vector<std::string> parts;
    std::string part;
    std::stringstream ss(date_str);

    while (std::getline(ss, part, '.')) {
        parts.push_back(part);
    }

    // Проверка, что дата разделена на три части
    if (parts.size() != 3) {
        return false;
    }

    try {
        int day = std::stoi(parts[0]);
        int month = std::stoi(parts[1]);
        int year = std::stoi(parts[2]);

        // Проверка значений дня, месяца и года
        if (day < 1 || day > 30) {
            return false;
        }
        if (month < 1 || month > 12) {
            return false;
        }
        if (year < 2001 || year > 2100) {
            return false;
        }

        // Проверка високосного года
        if (year % 4 == 0 && (year % 100 != 0 || year % 400 == 0)) {
            return false;
        }

        // Проверка на 13 июля
        if (day == 13 && month == 7) {
            return false;
        }

        return true;
    } catch (const std::invalid_argument&) {
        return false;
    } catch (const std::out_of_range&) {
        return false;
    }
}\n\n""" + student_answer

    else:
        student_answer = """\n
import pytest
import re


def foo(date_str):

    if not re.match(r'^\d{1,2}\.\d{1,2}\.\d{4}$', date_str):
        return False

    parts = date_str.split('.')

    try:
        day = int(parts[0])
        month = int(parts[1])
        year = int(parts[2])

        # Check day, month, year ranges
        if not (1 <= day <= 30):
            return False
        if not (1 <= month <= 12):
            return False
        if not (2001 <= year <= 2100):
            return False

        # Check for leap year
        if year % 4 == 0 and (year % 100 != 0 or year % 400 == 0):
            return False

        # Check for the specific date (13th July)
        if day == 13 and month == 7:
            return False

        return True
    except ValueError:
        return False\n\n""" + student_answer

    # Write the student code to a file

    with open(filename, "w") as src:
        print(student_answer, file=src)

    # Compile C++
    if language == 'cpp':

        return_code = subprocess.call(
            "g++ -std=c++11 -isystem /usr/include/gtest -pthread __tester__.cpp -lgtest -lgtest_main -o __tester__".split())
        if return_code != 0:
            raise Exception("** Compilation failed. Testing aborted **")

        obj = CTestParser(filepath=filename)
        exec_command = ["./__tester__"]

    else:  # Python doesn't need a compile phase
        obj = PythonTestParser(filepath=filename)
        exec_command = ["python3", "./__tester__.py"]

    correct_count = 0

    try:
        # Запускаем программу пользователя для проверки тестов
        output = run_tests(language_extension_map[language], exec_command)
        if not output.returncode == 0:
            raise Exception("** Error: mistake in user tests **")

        # объект с вызовом метода класса, который пропарсит код и записывает словарь со всеми тестами, аналогичный полю test_cases абстрактного класса, в 
        # котором отображено наличии у пользователя нужных тестов.
        correctness = obj.analyze_tests()

        for el in correctness.keys():
            if not correctness[el]:  # Если не все тесты проверены студентом, то сохраняем прежний вывод с небольшим упрощением
                result = 'Test: {}\n'.format('1')
                result += 'Your answer: {}\n'.format('Incorrect set of tests.')
                result += 'Correct: {}\n'.format('Correct set of tests.')
                print(result)
                break

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
    if correct_count == TRUE_TEST_AMOUNT:
        print('OK')
    else:
        print('Wrong answer')
