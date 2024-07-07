#include <iostream>
#include <vector>
#include <algorithm>
#include <sstream>

int coin_change(std::vector<int>& coins, int amount) {
    std::sort(coins.begin(), coins.end(), std::greater<int>());
    std::vector<int> result;
    for (int coin : coins) {
        while (amount >= coin) {
            amount -= coin;
            result.push_back(coin);
        }
    }
    return result.size();
}

int main() {
    int amount;
    std::cin >> amount;
    std::cin.ignore();

    std::string input;
    std::getline(std::cin, input);
    
    std::vector<int> coins;
    std::stringstream ss(input);
    int coin;
    while (ss >> coin) {
        coins.push_back(coin);
        if (ss.peek() == ',') {
            ss.ignore();
        }
    }

    int result = coin_change(coins, amount);
    std::cout << result << std::endl;

    return 0;
}

