import os.path
import unittest

from statistics import Report


class TestReport(unittest.TestCase):
    def setUp(self) -> None:
        self.report = Report("Аналитик", {2007: 40000, 2008: 50000}, {2007: 200, 2008: 205},
                             {"Аналитик": 20000, "Программист": 40000}, {"Аналитик": 200, "Программист": 400},
                             {"Москва": 50000, "Екатеринбург": 40000}, {"Москва": 0.4, "Екатеринбург": 0.6})

    def test_wb(self):
        self.assertEqual(type(self.report.wb).__name__, "Workbook")

    def test_vacancy_name(self):
        self.assertEqual(self.report.vacancy_name, "Аналитик")

    def test_salary_by_year(self):
        self.assertEqual(self.report.salary_by_year[2007], 40000)

    def test_vacs_per_year(self):
        self.assertEqual(self.report.vacs_per_year[2008], 205)

    def test_salary_by_vac(self):
        self.assertEqual(self.report.salary_by_vac["Аналитик"], 20000)

    def test_count_by_vac(self):
        self.assertEqual(self.report.count_by_vac["Программист"], 400)

    def test_salary_by_city(self):
        self.assertEqual(self.report.salary_by_city["Екатеринбург"], 40000)

    def test_city_percents(self):
        self.assertEqual(self.report.city_percents["Москва"], 0.4)
