TEST(FooTest, DivisionByZero) {
    EXPECT_EQ(foo(0), -1);
}

TEST(FooTest, DivisionPositiveThree) {
    EXPECT_EQ(foo(3), -1);
}

TEST(FooTest, DivisionPositiveSix) {
    EXPECT_EQ(foo(6), -1);
}

TEST(FooTest, NegativeValue) {
    EXPECT_EQ(foo(-3), -1);
}

int main(int argc, char **argv) {
    ::testing::InitGoogleTest(&argc, argv);
    return RUN_ALL_TESTS();
}