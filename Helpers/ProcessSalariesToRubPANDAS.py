import pandas as pd


class ProcessSalaries:
    def __init__(self, file_name: str) -> None:
        """
        Инициализирует объект ProcessSalaries
        :param file_name: Имя файла для обработки
        """
        self.__file_name = file_name
        self.__currencies = pd.read_csv('../currency.csv')
        self.__available_currencies = list(self.__currencies.keys()[2:])

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
            multiplier = self.__currencies[self.__currencies['date'] == date][salary_currency].iat[0]
            salary *= multiplier
        return salary

    def process_salaries(self) -> None:
        """
        Обрабатывает зарплаты, переводя в рубли в соответствии с нужным курсом. Удаляет строки,
         в которых невозможно посчитать зарплату. Сохраняет в формате CSV
        :return: None
        """
        df = pd.read_csv(self.__file_name)
        df['salary'] = df[['salary_from', 'salary_to', 'salary_currency', 'published_at']].apply(self.get_salary, axis=1)
        df.drop(labels=['salary_to', 'salary_from', 'salary_currency'], axis=1, inplace=True)
        df = df.loc[df['salary'] != 'nan']
        df.head(100).to_csv('top100_2.csv', index=False)


ProcessSalaries('../vacancies_dif_currencies.csv').process_salaries()
