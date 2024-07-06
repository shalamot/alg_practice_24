
'''
n = int(input())
tasks = [input().split() for _ in range(n)]

# Обработка задач, группировка по проектам
projects = {}
for task in tasks:
    project_name, priority, duration = task[0], int(task[1]), int(task[2])
    if project_name not in projects:
        projects[project_name] = {'priorities': [], 'total_duration': 0}
    projects[project_name]['priorities'].append(priority)
    projects[project_name]['total_duration'] += duration

# Вычисление среднего приоритета и суммарной длительности
project_stats = []
for project, data in projects.items():
    average_priority = sum(data['priorities']) / len(data['priorities'])
    total_duration = data['total_duration']
    project_stats.append((project, average_priority, total_duration))

# Сортировка проектов
sorted_projects = sorted(
    project_stats,
    key=lambda x: (x[1], x[2], x[0])
)

# Вывод названий проектов
result = ''.join(project[0] for project in sorted_projects)
print(result)
'''


'''
#include <iostream>
#include <vector>
#include <unordered_map>
#include <algorithm>
#include <numeric>

struct ProjectData {
    std::vector<int> priorities;
    int total_duration = 0;
};

struct ProjectStats {
    char name;
    double average_priority;
    int total_duration;
};

bool compareProjects(const ProjectStats& a, const ProjectStats& b) {
    if (a.average_priority != b.average_priority) {
        return a.average_priority < b.average_priority;
    }
    if (a.total_duration != b.total_duration) {
        return a.total_duration < b.total_duration;
    }
    return a.name < b.name;
}

int main() {
    int n;
    std::cin >> n;
    std::vector<std::tuple<char, int, int>> tasks(n);

    // Ввод данных задач
    for (int i = 0; i < n; ++i) {
        char project_name;
        int priority, duration;
        std::cin >> project_name >> priority >> duration;
        tasks[i] = std::make_tuple(project_name, priority, duration);
    }

    // Обработка задач, группировка по проектам
    std::unordered_map<char, ProjectData> projects;
    for (const auto& task : tasks) {
        char project_name = std::get<0>(task);
        int priority = std::get<1>(task);
        int duration = std::get<2>(task);
        projects[project_name].priorities.push_back(priority);
        projects[project_name].total_duration += duration;
    }

    // Вычисление среднего приоритета и суммарной длительности
    std::vector<ProjectStats> project_stats;
    for (const auto& project : projects) {
        char project_name = project.first;
        const ProjectData& data = project.second;
        double average_priority = std::accumulate(data.priorities.begin(), data.priorities.end(), 0.0) / data.priorities.size();
        project_stats.push_back({project_name, average_priority, data.total_duration});
    }

    // Сортировка проектов
    std::sort(project_stats.begin(), project_stats.end(), compareProjects);

    // Вывод названий проектов
    for (size_t i = 0; i < project_stats.size(); ++i) {
        std::cout << project_stats[i].name;
    }
    std::cout << std::endl;

    return 0;
}
'''


'''
# moodle code style

def foo(dataset):
    info = dataset.split('\n')
    info.pop()

    n = int(info.pop(0))
    tasks = [info.pop(0).split() for _ in range(n)]

    # Обработка задач, группировка по проектам
    projects = {}
    for task in tasks:
        project_name, priority, duration = task[0], int(task[1]), int(task[2])
        if project_name not in projects:
            projects[project_name] = {'priorities': [], 'total_duration': 0}
        projects[project_name]['priorities'].append(priority)
        projects[project_name]['total_duration'] += duration

    # Вычисление среднего приоритета и суммарной длительности
    project_stats = []
    for project, data in projects.items():
        average_priority = sum(data['priorities']) / len(data['priorities'])
        total_duration = data['total_duration']
        project_stats.append((project, average_priority, total_duration))

    # Сортировка проектов
    sorted_projects = sorted(
        project_stats,
        key=lambda x: (x[1], x[2], x[0])
    )

    # Вывод названий проектов
    answ = ''.join(project[0] for project in sorted_projects)
    return answ


print(foo("5\nA 3 45\nA 4 14\nB 2 67\nB 8 11\nA 10 22\n"))

'''


'''
Варианты датасетов: 

    * Обычный (+)
    * Если два проекта имеют одинаковый средний приоритет (+)
    * Если два проекта имеют одинаковый средний приоритет и суммарную длительность (+).
    * Одиночный проект (+)
========================================
1)
5
A 3 45
A 4 14
B 2 67
B 8 11
A 10 22


BA
========================================

========================================
2)
6
A 5 100
A 5 23
A 5 16
B 4 45
B 6 69
B 5 23


BA
========================================

========================================
3)
18
S 5 100
S 5 23
S 5 16
B 4 45
B 6 69
B 5 23
A 5 100
A 5 23
A 5 16
N 4 45
N 6 69
N 5 23
G 5 100
G 5 23
G 5 16
K 4 45
K 6 69
K 5 23


BKNAGS
========================================

========================================
4)
1
A 3 45


A
========================================








5
A 3 45
A 4 14
B 2 67
B 8 11
A 10 22


BA




'''
