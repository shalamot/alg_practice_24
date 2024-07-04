#include <gtest/gtest.h>

TEST(FooTest, DivisionByZero) {
    EXPECT_EQ(foo(0), -1);
}

TEST(FooTest, DivisionPositive) {
    EXPECT_EQ(foo(2), -1);
}

int main(int argc, char **argv) {
    ::testing::InitGoogleTest(&argc, argv);
    return RUN_ALL_TESTS();
}