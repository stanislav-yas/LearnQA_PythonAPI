import pytest

def test_check_phrase_length():
    phrase = input("Введите фразу, короче 15 символов: ")
    assert len(phrase) < 15, f"Длина фразы '{phrase}' больше 15 символов"
 