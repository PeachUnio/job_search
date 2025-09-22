from abc import ABC, abstractmethod
from src.vacancies import Vacancy
import os
import json

class BaseLoad(ABC):
    """Базовый класс для загрузки вакансий"""

    @abstractmethod
    def load_vac(self):
        pass

    @abstractmethod
    def get_vac(self):
        pass

    @abstractmethod
    def clean_vac(self):
        pass

    @abstractmethod
    def clean_all(self):
        pass

class LoadVacancy(BaseLoad):
    """
    Загрузка и удаление вакансий в отдельный файл и удаление их из него.
    """

    def __init__(self, filename="vacancies.json"):
        self.filename = filename
        self.check_exist_file()

    def check_exist_file(self):
        """Создает файл если его не существует"""
        if not os.path.exists(self.filename):
            with open(self.filename, "w", encoding="utf-8") as f:
                json.dump([], f)

    def load_vac(self, vacancy):
        """Функция, которая загружает вакансии в файл если их там нет"""
        if isinstance(vacancy, Vacancy):
            salary = f'{vacancy.salary_from}-{vacancy.salary_to}'
            vacancy_dict = {
                'name': vacancy.name,
                'link': vacancy.link,
                'description': vacancy.description,
                'salary': salary,
                'address': vacancy.address
            }
            self.check_exist_file()

            with open(self.filename, "r", encoding="utf-8") as f:
                all_data = json.load(f)

            vac_exist = any(vac.get('name') == vacancy_dict['name'] and
                            vac.get('link') == vacancy_dict['link']
                            for vac in all_data)
            if not vac_exist:
                all_data.append(vacancy_dict)
                with open(self.filename, "w", encoding="utf-8") as f:
                    json.dump(all_data, f, ensure_ascii=False, indent=2)

        else:
            raise TypeError

    def get_vacancies(self, criteria):
        """Получить вакансии по критериям файла"""
        with open(self.filename, 'r', encoding='utf-8') as f:
            data = json.load(f)

        filtered_vacancies = []
        for item in data:
            match = True
            for key, value in criteria.items():
                if key not in item or item[key] != value:
                    match = False
                    break
            if match:
                salary_from, salary_to = item['salary'].split("-")
                dict_vacancy = Vacancy(name=item['name'],
                                       link=item['link'],
                                       description=item['description'],
                                       salary_from=salary_from,
                                       salary_to=salary_to,
                                       address=item['address'])
                filtered_vacancies.append(dict_vacancy)

        return filtered_vacancies

    def clear_all(self):
        """Очистить все вакансии из JSON-файла"""
        with open(self.filename, 'w', encoding='utf-8') as f:
            json.dump([], f, ensure_ascii=False, indent=2)
