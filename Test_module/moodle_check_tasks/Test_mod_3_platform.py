from abc import ABC, abstractmethod
import clang.cindex  # Импорт модуля clang для работы с AST
import ast
import pytest
import subprocess, sys, re

clang.cindex.Config.set_library_file("/usr/local/lib/python3.8/dist-packages/clang/native/libclang.so")
TRUE_TEST_AMOUNT = 3


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
        self.func_builtin_str_len = 21
        self.test_cases = {
            "cut_negative": False,
            "cut_over_len": False,
            "cut_possible": False,
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

            # Проверяем, что в функцию передается один аргумент
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
            if value < 0:
                self.test_cases["cut_negative"] = True
            elif value >= self.func_builtin_str_len:
                self.test_cases["cut_over_len"] = True
            elif 0 < value < self.func_builtin_str_len:
                self.test_cases["cut_possible"] = True

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
        # что стоит следующим значением. Если был вызов функции, мы делаем её True, если она встретилась следующей по итерации
        if (
                node.kind == clang.cindex.CursorKind.CALL_EXPR or node.kind == clang.cindex.CursorKind.OVERLOADED_DECL_REF) and node.spelling == 'foo' or self.func_key:
            # Если это вызов функции foo, проверяем её аргументы
            if self.func_key:
                self.check_func(node)
            else:
                self.func_key = True

        # Рекурсивно вызываем walk_ast для детей текущего узла
        for child in node.get_children():
            self.walk_ast(child, depth + 1)

    def check_func(self, node):

        value = None  # Инициализируем переменную для хранения значения аргумента
        key = False  # Инициализируем ключ для проверки унарного оператора

        # Проверяем, что аргумент - это либо целое число, либо унарная операция
        if node.kind not in [clang.cindex.CursorKind.INTEGER_LITERAL, clang.cindex.CursorKind.UNARY_OPERATOR]:
            raise Exception("Аргумент функции foo должен быть целым числом.")
        else:

            # Получаем целочисленным переменную

            # Если это унарная операция, получаем её операнд
            if node.kind == clang.cindex.CursorKind.UNARY_OPERATOR:
                # Получаем дочерние узлы унарного оператора
                node = list(node.get_children())[0]
                key = True  # Устанавливаем ключ в True

            value = list(node.get_tokens())[0].spelling
            value = int(value)
            self.func_key = False

            # Проверяем значение аргумента и обновляем словарь test_cases
            if value > 0 and key:
                self.test_cases["cut_negative"] = True
            elif value >= self.func_builtin_str_len and not key:
                self.test_cases["cut_over_len"] = True
            elif 0 < value < self.func_builtin_str_len and not key:
                self.test_cases["cut_possible"] = True

    def analyze_tests(self):

        # Создаем индекс для парсинга исходного кода
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
    saved_for_cpp = student_answer
    language = """{{ ANSWER_LANGUAGE | e('py') }}""".lower()
    language_extension_map = {'cpp': 'cpp', 'python3': 'py'}

    if language not in language_extension_map.keys():
        raise Exception('Error in question. Unknown/unexpected language ({})'.format(language))

    filename = '__tester__.' + language_extension_map[language]
    for_cpp_filename = 'for_cpp.cpp'

    if language == 'cpp':
        student_answer = """\n
#include <string>
#include <gtest/gtest.h>

bool foo(int idx) {
    std::string foo_string = "This is foo() string.";
    if (idx < 0 || idx >= foo_string.length()) {
        return false;
    }
    return true;
}\n\n""" + student_answer

        if '#include' and 'gtest' in saved_for_cpp:
            raise Exception('Уберите импорт библиотеки :)')

        with open(for_cpp_filename, "w") as src:
            print(saved_for_cpp, file=src)

    else:
        student_answer = """\n
import pytest

def foo(idx):
    foo_string = 'This is foo() string.'
    if idx < 0 or len(foo_string) <= idx:
        return False
    return True\n\n""" + student_answer

    # Write the student code to a file

    with open(filename, "w") as src:
        print(student_answer, file=src)

    # Compile C++
    if language == 'cpp':

        return_code = subprocess.call(
            "g++ -std=c++11 -isystem /usr/include/gtest -pthread __tester__.cpp -lgtest -lgtest_main -o __tester__".split())
        if return_code != 0:
            raise Exception("** Compilation failed. Testing aborted **")

        obj = CTestParser(filepath=for_cpp_filename)
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
            if not correctness[
                el]:  # Если не все тесты проверены студентом, то сохраняем прежний вывод с небольшим упрощением
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