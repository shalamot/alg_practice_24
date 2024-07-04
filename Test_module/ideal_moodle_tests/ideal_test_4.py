import pytest

def test_1():
    assert foo("31.12.2022") == False

def test_2():
    assert foo("1.0.2022") == False

def test_3():
    assert foo("20.1.1999") == False

def test_4():
    assert foo("20.1.2024") == False

def test_5():
    assert foo("13.7.2021") == False