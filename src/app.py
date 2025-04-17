from collections import defaultdict

from typing import List, Pattern, DefaultDict, Dict

import re

import pandas as pd

def get_data(paths: List[str]) -> Dict[str, Dict[str, int]]:
    pattern: Pattern[str] = re.compile(
        r'^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d{3} (DEBUG|INFO|WARNING|ERROR|CRITICAL) django\.request: [^/]*(\/\S+)'
    )

    # создаём словарь DefaultDict{'url': {'log_method': count}}
    data: DefaultDict[str, Dict[str, int]] = defaultdict(
        lambda: defaultdict(int)
    )

    for path in paths:
        try:
            with open(path, 'r', encoding='utf-8') as log_file:
                for line in log_file:
                    match = pattern.match(line)
                    if match:
                        log_method, url = match.groups()
                        data[url][log_method] += 1

        except FileNotFoundError:
            print(f'Файл с путем {path} не был найден')
            continue

    result: Dict[str, Dict[str, int]] = {
        url: dict(methods)
        for url, methods in sorted(data.items(), key=lambda x: x[0])
    }

    return result



def create_report(paths: List[str], title:str, func=get_data) -> None:
    data = func(paths)
    all_log_levels = ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']
    count_all_request = 0

    count_all_methods = {
        log_method: 0
        for log_method in all_log_levels
    }

    # Преобразуем данные в список списков для DataFrame
    table_data = []
    index = []  # Список для хранения URL, которые будут индексом

    for handler, log_counts in data.items():
        row = []
        for level in all_log_levels:
            count = log_counts.get(level, 0)
            row.append(count)
            count_all_methods[level] += count
            count_all_request += count
        table_data.append(row)
        index.append(handler)

    index.append('TOTAL')
    table_data.append(count_all_methods.values())
    # создаем DataFrame
    df = pd.DataFrame(table_data, index=index, columns=all_log_levels)
    df.index.name = title
    print(f'Total request: {count_all_request}')
    print(df)