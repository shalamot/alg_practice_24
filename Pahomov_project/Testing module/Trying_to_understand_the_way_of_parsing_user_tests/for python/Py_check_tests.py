import ast
import pytest

def run_all_tests(test_file_run):
    """
    Функция запускает все тесты из указанного файла с использованием pytest.

    Аргументы:
    test_file_run (str): Путь к файлу с тестами.

    Возвращает:
    int: Результат выполнения тестов (0 - все тесты пройдены успешно, другое значение - не все тесты пройдены).
    """
    # Запускаем тесты с флагом -v для подробного вывода
    result = pytest.main([test_file_run])

    # Проверяем статус выполнения тестов и выводим результат
    if result == 0:
        print("Все тесты пройдены успешно.")
    else:
        print("Не все тесты пройдены.")

    return result

def analyze_tests(file_path):
    """
    Функция анализирует тесты в указанном файле и проверяет наличие тестов на деление на ноль,
    положительное деление и отрицательное деление.

    Аргументы:
    file_path (str): Путь к файлу с тестами.

    Возвращает:
    dict: Словарь с ключами "division_by_zero", "division_positive", "division_negative" и значениями True или False,
    указывающими на наличие соответствующих тестов.
    """
    # Чтение и парсинг исходного кода тестового файла
    with open(file_path, "r") as file:
        tree = ast.parse(file.read())

    # Инициализация словаря для хранения результатов анализа
    test_cases = {
        "division_by_zero": False,
        "division_positive": False,
        "division_negative": False,
    }

    def check_divide(sub_node):
        """
        Вспомогательная функция для проверки вызова функции divide и анализа её аргументов.
        (Анализирует, является ли вызываемая функция функцией divide и корректно ли в неё переданы аргументы)

        Аргументы:
        sub_node (ast.Call): Узел AST, представляющий вызов функции.

        Исключения:
        ValueError: Если функция divide принимает не два аргумента или второй аргумент не является числом.
        """
        # Проверяем, является ли вызов функции вызовом функции 'divide'
        if isinstance(sub_node.func, ast.Name) and sub_node.func.id == "divide":

            # Проверяем, что в функцию передаются два аргумента
            if len(sub_node.args) != 2:
                raise ValueError("Функция divide должна принимать ровно два аргумента.")

            # Проверяем, что второй аргумент - это либо константа, либо унарная операция
            # В структуре AST отрицательное число представлено не типом ast.Constant, но ast.UnaryOp,
            # имеющего свой знак и операнд, что требует большего количества проверок

            second_arg = sub_node.args[1]
            value = None

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
                test_cases["division_by_zero"] = True
            elif value > 0 and not isinstance(second_arg, ast.UnaryOp):
                test_cases["division_positive"] = True
            elif value < 0 or isinstance(second_arg, ast.UnaryOp):
                test_cases["division_negative"] = True

    # Проход по узлам дерева AST
    for node in ast.walk(tree):
        # Ищем функции, начинающиеся с 'test_'
        if isinstance(node, ast.FunctionDef) and node.name.startswith("test_"):
            # Проход по узлам внутри функции теста
            for i, subnode in enumerate(ast.walk(node)):
                # Проверяем, является ли узел вызовом assert
                if isinstance(subnode, ast.Assert):
                    mas = list(ast.walk(node))[i:]

                    for elem in mas:
                        if isinstance(elem, ast.Call):  # Проверяем, есть ли после assert вызов функции
                            # Проверяем, относится ли он к divide
                            check_divide(elem)
                            break

    return test_cases

if __name__ == "__main__":
    file_path = "Py_tests.py"  # Замените на путь к вашему файлу с тестами

    # Запускаем все тесты и проверяем результат
    if run_all_tests(file_path) != 0:
        raise Exception('Tests Error: Не пройдены написанные пользователем тесты (проверьте корректность своих тестов).')

    # Анализируем тесты и выводим результаты
    results = analyze_tests(file_path)
    print("Test cases covered:")
    for case, covered in results.items():
        print(f"{case}: {'Yes' if covered else 'No'}")
