from src.API import HhAPI
from src.load_vac import LoadVacancy
from src.vacancies import Vacancy


def function_for_user():
    """Функция для взаимодействия с пользователем"""

    # сбор данных для функции
    vac_name = input("Введите название вакансии: ").capitalize()
    special_words = input("Введите ключевые слова для поиска в описании вакансии: ").split()
    top_n = int(input("Введите количество вакансий для вывода в топ N: "))

    vac = HhAPI()
    vac.load_vacancies(vac_name)
    sorted_list = vac.sorted_by_salary()

    # фильтрация по слову
    filter_list = sorted_list

    if special_words:
        temp_list = []

        for word in special_words:
            filtered = vac.sorted_by_world(word)
            for vacancy in filtered:
                if vacancy not in temp_list:
                    temp_list.append(vacancy)

        if temp_list:
            filter_list = temp_list

    yes_or_no = input("Загрузить топ N вакансий в отдельный файл (введите да или нет): ").lower()
    if yes_or_no == "да":
        i = 0
        load = LoadVacancy()
        for vacancy in filter_list:
            vacancy_in = Vacancy.add_new_vac(vacancy)
            load.load_vacancy(vacancy_in)
            i += 1
            if i == top_n:
                break

    else:
        i = 0
        for vacancy in filter_list:
            vacancy_in = Vacancy.add_new_vac(vacancy)
            print(vacancy_in)
            i += 1
            if i == top_n:
                break


if __name__ == "__main__":
    function_for_user()
