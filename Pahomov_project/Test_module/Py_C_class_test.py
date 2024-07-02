from abc import ABC, abstractmethod
import clang.cindex  # Импорт модуля clang для работы с AST
import ast
import pytest
import subprocess, sys, re

clang.cindex.Config.set_library_file(
    "C:\\Users\\stepa\\PycharmProjects\\pythonProject11\\venv\\Lib\\site-packages\\clang\\native\\libclang.dll"
)


def run_tests(lang, exec_comm):

    if lang == 'py':
        res = subprocess.run(["pytest", exec_comm[1][2:]], capture_output=True, text=True)
    else:
        res = subprocess.run([exec_comm], capture_output=True, text=True)

    return res


class TestParser(ABC):
    def __init__(self, filepath):
        self.filepath = filepath
        self.test_cases = {
            "division_by_zero": False,
            "division_positive": False,
            "division_negative": False,
        }

    @abstractmethod
    def analyze_tests(self):
        pass


class PythonTestParser(TestParser):

    def walk_ast(self, node, depth=0):

        if isinstance(node, ast.Call):
            self.check_divide(node)

        # Рекурсивно вызываем walk_ast для детей текущего узла
        for child in ast.iter_child_nodes(node):
            self.walk_ast(child, depth + 1)

    def check_divide(self, sub_node):

        # Проверяем, является ли вызов функции вызовом функции 'divide'
        if isinstance(sub_node.func, ast.Name) and sub_node.func.id == "divide":

            # Проверяем, что в функцию передаются два аргумента
            if len(sub_node.args) != 2:
                raise ValueError("Функция divide должна принимать ровно два аргумента.")

            # Проверяем, что второй аргумент - это либо константа, либо унарная операция
            # В структуре AST отрицательное число представлено не типом ast.Constant, но ast.UnaryOp,
            # имеющего свой знак и операнд, что требует большего количества проверок

            second_arg = sub_node.args[1]

            # Условия для присвоения значения переменной value, необходимой
            # для проставления наличия определённых типов проверок

            if isinstance(second_arg, ast.UnaryOp):
                # Проверяем, что унарный оператор - это отрицание (минус)
                if not isinstance(second_arg.op, ast.USub):
                    raise ValueError("Унарный оператор должен быть USub (унарный минус).")

                # Проверяем, что операнд унарной операции - это число
                if isinstance(second_arg.operand, ast.Constant):
                    value = -second_arg.operand.value
                else:
                    raise ValueError("Операнд UnaryOp должен быть числом.")
            elif isinstance(second_arg, ast.Constant):
                value = second_arg.value
            else:
                raise ValueError("Второй аргумент функции divide должен быть числом.")

            # Проверяем значение второго аргумента
            if value == 0:
                self.test_cases["division_by_zero"] = True
            elif value > 0 and not isinstance(second_arg, ast.UnaryOp):
                self.test_cases["division_positive"] = True
            elif value < 0 or isinstance(second_arg, ast.UnaryOp):
                self.test_cases["division_negative"] = True

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

        # Проверяем, является ли узел вызовом функции divide
        if node.kind == clang.cindex.CursorKind.CALL_EXPR:
            # Если это вызов функции divide, проверяем её аргументы
            if node.kind == clang.cindex.CursorKind.CALL_EXPR and node.spelling == 'divide':
                self.check_divide(node)

        # Рекурсивно вызываем walk_ast для детей текущего узла
        for child in node.get_children():
            self.walk_ast(child, depth + 1)

    def check_divide(self, node):

        # Получаем аргументы функции
        args = list(node.get_arguments())
        value = None  # Инициализируем переменную для хранения значения аргумента
        key = False  # Инициализируем ключ для проверки унарного оператора

        # Проверяем, что функция имеет ровно два аргумента
        if len(args) == 2:
            right_arg = args[1]  # Получаем второй аргумент функции

            # Проверяем, что второй аргумент - это либо целое число, либо унарная операция
            if right_arg.kind not in [clang.cindex.CursorKind.INTEGER_LITERAL,
                                      clang.cindex.CursorKind.UNARY_OPERATOR]:
                return

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
            elif value > 0 and not key:
                self.test_cases["division_positive"] = True
            elif value > 0 and key:
                self.test_cases["division_negative"] = True

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
    file_path = "Py_tests.py"  # Замените на путь к вашему файлу с тестами
    # file_path = "C_tests.cpp"  # Замените на путь к вашему файлу с тестами
    name, language = file_path.split('.')

    if language not in ['cpp', 'py']:
        raise Exception('Error in question. Unknown/unexpected language ({})'.format(language))

    if language == 'cpp':
        obj = CTestParser(filepath=file_path)
        string_command_list = f'g++ -o {name} {file_path}'.split()
        return_code = subprocess.call(string_command_list)

        if return_code != 0:
            raise Exception("** Compilation failed. Testing aborted **")
        exec_command = ['./' + name]

    else:  # Python doesn't need a compile phase
        obj = PythonTestParser(filepath=file_path)
        exec_command = ["python3", './' + file_path]

    correct_count = 0

    try:
        # Запускаем программу пользователя для проверки тестов
        output = run_tests(language, exec_command)
        if not output.returncode == 0:
            raise Exception("** Error: mistake in user tests **")

        # Здесь будет объект с вызовом метода класса, который пропарсит код и вернёт некий ответ (True / False)
        correctness = obj.analyze_tests()

        for el in correctness.keys():
            if not correctness[el]:  # Если не все тесты проверены студентом, то сохраняем прежний вывод с небольшим упрощением
                result = 'Test: {}\n'.format('1')
                result += 'Your answer: {}\n'.format('Incorrect set of tests.')
                result += 'Correct: {}\n'.format('Correct set of tests.')
                print(result)
                break
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
