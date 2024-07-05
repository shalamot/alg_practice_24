#include <gtest/gtest.h>

TEST(FooTest, HandlesNegativeThree) {
    EXPECT_DOUBLE_EQ(foo(-3), -1);
}

TEST(FooTest, HandlesNegativeOne) {
    EXPECT_DOUBLE_EQ(foo(-1), -1);
}

int main(int argc, char **argv) {
    ::testing::InitGoogleTest(&argc, argv);
    return RUN_ALL_TESTS();
}