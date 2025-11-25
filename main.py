import argparse  # для обработки аргументов командной строки
import csv       # для работы с CSV-файлами
from collections import defaultdict  # словарь с автоматическим созданием пустых списков
from tabulate import tabulate       # для красивого вывода таблиц в консоли

# Функция для чтения нескольких CSV-файлов
def read_csv_files(file_paths):
    data = []  # список, куда будут складываться все строки из всех файлов
    for file_path in file_paths:  # проходим по каждому пути к файлу
        # открываем файл в режиме чтения с правильной кодировкой
        with open(file_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)  # читаем CSV как словарь (ключи = заголовки)
            # добавляем все строки из текущего файла в общий список
            data.extend(row for row in reader)
    return data  # возвращаем объединённые данные всех файлов

# Функция для генерации отчёта по эффективности сотрудников
def generate_performance_report(data):
    performance_by_position = defaultdict(list)  # словарь: ключ = позиция, значение = список показателей performance

    # собираем показатели performance по каждой позиции
    for row in data:
        position = row['position']  # получаем позицию сотрудника
        performance = float(row['performance'])  # преобразуем строку в число
        performance_by_position[position].append(performance)  # добавляем показатель в список для позиции

    report = []  # список для итогового отчёта
    # считаем среднюю эффективность для каждой позиции
    for position, performances in performance_by_position.items():
        avg_performance = sum(performances) / len(performances)  # среднее арифметическое
        report.append((position, round(avg_performance, 2)))  # добавляем кортеж (позиция, среднее), округляем до 2 знаков

    # сортируем список по эффективности по убыванию
    report.sort(key=lambda x: x[1], reverse=True)
    return report  # возвращаем готовый отчёт

# Главная функция скрипта
def main():
    parser = argparse.ArgumentParser(description='Generate employee reports.')  # создаём парсер аргументов
    parser.add_argument('--files', nargs='+', required=True, help='CSV files with employee data')  # файлы CSV
    parser.add_argument('--report', required=True, choices=['performance'], help='Type of report')  # тип отчёта
    args = parser.parse_args()  # читаем аргументы командной строки

    data = read_csv_files(args.files)  # читаем данные из всех файлов

    # если выбран отчёт по эффективности
    if args.report == 'performance':
        report = generate_performance_report(data)  # генерируем отчёт
        # выводим отчёт в виде таблицы с индексами строк
        print(tabulate(report, headers=['position', 'performance'], showindex=True))


if __name__ == "__main__":
    main()