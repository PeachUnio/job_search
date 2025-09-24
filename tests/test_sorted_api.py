import unittest
from unittest.mock import patch, Mock
from src.API import HhAPI


class TestHhAPI(unittest.TestCase):

    def setUp(self):
        """Настройка тестовых данных"""
        self.api = HhAPI()


        self.test_vacancies = [
            {
                'name': 'Повар',
                'salary': {'from': 50000, 'to': 80000, 'currency': 'RUR'},
                'snippet': {
                    'requirement': 'Опыт работы поваром в ресторане',
                    'responsibility': 'Приготовление блюд русской кухни'
                }
            },
            {
                'name': 'Бариста',
                'salary': {'from': 30000, 'to': None, 'currency': 'RUR'},
                'snippet': {
                    'requirement': 'Знание кофейных напитков',
                    'responsibility': 'Приготовление кофе, обслуживание гостей'
                }
            },
            {
                'name': 'Уборщик',
                'salary': None,
                'snippet': {
                    'requirement': 'Ответственность',
                    'responsibility': 'Уборка помещений'
                }
            },
            {
                'name': 'Шеф-повар',
                'salary': {'from': None, 'to': 150000, 'currency': 'RUR'},
                'snippet': {
                    'requirement': 'Опыт управления кухней',
                    'responsibility': 'Управление персоналом, разработка меню'
                }
            }
        ]

        self.api.vacancies = self.test_vacancies

    def test_sorted_by_salary(self):
        """Тестирование сортировки по зарплате"""
        sorted_vacancies = self.api.sorted_by_salary()

        salaries = []
        for vac in sorted_vacancies:
            salary = vac.get('salary')
            if salary:
                salary_to = salary.get('to', 0) or 0
                salary_from = salary.get('from', 0) or 0
                max_salary = max(salary_to, salary_from)
                salaries.append(max_salary)
            else:
                salaries.append(0)

        self.assertEqual(salaries, sorted(salaries, reverse=True))
        self.assertEqual(len(sorted_vacancies), 4)



    def test_sorted_by_word_not_found(self):
        result = self.api.sorted_by_world("программист")
        self.assertEqual(len(result), 0)