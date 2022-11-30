import csv
from Helper import Helper
import pandas as pd


class CSVSplitterData:
    """
    Класс для представления данных в удобном формате для CSV Splitter'a

    Attributes:
        titles (list[str]): Заголовки CSV-файлов
        data: (dict[int, list]): Данные CSV-файлов по годам
    """
    def __init__(self, titles: list[str], data: dict[int, list]):
        self.titles = titles
        self.data = data


class CSVSplitter:
    """
    Класс для разделения файла с вакансиями по годам

    Attributes:
        file_name (str): Название файла(путь) относительно расположения скрипта
    """
    def __init__(self, file_name: str):
        self.__file_name = file_name

    def create_data(self) -> CSVSplitterData:
        """
        Создаёт данные для сплиттера

        :returns: CSVSplitterData
        """
        data = {}
        with open(self.__file_name, mode='r', encoding='utf-8-sig') as f:
            reader = csv.reader(f)
            titles = next(reader)
            titles_count = len(titles)
            for row in reader:
                if '' not in row and len(row) == titles_count:
                    row_year = Helper.parse_year_from_date_slice(row[-1])
                    if row_year not in data.keys():
                        data[row_year] = [row]
                    else:
                        data[row_year].append(row)
        return CSVSplitterData(titles, data)

    def create_files(self, data: CSVSplitterData) -> None:
        """
        Создаёт новые файлы из исходного

        :param data: Данные
        :returns: None
        """
        for key in data.data.keys():
            df = pd.DataFrame(data.data[key], columns=data.titles)
            df.to_csv(f'../CSVsByYears/{key}.csv', index=False)


splitter = CSVSplitter('../vacancies_by_year.csv')
data = splitter.create_data()
splitter.create_files(data)
