def test_1():
    assert foo(0) == False

def test_2():
    assert foo(-2) == False

def test_3():
    assert foo(100) == False

def test_4():
    assert foo(4) == True