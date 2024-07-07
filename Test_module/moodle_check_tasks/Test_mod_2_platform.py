from abc import ABC, abstractmethod
import clang.cindex  # Импорт модуля clang для работы с AST
import ast
import pytest
import subprocess, sys, re

TRUE_TEST_AMOUNT = 4


def run_tests(lang, exec_comm):
    if lang == 'py':
        res = subprocess.run(["pytest", exec_comm[1][2:]], capture_output=True, text=True)
    else:
        res = subprocess.run(exec_comm, capture_output=True, text=True)

    return res


class TestParser(ABC):
    def __init__(self, filepath):
        self.filepath = filepath
        self.test_cases = {
            "division_by_zero": False,
            "division_by_3": False,
            "division_by_6": False,
            "negative_num": False,
        }

    @abstractmethod
    def analyze_tests(self):
        pass


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

            # Проверяем, что в функцию передаются два аргумента
            if len(sub_node.args) != 1:
                raise Exception("Функция foo должна принимать ровно один аргумент.")

            # Проверяем, что аргумент - это либо константа, либо унарная операция
            # В структуре AST отрицательное число представлено не типом ast.Constant, но ast.UnaryOp,
            # имеющего свой знак и операнд, что требует большего количества проверок

            _arg = sub_node.args[0]

            # Условия для присвоения значения переменной value, необходимой
            # для проставления наличия определённых типов проверок

            if isinstance(_arg, ast.UnaryOp):
                # Проверяем, что унарный оператор - это отрицание (минус)
                if not isinstance(_arg.op, ast.USub):
                    raise Exception("Унарный оператор должен быть USub (унарный минус).")

                # Проверяем, что операнд унарной операции - это число
                if isinstance(_arg.operand, ast.Constant):
                    value = -_arg.operand.value
                else:
                    raise Exception("Операнд UnaryOp должен быть числом.")
            elif isinstance(_arg, ast.Constant):
                value = _arg.value
            else:
                raise Exception("Аргумент функции foo должен быть целым числом.")

            # Проверяем значение аргумента
            if value == 0:
                self.test_cases["division_by_zero"] = True
            elif value == 3:
                self.test_cases["division_by_3"] = True
            elif value == 6:
                self.test_cases["division_by_6"] = True
            elif value < 0:
                self.test_cases["negative_num"] = True

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
        if node.kind == clang.cindex.CursorKind.CALL_EXPR:
            # Если это вызов функции divide, проверяем её аргументы
            if node.kind == clang.cindex.CursorKind.CALL_EXPR and node.spelling == 'foo':
                self.check_func(node)

        # Рекурсивно вызываем walk_ast для детей текущего узла
        for child in node.get_children():
            self.walk_ast(child, depth + 1)

    def check_func(self, node):

        # Получаем аргументы функции
        args = list(node.get_arguments())
        value = None  # Инициализируем переменную для хранения значения аргумента
        key = False  # Инициализируем ключ для проверки унарного оператора

        if len(args) != 1:
            raise Exception("Функция foo должна принимать ровно один аргумент.")
        # Проверяем, что функция имеет ровно один аргумент
        else:
            right_arg = args[0]  # Получаем аргумент функции

            # Проверяем, что аргумент - это либо целое число, либо унарная операция
            if right_arg.kind not in [clang.cindex.CursorKind.INTEGER_LITERAL,
                                      clang.cindex.CursorKind.UNARY_OPERATOR]:
                raise Exception("Аргумент функции foo должен быть целым числом.")

            # Если это унарная операция, получаем её операнд
            if right_arg.kind == clang.cindex.CursorKind.UNARY_OPERATOR:
                # Получаем дочерние узлы унарного оператора
                right_arg = list(right_arg.get_children())[0]
                key = True  # Устанавливаем ключ в True

            # Получаем значение аргумента и преобразуем его в целое число
            value = list(right_arg.get_tokens())[0].spelling
            value = int(value)

            # Проверяем значение аргумента и обновляем словарь test_cases
            if value == 0:
                self.test_cases["division_by_zero"] = True
            elif value == 3 and not key:
                self.test_cases["division_by_3"] = True
            elif value == 6 and not key:
                self.test_cases["division_by_6"] = True
            elif value > 0 and key:
                self.test_cases["negative_num"] = True

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
#include <cmath>


double foo(int n) {
    if (n <= 0 || n == 3 || n == 6) {
        return -1;
    }
    return std::round(std::abs(std::sqrt(n) + 1.0 / n + std::pow(n, 2) - 16.0 / ((std::pow(n, 2) - 9) * (n * 6))) * 100) / 100.0;
}\n\n""" + student_answer

    else:
        student_answer = """\n
import pytest

def foo(n):
    if not isinstance(n, int):
        raise Exception("** Program failed. Incorrect type for function foo **")
    if n in [3, 6] or n <= 0:
        return -1
    return abs(math.sqrt(n) + 1/n + n**2 - 16/((n**2 - 9)*(n * 6))).__round__()\n\n""" + student_answer

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
