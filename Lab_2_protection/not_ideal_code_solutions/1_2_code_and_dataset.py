
'''
info = [input().split() for _ in range(int(input()))]
books = [tuple([el[0], int(el[1])]) for el in info]

# Сортировка списка книг
sorted_books = sorted(books, key=lambda book: (book[1], book[0]))

# Вывод результата
for title, year in sorted_books:
    print(f"{title} {year}")
'''


'''
#include <iostream>
#include <vector>
#include <string>
#include <algorithm>

// Структура для представления книги
struct Book {
    std::string title;
    int year;
};

// Функция сравнения для сортировки
bool compareBooks(const Book& a, const Book& b) {
    if (a.year == b.year) {
        return a.title < b.title;
    }
    return a.year < b.year;
}

int main() {
    int n;
    std::cin >> n;
    std::vector<Book> books(n);

    // Ввод данных о книгах
    for (int i = 0; i < n; ++i) {
        std::cin >> books[i].title >> books[i].year;
    }

    // Сортировка списка книг
    std::sort(books.begin(), books.end(), compareBooks);

    // Вывод результата
    for (const auto& book : books) {
        std::cout << book.title << " " << book.year << std::endl;
    }

    return 0;
}
'''


'''
# moodle code style

def foo(dataset):
    info = dataset.split('\n')[1:len(dataset) - 1]
    info = [el.split() for el in info][:-1]
    books = [tuple([el[0], int(el[1])]) for el in info]
    answ = ''

    # Сортировка списка книг
    sorted_books = sorted(books, key=lambda book: (book[1], book[0]))

    # Вывод результата
    for title, year in sorted_books:
        answ = answ + f"{title} {year}" + '\n'

    return answ

print(foo("4\nBrave_New_World 1932\nWuthering_Heights 1847\nThe_Great_Gatsby 1925\nThe_Catcher_in_the_Rye 1951\n"))
'''


'''
========================================
1)
4
Brave_New_World 1932
Wuthering_Heights 1847
The_Great_Gatsby 1925
The_Catcher_in_the_Rye 1951


Wuthering_Heights 1847
The_Great_Gatsby 1925
Brave_New_World 1932
The_Catcher_in_the_Rye 1951
========================================

========================================
2)
4
Book_C 1950
Book_A 1950
Book_B 1950
Book_D 1950


Book_A 1950
Book_B 1950
Book_C 1950
Book_D 1950
========================================

========================================
3)
4
Same_Title 1960
Same_Title 1970
Same_Title 1950
Same_Title 1980


Same_Title 1950
Same_Title 1960
Same_Title 1970
Same_Title 1980
========================================

========================================
4)
4
Book_One 2000
Book_Two 1999
Book_Three 2000
Book_Four 1998


Book_Four 1998
Book_Two 1999
Book_One 2000
Book_Three 2000
========================================

========================================
5)
4
Book_One 2000
Book_Two 1999
Book_Three 2000
Book_Four 1998


Book_Four 1998
Book_Two 1999
Book_One 2000
Book_Three 2000
========================================
'''