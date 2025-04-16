import tempfile
from pathlib import Path

import pytest

from src.app import get_data, create_report


@pytest.fixture
def sample_log_files():
    """Создаем временные лог-файлы для тестирования"""
    with tempfile.TemporaryDirectory() as tmp_dir:
        log1 = Path(tmp_dir) / "app1.log"
        log1.write_text("""2025-03-28 12:05:13,000 INFO django.request: GET /api/v1/users/ 200 OK
2025-03-28 12:05:14,000 ERROR django.request: POST /api/v1/auth/ 500 Error""")

        log2 = Path(tmp_dir) / "app2.log"
        log2.write_text(
            """2025-03-28 12:31:51,000 ERROR django.request: Internal Server Error: /api/v1/support/ [192.168.1.90]
            - SuspiciousOperation: Invalid HTTP_HOST header"""
                        )

        # Файл 3 - несуществующий
        yield [str(log1), str(log2), 'some.log']


def test_get_data_success(sample_log_files):
    """Тестируем корректную обработку логов"""
    existing_files = sample_log_files[:2]  # Берем только существующие файлы
    result = get_data(existing_files)

    assert isinstance(result, dict)
    assert "/api/v1/users/" in result
    assert result["/api/v1/users/"]["INFO"] == 1
    assert "/api/v1/auth/" in result
    assert result["/api/v1/auth/"]["ERROR"] == 1


def test_get_data_with_missing_file(sample_log_files, capsys):
    """Тестируем обработку отсутствующего файла"""
    result = get_data(sample_log_files)  # Последний файл не существует

    captured = capsys.readouterr()
    assert "не был найден" in captured.out
    assert isinstance(result, dict)

def test_get_data_log_file_not_found():
    """Тестируем возврат пустого словаря, если файл был не найден"""
    result = get_data(['some.log'])
    assert result == {}

def test_create_report(sample_log_files, capsys):
    """Тестируем создание репортов"""
    title = 'handler'
    create_report(sample_log_files, title)

    captured = capsys.readouterr()
    assert title in captured.out

