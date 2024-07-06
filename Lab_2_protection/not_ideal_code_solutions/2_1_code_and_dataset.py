
'''
def calculate_average_grades(grades):
    """
    Вычислить средний балл для каждого ученика.
    """
    from collections import defaultdict
    students = defaultdict(list)

    for student_id, grade in grades:
        students[student_id].append(grade)

    # Рассчитываем средний балл для каждого ученика
    average_grades = {student: sum(grades) / len(grades) for student, grades in students.items()}
    return average_grades


# Ввод данных
n = int(input())
grades_11A = [tuple(map(int, input().split())) for _ in range(n)]

m = int(input())
grades_11B = [tuple(map(int, input().split())) for _ in range(m)]

# Вычисление среднего балла для каждого ученика в 11А и 11Б
average_grades_11A = calculate_average_grades(grades_11A)
average_grades_11B = calculate_average_grades(grades_11B)

# Сортировка учеников по убыванию среднего балла
sorted_11A = sorted(average_grades_11A.items(), key=lambda x: (x[1], x[0]), reverse=True)
sorted_11B = sorted(average_grades_11B.items(), key=lambda x: (x[1], x[0]), reverse=True)

# Вывод номеров учеников 11А в порядке убывания среднего балла
print(" ".join(str(student_id) for student_id, _ in sorted_11A))

# Вывод номеров учеников 11Б в порядке убывания среднего балла
print(" ".join(str(student_id) for student_id, _ in sorted_11B))

# Объединение списков и сортировка по возрастанию среднего балла
all_students = list(average_grades_11A.items()) + list(average_grades_11B.items())
sorted_all_students = sorted(all_students, key=lambda x: (x[1], x[0]))

# Вывод общего списка учеников
print(" ".join(str(student_id) for student_id, _ in sorted_all_students))
'''


'''
#include <iostream>
#include <vector>
#include <unordered_map>
#include <algorithm>

// Функция для вычисления среднего балла для каждого ученика
std::unordered_map<int, double> calculate_average_grades(const std::vector<std::pair<int, int>>& grades) {
    std::unordered_map<int, std::vector<int>> students;

    // Заполнение данных об учениках
    for (const auto& grade : grades) {
        students[grade.first].push_back(grade.second);
    }

    // Вычисление среднего балла для каждого ученика
    std::unordered_map<int, double> average_grades;
    for (const auto& student : students) {
        const std::vector<int>& grades = student.second;
        double sum = 0.0;
        for (int grade : grades) {
            sum += grade;
        }
        average_grades[student.first] = sum / grades.size();
    }

    return average_grades;
}

// Функция для сравнения пар (ученик, средний балл) для сортировки
bool compare_students(const std::pair<int, double>& a, const std::pair<int, double>& b) {
    if (a.second == b.second) {
        return a.first > b.first; // Сортировка по возрастанию номера ученика при равенстве среднего балла
    }
    return a.second > b.second; // Сортировка по убыванию среднего балла
}

bool compare_students_2(const std::pair<int, double>& a, const std::pair<int, double>& b) {
    if (a.second == b.second) {
        return a.first < b.first; // Сортировка по возрастанию номера ученика при равенстве среднего балла
    }
    return a.second < b.second; // Сортировка по убыванию среднего балла
}

int main() {
    int n;
    std::cin >> n;
    std::vector<std::pair<int, int>> grades_11A(n);

    // Ввод данных для 11A класса
    for (int i = 0; i < n; ++i) {
        std::cin >> grades_11A[i].first >> grades_11A[i].second;
    }

    int m;
    std::cin >> m;
    std::vector<std::pair<int, int>> grades_11B(m);

    // Ввод данных для 11B класса
    for (int i = 0; i < m; ++i) {
        std::cin >> grades_11B[i].first >> grades_11B[i].second;
    }

    // Вычисление среднего балла для каждого класса
    auto average_grades_11A = calculate_average_grades(grades_11A);
    auto average_grades_11B = calculate_average_grades(grades_11B);

    // Сортировка учеников 11A по убыванию среднего балла
    std::vector<std::pair<int, double>> sorted_11A(average_grades_11A.begin(), average_grades_11A.end());
    std::sort(sorted_11A.begin(), sorted_11A.end(), compare_students);

    // Сортировка учеников 11B по убыванию среднего балла
    std::vector<std::pair<int, double>> sorted_11B(average_grades_11B.begin(), average_grades_11B.end());
    std::sort(sorted_11B.begin(), sorted_11B.end(), compare_students);

    // Вывод учеников 11A в порядке убывания среднего балла
    for (int i = 0; i < sorted_11A.size(); ++i) {
        std::cout << sorted_11A[i].first;
        if (i != sorted_11A.size() - 1) {
            std::cout << " ";
        }
    }
    std::cout << std::endl;

    // Вывод учеников 11B в порядке убывания среднего балла
    for (int i = 0; i < sorted_11B.size(); ++i) {
        std::cout << sorted_11B[i].first;
        if (i != sorted_11B.size() - 1) {
            std::cout << " ";
        }
    }
    std::cout << std::endl;

    // Объединение списков и сортировка по убыванию среднего балла, и по возрастанию номера при равенстве баллов
    std::vector<std::pair<int, double>> all_students(sorted_11A.begin(), sorted_11A.end());
    all_students.insert(all_students.end(), sorted_11B.begin(), sorted_11B.end());
    std::sort(all_students.begin(), all_students.end(), compare_students_2);

    // Вывод общего списка учеников
    for (int i = 0; i < all_students.size(); ++i) {
        std::cout << all_students[i].first;
        if (i != all_students.size() - 1) {
            std::cout << " ";
        }
    }
    std::cout << std::endl;

    return 0;
}
'''


'''
# moodle code style

def foo(dataset):
    def calculate_average_grades(grades):
        # Средний балл для каждого ученика.

        from collections import defaultdict
        students = defaultdict(list)

        for student_id, grade in grades:
            students[student_id].append(grade)

        # Рассчитываем средний балл для каждого ученика
        average_grades = {student: sum(grades) / len(grades) for student, grades in students.items()}
        return average_grades

    parse = dataset.split('\n')
    answ = ''

    n = int(parse.pop(0))
    grades_11A = [tuple(map(int, parse.pop(0).split())) for _ in range(n)]

    m = int(parse.pop(0))
    grades_11B = [tuple(map(int, parse.pop(0).split())) for _ in range(m)]

    # Вычисление среднего балла для каждого ученика в 11А и 11Б
    average_grades_11A = calculate_average_grades(grades_11A)
    average_grades_11B = calculate_average_grades(grades_11B)

    # Сортировка учеников по убыванию среднего балла
    sorted_11A = sorted(average_grades_11A.items(), key=lambda x: (x[1], x[0]), reverse=True)
    sorted_11B = sorted(average_grades_11B.items(), key=lambda x: (x[1], x[0]), reverse=True)

    # Вывод номеров учеников 11А в порядке убывания среднего балла
    answ += " ".join(str(student_id) for student_id, _ in sorted_11A) + '\n'

    # Вывод номеров учеников 11Б в порядке убывания среднего балла
    answ += " ".join(str(student_id) for student_id, _ in sorted_11B) + '\n'

    # Объединение списков и сортировка по возрастанию среднего балла
    all_students = list(average_grades_11A.items()) + list(average_grades_11B.items())
    sorted_all_students = sorted(all_students, key=lambda x: (x[1], x[0]))

    # Вывод общего списка учеников
    answ += " ".join(str(student_id) for student_id, _ in sorted_all_students) + '\n'

    return answ


print(foo("4\n1 3\n4 4\n4 5\n2 4\n2\n5 5\n7 4\n"))
'''


'''
Варианты датасетов: (порядке уменьшения среднего балла и номеров для групп + возрастания для всех учеников и их номеров

    * Обычный (+)
    * Одинаковый средний балл студентов одной группы (+)
    * Одинаковый средний балл в массиве всех студентов (в разных группах по человеку) (+)
========================================
1)
4
1 3
4 4
4 5
2 4
2
5 5
7 4


4 2 1
5 7
1 2 7 4 5
========================================

========================================
2)
4
3 4
5 4
6 5
4 3
4
2 5
2 2
8 2
8 1


6 5 3 4
2 8
8 4 2 3 5 6
========================================

========================================
3)
4
3 4
5 4
6 5
4 3
4
2 4
2 4
8 5
8 3


6 5 3 4
8 2
4 2 3 5 8 6
========================================

========================================
4)
1
4 5
1
4 5


4
4
4 4
========================================
'''
