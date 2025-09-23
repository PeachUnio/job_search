from abc import ABC, abstractmethod

import requests


class BasicAPI(ABC):
    """Базовый класс для работы с API сервиса с вакансиями"""

    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def load_vacancies(self, keyword):
        pass


class HhAPI(BasicAPI):
    """
    Класс для работы с API HeadHunter
    Класс Parser является родительским классом, который вам необходимо реализовать
    """

    def __init__(self):
        self.url = "https://api.hh.ru/vacancies"
        self.headers = {"User-Agent": "HH-User-Agent"}
        self.params = {"text": "", "page": 0, "per_page": 100}
        HhAPI.vacancies = []

    @classmethod
    def load_in_class(cls, vac_list):
        return cls.vacancies.extend(vac_list)

    @classmethod
    def delete_all_vacancies(cls):
        cls.vacancies = []

    def load_vacancies(self, keyword):
        """Поиск вакансий по ключевому слову"""
        self.params["text"] = keyword
        self.params["page"] = 0
        all_vacancies = []

        for page in range(20):
            self.params["page"] = page
            try:
                response = requests.get(self.url, headers=self.headers, params=self.params)
                response.raise_for_status()

                data = response.json()
                vacancies = data.get("items", [])
                all_vacancies.extend(vacancies)
                self.load_in_class(all_vacancies)

                if page >= data.get("pages", 0) - 1:
                    break
            except requests.exceptions.RequestException as e:
                print(f"Ошибка при запросе к API: {e}")
                break
            except ValueError as e:
                print(f"Ошибка с JSON: {e}")
                break
        return all_vacancies

    def sorted_by_salary(self):
        pass

