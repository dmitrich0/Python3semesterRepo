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

    def process_salaries(self) -> None:
        """
        Обрабатывает зарплаты, переводя в рубли в соответствии с нужным курсом. Сохраняет в формате CSV
        :return: None
        """
        salaries = []
        to_delete = []
        df = pd.read_csv(self.__file_name)
        for row in df.itertuples():
            salary_from = str(row[2])
            salary_to = str(row[3])
            if salary_from != 'nan' and salary_to != 'nan':
                salary = float(salary_from) + float(salary_to)
            elif salary_from != 'nan' and salary_to == 'nan':
                salary = float(salary_from)
            elif salary_from == 'nan' and salary_to != 'nan':
                salary = float(salary_to)
            else:
                to_delete.append(int(row[0]))
                continue
            if row[4] == 'nan' or row[4] not in self.__available_currencies:
                to_delete.append(int(row[0]))
                continue
            if row[4] != 'RUR':
                date = row[6][:7]
                multiplier = self.__currencies[self.__currencies['date'] == date][row[4]].iat[0]
                salary *= multiplier
            salaries.append(salary)
        df.drop(labels=to_delete, axis=0, inplace=True)
        df.drop(labels=['salary_to', 'salary_from', 'salary_currency'], axis=1, inplace=True)
        df['salary'] = salaries
        df.to_csv('1.csv')


a = ProcessSalaries('../vacancies_dif_currencies.csv').process_salaries()
