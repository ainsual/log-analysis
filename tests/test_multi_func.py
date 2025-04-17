import pytest

from src.multi_func import get_data_multi
from test_app import sample_log_files

def test_get_data_multi(sample_log_files):
    paths = sample_log_files
    result = get_data_multi(paths)

    assert isinstance(result, dict)
    assert "/api/v1/users/" in result
    assert result["/api/v1/users/"]["INFO"] == 1
    assert "/api/v1/auth/" in result
    assert result["/api/v1/auth/"]["ERROR"] == 1