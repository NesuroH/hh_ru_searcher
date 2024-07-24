from src.HH_API_CONNECTOR import HH
from src.SaverJSON import SaverJSON
from src.Vacancy import Vacancy
from unittest.mock import patch, MagicMock
import pytest, json

# Test data
vacancy_data = {
    "name": "Software Engineer",
    "alternate_url": "http://example.com",
    "salary": {"from": 1000, "to": 2000},
    "area": {"name": "New York"},
    "snippet": {"requirement": "Python", "responsibility": "Develop software"}
}


@pytest.fixture
def vacancy_instance():
    return Vacancy.from_hh_dict(vacancy_data)


# Test HH class
def test_hh_get_response():
    hh = HH()
    with patch('requests.get') as mock_get:
        mock_get.return_value = MagicMock(status_code=200, json=lambda: {"items": [vacancy_data]})
        response = hh._HH__get_response("Python", 1)
        assert response.status_code == 200
        assert response.json() == {"items": [vacancy_data]}


def test_hh_get_vacancies():
    hh = HH()
    with patch('requests.get') as mock_get:
        mock_get.return_value = MagicMock(status_code=200, json=lambda: {"items": [vacancy_data]})
        vacancies = hh.get_vacancies("Python", 1)
        assert len(vacancies) == 1
        assert vacancies[0]["name"] == "Software Engineer"


# Test SaverJSON class
@pytest.fixture
def temp_file(tmp_path):
    return tmp_path / "vacancies.json"


def test_saverjson_write_data(temp_file, vacancy_instance):
    saver = SaverJSON(temp_file)
    saver.write_data([vacancy_instance.to_dict()])
    with open(temp_file, "r", encoding="utf-8") as file:
        data = json.load(file)
        assert len(data) == 1
        assert data[0]["name"] == "Software Engineer"


def test_saverjson_get_data(temp_file, vacancy_instance):
    saver = SaverJSON(temp_file)
    saver.write_data([vacancy_instance.to_dict()])
    data = saver.get_data()
    assert len(data) == 1
    assert data[0]["name"] == "Software Engineer"


def test_saverjson_del_data(temp_file, vacancy_instance):
    saver = SaverJSON(temp_file)
    saver.write_data([vacancy_instance.to_dict()])
    saver.del_data()
    data = saver.get_data()
    assert data == []


# Test Vacancy class
def test_vacancy_str(vacancy_instance):
    expected_str = (
        "Наименование вакансии: Software Engineer\n"
        "Ссылка на вакансию: http://example.com\n"
        "Зарплата: от 1000 до 2000\n"
        "Место работы: New York\n"
        "Краткое описание: Python\n"
        "Develop software\n"
    )
    assert str(vacancy_instance) == expected_str


def test_vacancy_lt():
    vacancy1 = Vacancy("Job1", "url1", 1000, 2000, "City1", "Req1", "Resp1")
    vacancy2 = Vacancy("Job2", "url2", 2000, 3000, "City2", "Req2", "Resp2")
    assert vacancy1 < vacancy2


def test_vacancy_from_hh_dict():
    vacancy = Vacancy.from_hh_dict(vacancy_data)
    assert vacancy.name == "Software Engineer"
    assert vacancy.salary_from == 1000
    assert vacancy.salary_to == 2000


def test_vacancy_to_dict(vacancy_instance):
    vacancy_dict = vacancy_instance.to_dict()
    assert vacancy_dict["name"] == "Software Engineer"
    assert vacancy_dict["salary_from"] == 1000
    assert vacancy_dict["salary_to"] == 2000
    assert vacancy_dict["area_name"] == "New York"
    assert vacancy_dict["requirement"] == "Python"
    assert vacancy_dict["responsibility"] == "Develop software"
