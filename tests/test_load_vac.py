import json
import os
from unittest.mock import mock_open, patch

import pytest

from src.load_vac import LoadVacancy  # Импортируйте ваш класс
from src.vacancies import Vacancy


@pytest.fixture
def sample_vacancy():
    """Фикстура для тестовой вакансии"""
    return Vacancy(
        name="Python Developer",
        link="https://example.com",
        description="Разработка на Python",
        salary_from=100000,
        salary_to=150000,
        address="Москва",
    )


@pytest.fixture
def load_vacancy():
    """Фикстура для объекта LoadVacancy"""
    return LoadVacancy("test_vacancies.json")


def test_check_exist_file(load_vacancy):
    if os.path.exists("test_vacancies.json"):
        os.remove("test_vacancies.json")

    lv = LoadVacancy("test_vacancies.json")
    assert os.path.exists("test_vacancies.json")

    with open("test_vacancies.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    assert data == []


def test_load_vacancy_success(load_vacancy, sample_vacancy):
    """Тестируем успешную загрузку вакансии"""
    load_vacancy.load_vacancy(sample_vacancy)

    with open("test_vacancies.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    assert len(data) == 1
    assert data[0]["name"] == "Python Developer"
    assert data[0]["salary"] == "100000-150000"


def test_load_vacancy_duplicate(load_vacancy, sample_vacancy):
    """Тестируем что дубликаты не добавляются"""
    load_vacancy.load_vacancy(sample_vacancy)
    load_vacancy.load_vacancy(sample_vacancy)  # Дубликат

    with open("test_vacancies.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    assert len(data) == 1


def test_load_vacancy_type_error(load_vacancy):
    """Тестируем ошибку типа"""
    with pytest.raises(TypeError):
        load_vacancy.load_vacancy("not a vacancy")  # Передаем строку вместо Vacancy


def test_get_vacancy_by_criteria(load_vacancy, sample_vacancy):
    """Тестируем поиск по критериям"""
    load_vacancy.load_vacancy(sample_vacancy)

    result = load_vacancy.get_vac({"name": "Python Developer"})
    assert len(result) == 1
    assert result[0].name == "Python Developer"

    result = load_vacancy.get_vac({"name": "Java Developer"})
    assert len(result) == 0


def test_clean_all(load_vacancy, sample_vacancy):
    load_vacancy.load_vacancy(sample_vacancy)

    load_vacancy.clean_all()

    with open("test_vacancies.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    assert data == []


def test_get_vacancy_salary_conversion(load_vacancy, sample_vacancy):
    """Тестируем преобразование salary из строки в числа"""
    load_vacancy.load_vacancy(sample_vacancy)

    result = load_vacancy.get_vac({"name": "Python Developer"})
    vacancy = result[0]

    assert isinstance(vacancy.salary_from, int)
    assert isinstance(vacancy.salary_to, int)
    assert vacancy.salary_from == 100000
    assert vacancy.salary_to == 150000


def teardown_function():
    """Очистка после каждого теста"""
    if os.path.exists("test_vacancies.json"):
        os.remove("test_vacancies.json")
