import clang.cindex  # Импортируем модуль clang для работы с AST

# Устанавливаем путь к библиотеке libclang
clang.cindex.Config.set_library_file("C:\\Users\\stepa\\PycharmProjects\\pythonProject11\\venv\\Lib\\site-packages\\clang\\native\\libclang.dll")  # замените на фактический путь к вашей libclang.dll

def analyze_tests(file_path):
    """
    Функция анализирует тесты в указанном C++ файле и проверяет наличие тестов на деление на ноль,
    положительное деление и отрицательное деление.

    Аргументы:
    file_path (str): Путь к файлу с тестами.

    Возвращает:
    dict: Словарь с ключами "division_by_zero", "division_positive", "division_negative" и значениями True или False,
    указывающими на наличие соответствующих тестов.
    """
    # Создаем индекс для парсинга исходного кода
    index = clang.cindex.Index.create()
    # Парсим исходный код и создаем единицу трансляции (translation unit)
    translation_unit = index.parse(file_path)

    # Инициализация словаря для хранения результатов анализа
    test_cases = {
        "division_by_zero": False,
        "division_positive": False,
        "division_negative": False,
    }

    def is_divide_call(node):
        """
        Проверяет, является ли данный узел вызовом функции divide.

        Аргументы:
        node (clang.cindex.Cursor): Узел AST.

        Возвращает:
        bool: True, если узел является вызовом функции divide, иначе False.
        """
        # Проверяем, является ли узел вызовом функции
        if node.kind == clang.cindex.CursorKind.CALL_EXPR:
            # Проходим по дочерним узлам
            for child in node.get_children():
                # Проверяем все возможные варианты узлов (именно в них хранится информация о вызываемой функции)
                if child.kind in [clang.cindex.CursorKind.UNEXPOSED_EXPR, clang.cindex.CursorKind.DECL_REF_EXPR]:
                    # Проверяем, является ли дочерний узел функцией divide
                    if child.spelling == 'divide':
                        return True
                    # Если узел типа UNEXPOSED_EXPR, проверяем его детей (особенность структуры
                    for grandchild in child.get_children():
                        # Проверяем, является ли внук узлом типа DECL_REF_EXPR и функцией divide
                        if grandchild.kind == clang.cindex.CursorKind.DECL_REF_EXPR and grandchild.spelling == 'divide':
                            return True
        return False

    def check_division_arguments(node):
        """
        Проверяет аргументы функции divide на предмет деления на ноль, положительного или отрицательного деления.

        Аргументы:
        node (clang.cindex.Cursor): Узел AST, представляющий вызов функции divide.
        """
        # Получаем аргументы функции
        args = list(node.get_arguments())
        value = None  # Инициализируем переменную для хранения значения аргумента
        key = False  # Инициализируем ключ для проверки унарного оператора

        # Проверяем, что функция имеет ровно два аргумента
        if len(args) == 2:
            right_arg = args[1]  # Получаем второй аргумент функции

            # Проверяем, что второй аргумент - это либо целое число, либо унарная операция
            if right_arg.kind not in [clang.cindex.CursorKind.INTEGER_LITERAL, clang.cindex.CursorKind.UNARY_OPERATOR]:
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
                test_cases["division_by_zero"] = True
            elif value > 0 and not key:
                test_cases["division_positive"] = True
            elif value > 0 and key:
                test_cases["division_negative"] = True

    def walk_ast(node, depth=0):
        """
        Рекурсивно проходит по узлам дерева AST и анализирует их.

        Аргументы:
        node (clang.cindex.Cursor): Текущий узел AST.
        depth (int): Текущая глубина рекурсии (используется для отступов в печати).
        """

        print("    " * depth + f"{node.kind.name} - {node.spelling}")  #---- для демонстрации вложенности (ВАЖНО)

        # Проверяем, является ли узел вызовом функции divide
        if node.kind == clang.cindex.CursorKind.CALL_EXPR:
            # Если это вызов функции divide, проверяем её аргументы
            if is_divide_call(node):
                check_division_arguments(node)

        # Рекурсивно вызываем walk_ast для детей текущего узла
        for child in node.get_children():
            walk_ast(child, depth + 1)

    # Проходим по всем узлам верхнего уровня (глобальные декларации)
    for _node in translation_unit.cursor.get_children():
        # Ищем функции, начинающиеся с "TEST", что обычно указывает на тестовые функции
        if _node.kind == clang.cindex.CursorKind.FUNCTION_DECL and _node.spelling.startswith("TEST"):
            # Анализируем содержимое тестовой функции
            walk_ast(_node)

    # Возвращаем результаты анализа
    return test_cases


if __name__ == "__main__":
    # Замените на путь к вашему файлу с тестами
    _file_path = "C_tests.cpp"
    # Получаем результаты анализа тестов
    results = analyze_tests(_file_path)
    # Печатаем результаты анализа
    print("Test cases covered:")
    for case, covered in results.items():
        print(f"{case}: {'Yes' if covered else 'No'}")
