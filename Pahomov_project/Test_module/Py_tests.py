from Prog import divide


def test_division_by_zero():
    assert divide(10, 0) == None


def test_division_positive():
    assert divide(10, 2) == 5


def test_division_negative():
    assert divide(10, -2) == -5
