import pytest
from analyzer import validate_text, ValidationError


@pytest.mark.parametrize("text", ["", " ", "hello", "слово a", "слово 5"])
def test_invalid(text):
    with pytest.raises(ValidationError):
        validate_text(text)

def test_valid():
    assert validate_text(" книга ") == "книга"