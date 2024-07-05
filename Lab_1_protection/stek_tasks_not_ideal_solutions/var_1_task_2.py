sym = input()
sym_del_amount = int(input())
string = input()

i = 0
while sym in string:
    if string[i] == sym:
        if i - sym_del_amount < 0:
            string = string[i + 1:]
            i = -1
        else:
            string = string[:i - sym_del_amount] + string[i + 1:]
            i = i - sym_del_amount - 1

    i += 1

print(string)


"""
#include <iostream>
#include <string>

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
                input_str = input_str.substr(i + 1);
                i = -1; // Устанавливаем i на -1, потому что он будет увеличен до 0 в конце цикла
            } else {
                input_str = input_str.substr(0, i - sym_del_amount) + input_str.substr(i + 1);
                i = i - sym_del_amount - 1;
            }
        }
        i++;
    }

    std::cout << input_str << std::endl;

    return 0;
}
"""