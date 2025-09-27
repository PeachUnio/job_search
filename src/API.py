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
        self.vacancies = []

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

                if page >= data.get("pages", 0) - 1:
                    break
            except requests.exceptions.RequestException as e:
                print(f"Ошибка при запросе к API: {e}")
                break
            except ValueError as e:
                print(f"Ошибка с JSON: {e}")
                break
        self.vacancies = all_vacancies
        return all_vacancies

    def sorted_by_salary(self):
        """Метод для сортировки вакансий по зарплате"""

        def get_salary_value(vacancy):
            """Вспомогательная функция для получения числового значения зарплаты"""
            salary = vacancy.get("salary")

            if not salary:
                return 0

            salary_from = salary.get("from", 0) or 0
            salary_to = salary.get("to", 0) or 0

            if salary_to > 0:
                return salary_to
            elif salary_from > 0:
                return salary_from
            else:
                return 0

        sorted_vacancies = sorted(self.vacancies, key=get_salary_value, reverse=True)

        return sorted_vacancies

    def sorted_by_world(self, keyword):
        """Метод для сортировки вакансий по словам в описании"""
        keyword_lower = keyword.lower()

        def contains_keyword(vacancy):
            """Проверяет, содержится ли ключевое слово в вакансии"""

            snippet = vacancy.get("snippet", {})

            requirement = snippet.get("requirement")
            if requirement and keyword_lower in requirement.lower():
                return True

            responsibility = snippet.get("responsibility")
            if responsibility and keyword_lower in responsibility.lower():
                return True

            return False

        return [vacancy for vacancy in self.vacancies if contains_keyword(vacancy)]
