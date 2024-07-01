#include <gtest/gtest.h>
#include "Prog.cpp"

TEST(DivisionTest, DivisionByZero) {
    EXPECT_EQ(divide(10, 0), 0);
}

TEST(DivisionTest, DivisionPositive) {
    EXPECT_EQ(divide(10, 2), 5);
}

TEST(DivisionTest, DivisionNegative) {
    EXPECT_EQ(divide(10, -2), -5);
}
