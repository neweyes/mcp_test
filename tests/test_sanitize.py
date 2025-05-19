import pytest
from utils.sanitize import sanitize_filename

def test_sanitize_filename():
    assert sanitize_filename('abc') == 'abc'
    assert sanitize_filename('a/b:c*?"<>|') == 'a_b_c_______'
    assert sanitize_filename('hello world') == 'hello world'
