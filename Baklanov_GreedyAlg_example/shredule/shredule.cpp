#include <iostream>
#include <vector>
#include <algorithm>

int shredule(const std::vector<std::pair<int, int>>& tasks) {
    std::vector<std::pair<int, int>> sorted_tasks = tasks;
    std::sort(sorted_tasks.begin(), sorted_tasks.end(), [](const std::pair<int, int>& a, const std::pair<int, int>& b) {
        return a.second < b.second;
    });

    std::vector<std::pair<int, int>> res;
    int begin = 8;
    int current_end = begin;
    int end = 17;

    for (const auto& task : sorted_tasks) {
        if (!(begin <= task.first && task.first < end && begin < task.second && task.second <= end)) {
            continue;
        }
        if (task.first >= current_end) {
            res.push_back(task);
            current_end = task.second;
        }
    }

    return res.size();
}

int main() {
    int n;
    std::cin >> n;
    std::vector<std::pair<int, int>> tasks;
    for (int i = 0; i < n; ++ i) {
        int start, finish;
        char comma;
        std::cin >> start >> comma >> finish;
        tasks.push_back(std::make_pair(start, finish));
    }

    std::cout << shredule(tasks) << std::endl;

    return 0;
}

