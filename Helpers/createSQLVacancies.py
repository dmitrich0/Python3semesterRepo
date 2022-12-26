import pandas as pd
import sqlite3


class ProcessSalaries:
    def __init__(self, file_name: str) -> None:
        """
        Инициализирует объект ProcessSalaries
        :param file_name: Имя файла для обработки
        """
        self.__con = sqlite3.connect("currencies_db.sqlite")
        self.__file_name = file_name
        self.__available_currencies = list(pd.read_sql("SELECT * from currencies WHERE date='2003-01'",
                                                       self.__con).keys()[1:])

    def get_salary(self, row: pd.DataFrame) -> float or str:
        """
        Генерирует одну зарплату по данным из каждого ряда
        :param row: Текущий ряд
        :return: salary(float) or 'nan'
        """
        salary_from, salary_to, salary_currency, published_at = str(row[0]), str(row[1]), str(row[2]), str(row[3])
        if salary_currency == 'nan':
            return 'nan'
        if salary_from != 'nan' and salary_to != 'nan':
            salary = float(salary_from) + float(salary_to)
        elif salary_from != 'nan' and salary_to == 'nan':
            salary = float(salary_from)
        elif salary_from == 'nan' and salary_to != 'nan':
            salary = float(salary_to)
        else:
            return 'nan'
        if salary_currency != 'RUR' and salary_currency in self.__available_currencies:
            date = published_at[:7]
            multi = pd.read_sql(f"SELECT {salary_currency} from currencies WHERE date='{date}'",
                                self.__con)[f'{salary_currency}'][0]
            if multi is not None:
                salary *= multi
            else:
                return 'nan'
        return round(salary)

    def process_salaries(self) -> None:
        """
        Обрабатывает зарплаты, переводя в рубли в соответствии с нужным курсом. Удаляет строки,
         в которых невозможно посчитать зарплату. Сохраняет в формате CSV
        :return: None
        """
        df = pd.read_csv(self.__file_name)
        df['salary'] = df[['salary_from', 'salary_to', 'salary_currency', 'published_at']].apply(self.get_salary, axis=1)
        df['published_at'] = df['published_at'].apply(lambda x: x[:7])
        df.drop(labels=['salary_to', 'salary_from', 'salary_currency'], axis=1, inplace=True)
        df = df.loc[df['salary'] != 'nan']
        df.to_csv('all.csv', index=False)

    def CSV_to_sqlite_vacancies(self, file_name: str) -> None:
        """
        Преобразует CSV-файл с обработанными вакансиями в БД
        :param file_name: имя файла с обработанными вакансиями
        :return: None
        """
        df = pd.read_csv(file_name)
        conn = sqlite3.connect('all_vacancies')
        c = conn.cursor()
        c.execute('CREATE TABLE IF NOT EXISTS all_vacancies (name text, area_name text, published_at text, salary number)')
        conn.commit()
        df.to_sql('all_vacancies', conn, if_exists='replace', index=False)


processor = ProcessSalaries('../vacancies_dif_currencies.csv')
processor.process_salaries()
processor.CSV_to_sqlite_vacancies('all.csv')
