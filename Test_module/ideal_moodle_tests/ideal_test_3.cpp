TEST(FooTest, ZeroIndex) {
    EXPECT_EQ(foo(0), false);
}

TEST(FooTest, NegativeIndex) {
    EXPECT_EQ(foo(-2), false);
}

TEST(FooTest, OutOfBoundsIndex) {
    EXPECT_EQ(foo(100), false);
}

TEST(FooTest, ValidIndex) {
    EXPECT_EQ(foo(4), true);
}

int main(int argc, char **argv) {
    ::testing::InitGoogleTest(&argc, argv);
    return RUN_ALL_TESTS();
}