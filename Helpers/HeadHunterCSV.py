import json
import pandas as pd
import requests

requests.packages.urllib3.util.connection.HAS_IPV6 = False


class HeadHunterRequester:
    """
    Класс, позволяющий получить выгрузку данных из HH за интересующую дату
    """
    def __init__(self, date: list[int]):
        """
        Инициализирует объект HeadHunterRequester
        :param date: Дата для поиска ваканский
        """
        self.__find_fields = ['name', 'salary', 'area', 'published_at']
        self.__table_fields = ['name', 'salary_from', 'salary_to', 'salary_currency', 'area_name', 'published_at']
        self.__timestamps = [('T00:00:00', 'T06:00:00'), ('T06:00:00', 'T12:00:00'),
                             ('T12:00:00', 'T18:00:00'), ('T18:00:00', 'T23:59:59')]
        self.__last_data = []
        self.__params = {
            'date_from': f'{date[0]}-{date[1]}-{date[2]}',
            'date_to': f'{date[0]}-{date[1]}-{date[2] + 1}',
        }
        self.vacancies = []

    def queryVacanciesDataByUrl(self, url: str) -> dict:
        """
        Выполняет GET-запрос и возвращает декодированные JSON-данные
        :param url: URL-адрес
        :return: dict
        """
        try:
            response = requests.get(url, timeout=5)
        except Exception:
            print('Произошла непредвиденная ошибка!')
            exit()
        return json.loads(response.content.decode())

    def getVacanciesResponses(self) -> list:
        """
        Получает все ответы от сервера с учётом запросов по промежуткам времени
        :return: Список ответов сервера
        """
        responses = []
        for pair in self.__timestamps:
            url = f'https://api.hh.ru/vacancies?specialization=1&per_page=100&page=1&date_from={self.__params["date_from"] + pair[0]}&date_to={self.__params["date_from"] + pair[1]}'
            response = self.queryVacanciesDataByUrl(url)
            response_data = response['items']
            pages = response['pages']
            for page in range(1, pages + 1):
                url = f'https://api.hh.ru/vacancies?specialization=1&per_page=100&page={page}&date_from={self.__params["date_from"] + pair[0]}&date_to={self.__params["date_from"] + pair[1]}'
                response = self.queryVacanciesDataByUrl(url)
                response_data = response['items']
                responses.append(response_data)
        return responses

    def createDataFromResponse(self, response_data: dict):
        """
        Формирует данные для выгрузки в CSV из ответов от сервера
        :param response_data: Данные от сервера в формате dict
        :return: Список с данными о вакансиях, выданных сервером по запросу
        """
        vacancies_data = []
        for elem in response_data:
            vacancy_data = []
            for key in self.__find_fields:
                if key == 'area':
                    vacancy_data.append(elem[key]['name'])
                elif key == 'salary':
                    if not elem[key]:
                        vacancy_data += ['', '', '']
                    else:
                        vacancy_data += [elem[key]['from'], elem[key]['to'], elem[key]['currency']]
                else:
                    vacancy_data.append(elem[key])
            vacancies_data.append(vacancy_data)
        return vacancies_data

    def createCSVFile(self, vacancies_data: list) -> None:
        """
        Создаёт CSV-файл по списку данных о ваканскиях
        :param vacancies_data: Данные о вакансии list
        :return: None
        """
        df = pd.DataFrame(vacancies_data, columns=self.__table_fields)
        df.to_csv('HHVacancies.csv', index=False)


a = HeadHunterRequester([2022, 11, 22])
responses = a.getVacanciesResponses()
res = []
for resp in responses:
    res += a.createDataFromResponse(resp)
a.createCSVFile(res)
