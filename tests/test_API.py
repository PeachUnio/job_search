from unittest.mock import Mock, patch

import requests

from src.API import HhAPI


def test_api_init():
    api = HhAPI()
    assert api.url == "https://api.hh.ru/vacancies"
    assert api.headers == {"User-Agent": "HH-User-Agent"}
    assert api.params == {"text": "", "page": 0, "per_page": 100}
    assert api.vacancies == []


@patch("src.API.requests.get")
def test_load_vocation(mock_get):
    mock_response = Mock()
    mock_response.json.return_value = {"items": [{"id": 1, "name": "Менеджер"}], "pages": 1}
    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response
    api = HhAPI()
    vacancies = api.load_vacancies("Менеджер")
    assert vacancies[0]["name"] == "Менеджер"
    mock_get.assert_called_once()


@patch("src.API.requests.get")
def test_empty_vocation(mock_get):
    mock_response = Mock()
    mock_response.json.return_value = {"items": [], "pages": 0}
    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response
    api = HhAPI()
    vacancies = api.load_vacancies("")
    assert vacancies == []
    mock_get.assert_called_once()


@patch("src.API.requests.get")
def test_error(mock_get):
    mock_get.side_effect = requests.exceptions.RequestException("API error")
    api = HhAPI()
    vacancies = api.load_vacancies("Python")
    assert vacancies == []
    assert mock_get.call_count == 1


@patch("src.API.requests.get")
def test_error_json(mock_get):
    mock_get.side_effect = ValueError("JSON error")
    api = HhAPI()
    vacancies = api.load_vacancies("Python")
    assert vacancies == []
    assert mock_get.call_count == 1
