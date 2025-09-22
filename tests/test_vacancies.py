import pytest

from src.vacancies import Vacancy


@pytest.fixture
def jax_vac():
    return Vacancy("Негодяй", "httts://jax.com", "Быть гадом и кринжом.", 1, 543, "")


def test_init_vacancies(jax_vac):
    assert jax_vac.name == "Негодяй"
    assert jax_vac.link == "httts://jax.com"
    assert jax_vac.description == "Быть гадом и кринжом."
    assert jax_vac.salary_to == 543
    assert jax_vac.salary_from == 1
    assert jax_vac.address == ""


def test_str_method(jax_vac):
    assert str(jax_vac) == "Вакансия Негодяй\nhttts://jax.com\nЗарплата 1-543 руб."


def test_salary_comparison(jax_vac):
    vac = Vacancy(
        "Ведущий", "htts://cain.com", "Устраивать Зубодробительные приключения", 100000, 300000, "Цифровой цирк"
    )
    result = jax_vac > vac
    result_2 = jax_vac == vac
    assert vac > jax_vac
    assert result == "Ведущий зарабатывает больше чем Негодяй."
    assert result_2 == "Негодяй и Ведущий зарабатывают не одинаково."


def test_no_salary():
    vac = Vacancy("Бандит", "htts://gamigoo.at", "Резвый и хороший парень", 0, 0, "Сладкое королевство")
    vac_2 = Vacancy("Бандит 2", "htts://macks.at", "Крепкий и добрый парень", 0, 0, "Сладкое королевство")
    result = vac == vac_2
    result_2 = vac > vac_2
    assert result == "Зарплата не указана"
    assert result_2 == "Зарплата не указана"


def test_error(jax_vac):
    with pytest.raises(TypeError):
        jax_vac > 9999
    with pytest.raises(TypeError):
        jax_vac == 9999
