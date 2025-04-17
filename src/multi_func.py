from collections import defaultdict

from typing import List, Pattern, DefaultDict, Dict

import re

import concurrent.futures
import threading

def get_data_multi(paths: List[str]) -> Dict[str, Dict[str, int]]:
    pattern: Pattern[str] = re.compile(
        r'^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d{3} (DEBUG|INFO|WARNING|ERROR|CRITICAL) django\.request: [^/]*(\/\S+)'
    )

    # создаём словарь DefaultDict{'url': {'log_method': count}}
    data: DefaultDict[str, Dict[str, int]] = defaultdict(
        lambda: defaultdict(int)
    )
    def process_file(path: str) -> Dict[str, Dict[str, int]]:
        local_data: DefaultDict[str, Dict[str, int]] = defaultdict(
            lambda: defaultdict(int)
        )
        try:
            with open(path, 'r', encoding='utf-8') as log_file:
                for line in log_file:
                    match = pattern.match(line)
                    if match:
                        log_method, url = match.groups()
                        local_data[url][log_method] += 1
        except FileNotFoundError:
            print(f'Файл с путем {path} не был найден')
            return {}

        return dict(local_data)

    '''Мультипоточность'''
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        results = executor.map(process_file, paths)

        for local_data in results:
            for url, methods in local_data.items():
                for method in methods:
                    data[url][method] += local_data[url][method]

    return dict(data)