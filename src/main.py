import argparse
from datetime import datetime

from app import create_report
from multi_func import get_data_multi


def main():
    parser = argparse.ArgumentParser(description='Обработка лог-файлов и генерация отчетов.')
    parser.add_argument('log_files',
                        nargs='+',
                        help='Пути к лог-файлам.'
                        )
    parser.add_argument('--report',
                        default=f"handler_{datetime.now().strftime('%Y_%m_%d_%H_%M')}",
                        help='Тип отчета для генерации: handlers.'
                        )
    args = parser.parse_args()
    create_report(args.log_files, args.report)
    create_report(args.log_files, args.report, func=get_data_multi)

if __name__ == "__main__":
    main()