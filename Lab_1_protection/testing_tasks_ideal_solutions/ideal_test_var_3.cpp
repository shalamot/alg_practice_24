#include <gtest/gtest.h>

TEST(FooTest, HandlesNegativeThree) {
    EXPECT_DOUBLE_EQ(foo(7), -1);
}

TEST(FooTest, HandlesNegativeOne) {
    EXPECT_DOUBLE_EQ(foo(5), -1);
}

TEST(FooTest, HandlesNegativeOne) {
    EXPECT_DOUBLE_EQ(foo(5), -1);
}

TEST(FooTest, HandlesNegativeOne) {
    EXPECT_DOUBLE_EQ(foo(0), -1);
}

int main(int argc, char **argv) {
    ::testing::InitGoogleTest(&argc, argv);
    return RUN_ALL_TESTS();
}