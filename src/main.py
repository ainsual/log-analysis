import argparse
from datetime import datetime

from app import create_report


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

if __name__ == "__main__":
    main()