from statistics import Vacancy
import unittest


class TestVacancy(unittest.TestCase):
    def setUp(self) -> None:
        self.vacancy = Vacancy({'name': 'Программист', 'salary_from': 50000, 'salary_to': 100000, 'salary_currency': 'RUR',
                        'area_name': 'Екатеринбург', 'published_at': '2007-12-03T17:34:36+0300'})

    def tearDown(self) -> None:
        self.vacancy = Vacancy(
            {'name': 'Программист', 'salary_from': 50000, 'salary_to': 100000, 'salary_currency': 'RUR',
             'area_name': 'Екатеринбург', 'published_at': '2007-12-03T17:34:36+0300'})

    def test_name(self):
        self.assertEqual(self.vacancy.name, 'Программист')

    def test_salary_from(self):
        self.assertEqual(self.vacancy.salary_from, 50000)

    def test_salary_to(self):
        self.assertEqual(self.vacancy.salary_to, 100000)

    def test_salary_average(self):
        self.assertEqual(self.vacancy.salary_average, 75000)

    def test_salary_average_double(self):
        self.vacancy = Vacancy(
            {'name': 'Программист', 'salary_from': 49455.50, 'salary_to': 100000, 'salary_currency': 'RUR',
             'area_name': 'Екатеринбург', 'published_at': '2007-12-03T17:34:36+0300'})
        self.assertEqual(self.vacancy.salary_average, 74727.50)

    def test_salary_year(self):
        self.assertEqual(self.vacancy.year, 2007)
