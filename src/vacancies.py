class Vacancy:
    """Класс для вакансий"""

    def __init__(self, name: str, link: str, description: str, salary_from: int, salary_to: int, address: str):
        self.name = name
        self.link = link
        self.description = description
        self.salary_from = salary_from
        self.salary_to = salary_to
        self.address = address

    def __str__(self):
        return f"Вакансия {self.name}\n{self.link}\nЗарплата {self.salary_from}-{self.salary_to} руб."

    def __gt__(self, other):
        if isinstance(other, Vacancy):
            if self.salary_from > 0 or other.salary_from > 0:
                if self.salary_to > other.salary_to:
                    return f"{self.name} зарабатывает больше чем {other.name}."
                else:
                    return f"{other.name} зарабатывает больше чем {self.name}."
            else:
                return "Зарплата не указана"
        else:
            raise TypeError

    def __eq__(self, other):
        if isinstance(other, Vacancy):
            if self.salary_from > 0 or other.salary_from > 0:
                if self.salary_to == other.salary_to:
                    return f"{self.name} и {other.name} зарабатывают одинаково."
                else:
                    return f"{self.name} и {other.name} зарабатывают не одинаково."
            else:
                return "Зарплата не указана"
        else:
            raise TypeError
