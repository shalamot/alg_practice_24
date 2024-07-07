#include <iostream>
#include <vector>
#include <algorithm>
#include <tuple>

using namespace std;

vector<pair<int, int>> maximize_loot(int capacity, const vector<pair<int, int>>& items) {
    vector<tuple<int, int, double>> items_with_ratio;
    for (const auto& item : items) {
        items_with_ratio.emplace_back(item.first, item.second, static_cast<double>(item.second) / item.first);
    }

    sort(items_with_ratio.begin(), items_with_ratio.end(), [](const auto& a, const auto& b) {
        return get<2>(a) > get<2>(b);
    });

    vector<pair<int, int>> loot;
    int current_weight = 0;
    int current_value = 0;

    for (const auto& item : items_with_ratio) {
        int weight = get<0>(item);
        int value = get<1>(item);
        // Add the item if it fits in the capacity
        if (current_weight + weight <= capacity) {
            loot.emplace_back(weight, value);
            current_weight += weight;
            current_value += value;
        }
    }

    return loot;
}


int main() {
    int capacity;
    cin >> capacity;
    int count_items;
    cin >> count_items;
    vector<pair<int, int>> items;
    for (int i = 0; i < count_items; ++i) {
        int weight, value;
        char comma;
        cin >> weight >> comma >> value;
        items.emplace_back(weight, value);
    }
    auto result = maximize_loot(capacity, items);
    int current_weight = 0;
    int current_value = 0;
    for (const auto& item : result) {
        int weight = item.first;
        int value = item.second;
        current_weight += weight;
        current_value += value;
    }
    cout << current_weight << " " << current_value << endl;
    return 0;
}

