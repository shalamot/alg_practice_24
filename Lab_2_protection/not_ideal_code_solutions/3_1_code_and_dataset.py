
'''
def read_fleet(num_ships):
    fleet = []
    for _ in range(num_ships):
        ship_id, ship_class, firepower = map(int, input().split())
        fleet.append((ship_id, ship_class, firepower))
    return fleet

# Чтение данных для флота Роя
n = int(input())
roy_fleet = read_fleet(n)

# Чтение данных для флота Унатари
m = int(input())
unatari_fleet = read_fleet(m)

# Функция для сортировки
def sort_key(ship):
    return (ship[1], ship[2])

# Сортировка флота Роя
sorted_roy_fleet = sorted(roy_fleet, key=sort_key)

# Сортировка объединённого флота
combined_fleet = sorted(roy_fleet + unatari_fleet, key=sort_key)

# Вывод идентификаторов флота Роя
roy_ids = " ".join(str(ship[0]) for ship in sorted_roy_fleet)
print(roy_ids)

# Вывод идентификаторов объединённого флота
combined_ids = " ".join(str(ship[0]) for ship in combined_fleet)
print(combined_ids)
'''


'''
#include <iostream>
#include <vector>
#include <tuple>
#include <algorithm>

// Функция для чтения данных о флоте
std::vector<std::tuple<int, int, int>> read_fleet(int num_ships) {
    std::vector<std::tuple<int, int, int>> fleet;
    for (int i = 0; i < num_ships; ++i) {
        int ship_id, ship_class, firepower;
        std::cin >> ship_id >> ship_class >> firepower;
        fleet.push_back(std::make_tuple(ship_id, ship_class, firepower));
    }
    return fleet;
}

// Функция для сортировки
bool sort_key(const std::tuple<int, int, int>& a, const std::tuple<int, int, int>& b) {
    if (std::get<1>(a) != std::get<1>(b)) {
        return std::get<1>(a) < std::get<1>(b);
    }
    return std::get<2>(a) < std::get<2>(b);
}

int main() {
    int n, m;
    std::cin >> n;
    std::vector<std::tuple<int, int, int>> roy_fleet = read_fleet(n);

    std::cin >> m;
    std::vector<std::tuple<int, int, int>> unatari_fleet = read_fleet(m);

    // Сортировка флота Роя
    std::sort(roy_fleet.begin(), roy_fleet.end(), sort_key);

    // Сортировка объединённого флота
    std::vector<std::tuple<int, int, int>> combined_fleet = roy_fleet;
    combined_fleet.insert(combined_fleet.end(), unatari_fleet.begin(), unatari_fleet.end());
    std::sort(combined_fleet.begin(), combined_fleet.end(), sort_key);

    // Вывод идентификаторов флота Роя
    for (size_t i = 0; i < roy_fleet.size(); ++i) {
        std::cout << std::get<0>(roy_fleet[i]);
        if (i != roy_fleet.size() - 1) {
            std::cout << " ";
        }
    }
    std::cout << std::endl;

    // Вывод идентификаторов объединённого флота
    for (size_t i = 0; i < combined_fleet.size(); ++i) {
        std::cout << std::get<0>(combined_fleet[i]);
        if (i != combined_fleet.size() - 1) {
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
    # Функция для сортировки
    def sort_key(ship):
        return (ship[1], ship[2])

    def read_fleet(num_ships):
        fleet = []
        for _ in range(num_ships):
            ship_id, ship_class, firepower = map(int, info.pop(0).split())
            fleet.append((ship_id, ship_class, firepower))
        return fleet

    info = dataset.split('\n')
    info.pop()
    answ = ''

    # Чтение данных для флота Роя
    n = int(info.pop(0))
    roy_fleet = read_fleet(n)

    # Чтение данных для флота Унатари
    m = int(info.pop(0))
    unatari_fleet = read_fleet(m)

    # Сортировка флота Роя
    sorted_roy_fleet = sorted(roy_fleet, key=sort_key)

    # Сортировка объединённого флота
    combined_fleet = sorted(roy_fleet + unatari_fleet, key=sort_key)

    # Вывод идентификаторов флота Роя
    roy_ids = " ".join(str(ship[0]) for ship in sorted_roy_fleet)
    answ += roy_ids + '\n'

    # Вывод идентификаторов объединённого флота
    combined_ids = " ".join(str(ship[0]) for ship in combined_fleet)
    answ += combined_ids + '\n'

    return answ


print(foo("3\n1034 2 213\n1043 2 206\n2067 4 1407\n4\n709 5 2600\n904 4 1389\n1067 2 220\n1455 3 856\n"))

'''


'''
Варианты датасетов: 
    * Обычный (+)
    * Одинаковые классы в одном флоте по отдельности (+)
    * Одинаковые классы в двух флотах (+)
    * Один корабль в каждом флоту (+)
========================================
1)
3
1034 2 213
1043 2 206
2067 4 1407
4
709 5 2600
904 4 1389
1067 2 220
1455 3 856


1043 1034 2067
1043 1034 1067 1455 904 2067 709
========================================

========================================
2)
5
1034 2 213
1043 2 206
1049 2 207
1036 2 201
2067 3 877
5
709 5 2623
711 5 2600
904 4 1389
1067 6 12367
1455 3 856


1036 1043 1049 1034 2067
1036 1043 1049 1034 1455 2067 904 711 709 1067
========================================

========================================
3)
5
1034 2 213
1043 2 206
1049 2 207
1036 2 201
2067 3 877
5
103 2 212
104 2 208
109 2 209
106 2 210
221 3 944


1036 1043 1049 1034 2067
1036 1043 1049 104 109 106 103 1034 2067 221
========================================

========================================
4)
1
1034 2 213
1
103 2 212


1034
103 1034
========================================
'''
