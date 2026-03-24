import pytest
from myproject.main import greet


def test_greet_returns_greeting():
    assert greet("World") == "Hello, World!"


def test_greet_with_name():
    assert greet("Alice") == "Hello, Alice!"
