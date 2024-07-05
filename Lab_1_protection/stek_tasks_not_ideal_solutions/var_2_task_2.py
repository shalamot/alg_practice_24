sym = input()
sym_del_amount = int(input())
string = input()

i = 0
while sym in string:
    if string[i] == sym:
        if i - sym_del_amount < 0:
            string = string[:i] + string[i + 1:]
        else:
            string = string[:i - sym_del_amount] + string[i - sym_del_amount:i][::-1] + string[i + 1:]
        i -= 1

    i += 1

print(string)


"""
#include <iostream>
#include <string>
#include <algorithm> // для std::reverse

int main() {
    char sym;
    int sym_del_amount;
    std::string input_str;

    std::cin >> sym;
    std::cin >> sym_del_amount;
    std::cin.ignore(); // Игнорируем оставшийся символ новой строки после чтения int
    std::getline(std::cin, input_str);

    size_t i = 0;
    while (input_str.find(sym) != std::string::npos) {
        if (input_str[i] == sym) {
            if (i < sym_del_amount) {
                input_str = input_str.substr(0, i) + input_str.substr(i + 1);
            } else {
                std::string reversed_substr = input_str.substr(i - sym_del_amount, sym_del_amount);
                std::reverse(reversed_substr.begin(), reversed_substr.end());
                input_str = input_str.substr(0, i - sym_del_amount) + reversed_substr + input_str.substr(i + 1);
            }
            i--;
        }
        i++;
    }

    std::cout << input_str << std::endl;

    return 0;
}
"""