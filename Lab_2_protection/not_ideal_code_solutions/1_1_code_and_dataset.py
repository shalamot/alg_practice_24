'''
classes_amount = int(input())
people_in_classes = list(map(int, input().split()))
all_classes = [list(map(int, input().split())) for _ in range(classes_amount)]

average = []
all_stud_mas = []
for i in range(len(all_classes)):
    all_classes[i].sort()
    average.append(sum(all_classes[i]) / len(all_classes[i]))
    all_stud_mas.extend(all_classes[i])

all_classes.sort(key=lambda x: (sum(x) / len(x), -len(x)))
for el in all_classes:
    print(*el)
print(*sorted(all_stud_mas))
'''


'''
#include <iostream>
#include <vector>
#include <algorithm>
#include <numeric>

int main() {
    int classes_amount;
    std::cin >> classes_amount;

    std::vector<int> people_in_classes(classes_amount);
    for (int i = 0; i < classes_amount; ++i) {
        std::cin >> people_in_classes[i];
    }

    std::vector<std::vector<int>> all_classes(classes_amount);
    for (int i = 0; i < classes_amount; ++i) {
        all_classes[i].resize(people_in_classes[i]);
        for (int j = 0; j < people_in_classes[i]; ++j) {
            std::cin >> all_classes[i][j];
        }
    }

    std::vector<double> average(classes_amount);
    std::vector<int> all_stud_mas;
    for (int i = 0; i < classes_amount; ++i) {
        std::sort(all_classes[i].begin(), all_classes[i].end());
        average[i] = std::accumulate(all_classes[i].begin(), all_classes[i].end(), 0.0) / all_classes[i].size();
        all_stud_mas.insert(all_stud_mas.end(), all_classes[i].begin(), all_classes[i].end());
    }

    std::sort(all_classes.begin(), all_classes.end(), [](const std::vector<int>& a, const std::vector<int>& b) {
        double avg_a = std::accumulate(a.begin(), a.end(), 0.0) / a.size();
        double avg_b = std::accumulate(b.begin(), b.end(), 0.0) / b.size();
        if (avg_a == avg_b) {
            return a.size() > b.size();
        }
        return avg_a < avg_b;
    });

    for (const auto& el : all_classes) {
        for (size_t i = 0; i < el.size(); ++i) {
            std::cout << el[i];
            if (i < el.size() - 1) {
                std::cout << " ";
            }
        }
        std::cout << std::endl;
    }

    std::sort(all_stud_mas.begin(), all_stud_mas.end());
    for (size_t i = 0; i < all_stud_mas.size(); ++i) {
        std::cout << all_stud_mas[i];
        if (i < all_stud_mas.size() - 1) {
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
    data = dataset.split('\n')
    needed_data = data[2:len(data) - 1]
    all_classes = [list(map(int, needed_data[i].split())) for i in range(len(needed_data))]
    answ = ''

    all_stud_mas = []
    for i in range(len(all_classes)):
        all_classes[i].sort()
        all_stud_mas.extend(all_classes[i])

    all_classes.sort(key=lambda x: (sum(x) / len(x), -len(x)))
    for el in all_classes:
        answ = answ + ' '.join(list(map(str, el))) + '\n'

    answ += ' '.join(list(map(str, sorted(all_stud_mas))))

    return answ


str_foo = foo("3\n4 4 4\n70 70 70 70\n56 37 49 54\n84 68 70 24\n")
print(str_foo)
'''


'''
========================================
1)
3
4 2 3
34 86 75 90
98 54
84 68 70


34 75 86 90
68 70 84
54 98
34 54 68 70 75 84 86 90 98
========================================

========================================
2)
3
4 4 4
70 70 70 70
56 37 49 54
84 68 70 24


37 49 54 56
24 68 70 84
70 70 70 70
24 37 49 54 56 68 70 70 70 70 70 84
========================================

========================================
3)
4
4 2 3 1
70 70 70 70
70 70
70 70 70
70


70 70 70 70
70 70 70
70 70
70
70 70 70 70 70 70 70 70 70 70
========================================

========================================
4)
5
1 1 3 1 1
78
35
78 82 74
90
43


35
43
74 78 82 
78
90
35 43 74 78 78 82 90
========================================
'''