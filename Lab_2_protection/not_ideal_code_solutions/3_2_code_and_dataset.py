
'''
from datetime import datetime

# Функция для чтения и парсинга даты
def parse_date(date_str):
    return datetime.strptime(date_str, '%d.%m.%Y')

# Чтение данных
n = int(input())
students = []
for _ in range(n):
    data = input().split()
    name = data[0]
    birth_date = parse_date(data[1])
    grade = int(data[2])
    students.append((name, birth_date, grade))

# Сортировка студентов
sorted_students = sorted(students, key=lambda x: (x[2], -x[1].timestamp(), x[0]))

# Вывод имен студентов
result = " ".join(student[0] for student in sorted_students)
print(result)
'''


'''
#include <iostream>
#include <vector>
#include <tuple>
#include <algorithm>
#include <sstream>
#include <ctime>
#include <iomanip>

// Функция для парсинга даты
std::tm parse_date(const std::string& date_str) {
    std::tm tm = {};
    std::stringstream ss(date_str);
    ss >> std::get_time(&tm, "%d.%m.%Y");
    return tm;
}

// Функция для сравнения двух студентов
bool compare_students(const std::tuple<std::string, std::tm, int>& a, const std::tuple<std::string, std::tm, int>& b) {
    // Сравнение по оценке
    if (std::get<2>(a) != std::get<2>(b)) {
        return std::get<2>(a) < std::get<2>(b);
    }
    // Сравнение по дате рождения (по убыванию)
    if (std::mktime(const_cast<std::tm*>(&std::get<1>(a))) != std::mktime(const_cast<std::tm*>(&std::get<1>(b)))) {
        return std::mktime(const_cast<std::tm*>(&std::get<1>(a))) > std::mktime(const_cast<std::tm*>(&std::get<1>(b)));
    }
    // Сравнение по имени
    return std::get<0>(a) < std::get<0>(b);
}

int main() {
    int n;
    std::cin >> n;
    std::vector<std::tuple<std::string, std::tm, int>> students;

    // Чтение данных
    for (int i = 0; i < n; ++i) {
        std::string name, date_str;
        int grade;
        std::cin >> name >> date_str >> grade;
        students.emplace_back(name, parse_date(date_str), grade);
    }

    // Сортировка студентов
    std::sort(students.begin(), students.end(), compare_students);

    // Вывод имен студентов
    for (size_t i = 0; i < students.size(); ++i) {
        if (i != 0) {
            std::cout << " ";
        }
        std::cout << std::get<0>(students[i]);
    }
    std::cout << std::endl;

    return 0;
}
'''


'''
# moodle code style

from datetime import datetime

def foo(dataset):
    # Функция для чтения и парсинга даты
    def parse_date(date_str):
        return datetime.strptime(date_str, '%d.%m.%Y')

    # Чтение данных
    info = dataset.split('\n')
    info.pop()

    n = int(info.pop(0))
    students = []
    for _ in range(n):
        data = info.pop(0).split()
        name = data[0]
        birth_date = parse_date(data[1])
        grade = int(data[2])
        students.append((name, birth_date, grade))

    # Сортировка студентов
    sorted_students = sorted(students, key=lambda x: (x[2], -x[1].timestamp(), x[0]))

    # Вывод имен студентов
    result = " ".join(student[0] for student in sorted_students)
    return result


print(foo("4\nJake 14.4.2000 87\nMike 1.12.2004 90\nSamson 15.4.2001 84\nLucy 30.8.2004 78\n"))

'''


'''
Варианты датасетов:
    * Обычный (+)
    * Одинаковые оценки, разные даты рождения (+)
    * Одинаковые оценки, одинаковые даты рождения (+)
    * Один человек (+)
    * Второй и третий случаи вместе (+)
========================================
1)
4
Jake 14.4.2000 87
Mike 1.12.2004 90
Samson 15.4.2001 84
Lucy 30.8.2004 78


Lucy Samson Jake Mike
========================================

========================================
2)
4
Jake 14.4.2000 87
Mike 1.12.2004 90
Samson 15.4.2001 87
Lucy 30.8.2004 78


Lucy Samson Jake Mike
========================================

========================================
3)
4
Samson 15.4.2001 87
Jake 15.4.2001 87
Mike 1.12.2004 90
Lucy 30.8.2004 78


Lucy Jake Samson Mike
========================================

========================================
4)
1
Jake 14.4.2000 87


Jake
========================================

========================================
5)
6
Samson 15.4.2001 86
Jake 15.4.2001 87
Mike 1.12.2004 90
Lucy 30.8.2004 78
Ann 15.4.2001 86
Becky 30.12.2004 78


Becky Lucy Ann Samson Jake Mike
========================================
'''
