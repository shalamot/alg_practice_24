#include <gtest/gtest.h>


// Тест для проверки недопустимого значения 0
TEST(FooTest, DivisionByZero) {
    EXPECT_EQ(foo(0), -1);
}

// Тест для проверки недопустимого значения 3
TEST(FooTest, DivisionPositiveThree) {
    EXPECT_EQ(foo(3), -1);
}

// Тест для проверки недопустимого значения 6
TEST(FooTest, DivisionPositiveSix) {
    EXPECT_EQ(foo(6), -1);
}

// Тест для проверки недопустимого значения -3
TEST(FooTest, NegativeValue) {
    EXPECT_EQ(foo(-3), -1);
}

int main(int argc, char **argv) {
    ::testing::InitGoogleTest(&argc, argv);
    return RUN_ALL_TESTS();
}