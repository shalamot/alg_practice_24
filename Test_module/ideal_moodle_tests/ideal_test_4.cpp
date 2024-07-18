TEST(TestFoo, InvalidDay) {
    EXPECT_EQ(foo("31.12.2022"), false);
}

TEST(TestFoo, InvalidMonth) {
    EXPECT_EQ(foo("1.0.2022"), false);
}

TEST(TestFoo, InvalidYear) {
    EXPECT_EQ(foo("20.1.1999"), false);
}

TEST(TestFoo, LeapYear) {
    EXPECT_EQ(foo("20.1.2024"), false);
}

TEST(TestFoo, July13th) {
    EXPECT_EQ(foo("13.7.2021"), false);
}

int main(int argc, char **argv) {
    ::testing::InitGoogleTest(&argc, argv);
    return RUN_ALL_TESTS();
}
