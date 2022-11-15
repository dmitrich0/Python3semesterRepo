import csv


class Vacancy:
    currency_to_rub = {
        "AZN": 35.68,
        "BYR": 23.91,
        "EUR": 59.90,
        "GEL": 21.74,
        "KGS": 0.76,
        "KZT": 0.13,
        "RUR": 1,
        "UAH": 1.64,
        "USD": 60.66,
        "UZS": 0.0055
    }

    def __init__(self, vacancy):
        self.name = vacancy['name']
        self.salary_from = int(float(vacancy['salary_from']))
        self.salary_to = int(float(vacancy['salary_to']))
        self.salary_currency = vacancy['salary_currency']
        self.salary_average = self.currency_to_rub[self.salary_currency] * (self.salary_from + self.salary_to) / 2
        self.area_name = vacancy['area_name']
        self.year = int(vacancy['published_at'][:4])


class DataSet:
    def __init__(self, file_name, vacancy_name):
        self.file_name = file_name
        self.vacancy_name = vacancy_name

    def csv_reader(self):
        titles = []
        salary = {}
        num_of_vacancies = {}
        vacancy_salary_name = {}
        vacancies_number_of_vacancy_name = {}
        salary_city = {}
        salary_number = {}
        count_of_vacancies = 0
        with open(self.file_name, mode='r', encoding='utf-8-sig') as file:
            reader = csv.reader(file)
            for index, row in enumerate(reader):
                if index == 0:
                    titles = row
                    csv_header_length = len(row)
                elif '' not in row and len(row) == csv_header_length:
                    vacancy = Vacancy(dict(zip(titles, row)))
                    if vacancy.year not in salary:
                        salary[vacancy.year] = [vacancy.salary_average]
                    else:
                        salary[vacancy.year].append(vacancy.salary_average)
                    if vacancy.year not in num_of_vacancies:
                        num_of_vacancies[vacancy.year] = 1
                    else:
                        num_of_vacancies[vacancy.year] += 1
                    if vacancy.name.find(self.vacancy_name) != -1:
                        if vacancy.year not in vacancy_salary_name:
                            vacancy_salary_name[vacancy.year] = [vacancy.salary_average]
                        else:
                            vacancy_salary_name[vacancy.year].append(vacancy.salary_average)
                        if vacancy.year not in vacancies_number_of_vacancy_name:
                            vacancies_number_of_vacancy_name[vacancy.year] = 1
                        else:
                            vacancies_number_of_vacancy_name[vacancy.year] += 1
                    if vacancy.area_name not in salary_city:
                        salary_city[vacancy.area_name] = [vacancy.salary_average]
                    else:
                        salary_city[vacancy.area_name].append(vacancy.salary_average)
                    if vacancy.area_name not in salary_number:
                        salary_number[vacancy.area_name] = 1
                    else:
                        salary_number[vacancy.area_name] += 1
                    count_of_vacancies += 1
        if not vacancy_salary_name:
            vacancy_salary_name = salary.copy()
            vacancy_salary_name = dict([(key, []) for key, value in vacancy_salary_name.items()])
            vacancies_number_of_vacancy_name = num_of_vacancies.copy()
            vacancies_number_of_vacancy_name = \
                dict([(key, 0) for key, value in vacancies_number_of_vacancy_name.items()])
        stats = {}
        stats2 = {}
        stats3 = {}
        stats4 = {}
        for year, list_of_salaries in salary.items():
            stats[year] = int(sum(list_of_salaries) / len(list_of_salaries))
        for year, list_of_salaries in vacancy_salary_name.items():
            if len(list_of_salaries) == 0:
                stats2[year] = 0
            else:
                stats2[year] = int(sum(list_of_salaries) / len(list_of_salaries))
        for year, list_of_salaries in salary_city.items():
            stats3[year] = int(sum(list_of_salaries) / len(list_of_salaries))
        for year, list_of_salaries in salary_number.items():
            stats4[year] = round(list_of_salaries / count_of_vacancies, 4)
        stats4 = list(filter(lambda a: a[-1] >= 0.01, [(key, value) for key, value in stats4.items()]))
        stats4.sort(key=lambda a: a[-1], reverse=True)
        stats5 = stats4.copy()
        stats4 = dict(stats4)
        stats3 = list(filter(lambda a: a[0] in list(stats4.keys()), [(key, value) for key, value in stats3.items()]))
        stats3.sort(key=lambda a: a[-1], reverse=True)
        stats3 = dict(stats3[:10])
        print(f'Динамика уровня зарплат по годам: {str(stats)}')
        print(f'Динамика количества вакансий по годам: {str(num_of_vacancies)}')
        print(f'Динамика уровня зарплат по годам для выбранной профессии: {str(stats2)}')
        print(f'Динамика количества вакансий по годам для выбранной профессии: {str(vacancies_number_of_vacancy_name)}')
        print(f'Уровень зарплат по городам (в порядке убывания): {str(stats3)}')
        print(f'Доля вакансий по городам (в порядке убывания): {str(dict(stats5[:10]))}')


class InputConnect:
    def __init__(self):
        self.file_name = input('Введите название файла: ')
        self.vacancy_name = input('Введите название профессии: ')
        data_set = DataSet(self.file_name, self.vacancy_name)
        data_set.csv_reader()


if __name__ == '__main__':
    InputConnect()
