import json
import requests
from abc import ABC, abstractmethod


class Parser(ABC):
    def __init__(self, file_worker):
        self.file_worker = file_worker

    @abstractmethod
    def load_vacancies(self, keyword):
        pass


class HH(Parser):
    """
    Класс для работы с API HeadHunter
    Класс Parser является родительским классом, который вам необходимо реализовать
    """

    def __init__(self, file_worker):
        self.url = 'https://api.hh.ru/vacancies'
        self.headers = {'User-Agent': 'HH-User-Agent'}
        self.params = {'text': '', 'page': 0, 'per_page': 100}
        self.vacancies = []
        super().__init__(file_worker)

    def load_vacancies(self, keyword):
        self.params['text'] = keyword
        while self.params.get('page') != 20:
            response = requests.get(self.url, headers=self.headers, params=self.params)
            vacancies = response.json()['items']
            self.vacancies.extend(vacancies)
            self.params['page'] += 1
        return self.vacancies


class Vacations:
    def __init__(self, name, url, salary, description):
        self.name = name
        self.url = url
        self.description = description
        self.salary = self.validate_salary(salary)

    @staticmethod
    def validate_salary(salary):
        if not isinstance(salary, (int, float)) or salary <= 0:
            return "Зарплата не указана"
        return salary

    def __eq__(self, other):
        if isinstance(other, Vacations):
            return self.salary == other.salary
        return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __lt__(self, other):
        if isinstance(other, Vacations):
            return self.salary < other.salary
        return NotImplemented

    def __le__(self, other):
        if isinstance(other, Vacations):
            return self.salary <= other.salary
        return NotImplemented

    def __gt__(self, other):
        if isinstance(other, Vacations):
            return self.salary > other.salary
        return NotImplemented

    def __ge__(self, other):
        if isinstance(other, Vacations):
            return self.salary >= other.salary
        return NotImplemented


class Saver(ABC):
    def __init__(self, filename):
        self.filename = filename

    @abstractmethod
    def write_data(self, data):
        pass

    @abstractmethod
    def get_data(self):
        pass

    @abstractmethod
    def del_data(self, key):
        pass


class SaverJSON(Saver):
    def __init__(self, filename):
        super().__init__(filename)

    def write_data(self, vacancies):
        data = self.get_data()
        if not isinstance(data, list):
            data = []
        data.extend(vacancies)
        with open(self.filename, 'w', encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

    def get_data(self):
        try:
            with open(self.filename, 'r', encoding="utf-8") as file:
                return json.load(file)
        except FileNotFoundError:
            return []

    def del_data(self, key):
        data = self.get_data()
        # Assuming each item in data is a dictionary and key is a unique identifier
        new_data = [item for item in data if item.get('id') != key]
        if len(new_data) != len(data):
            self.save_data(new_data)
            print(f"Key '{key}' has been deleted.")
        else:
            print(f"Key '{key}' not found in the JSON file.")

    def save_data(self, data):
        with open(self.filename, 'w', encoding="utf-8") as file:
            json.dump(data, file, indent=4)

    def cast_to_object_list(self, data):
        # Assuming you want to convert dictionaries to some object instances
        # This is a placeholder implementation
        return [self.dict_to_object(item) for item in data]

    def dict_to_object(self, dict_item):
        # Placeholder for converting a dictionary to an object
        # You need to define how to convert a dictionary to your specific object
        return dict_item  # Replace with actual conversion logic


class VacancyManager:
    @staticmethod
    def search_vacancy(user_search, vacancies):
        filtered = {}
        for vacancy in vacancies:
            if user_search in vacancy["name"]:
                filtered += vacancy

        return filtered



    @staticmethod
    def filter_vacancies(vacancies, filter_words):
        filtered = []
        for vacancy in vacancies:
            if any(word in vacancy['requirement'] for word in filter_words):
                filtered.append(vacancy)
        return filtered

    @staticmethod
    def get_vacancies_by_salary(vacancies, salary_range):
        min_salary, max_salary = map(int, salary_range.split(' - '))
        ranged_vacancies = []
        for vacancy in vacancies:
            salary_min, salary_max = vacancy['salary']['from'], vacancy['salary']['to']
            if salary_min and salary_min <= min_salary <= max_salary <= max_salary:
                ranged_vacancies.append(vacancy)
        return ranged_vacancies

    @staticmethod
    def sort_vacancies(vacancies):
        return sorted(vacancies, key=lambda x: x['salary'], reverse=True)

    @staticmethod
    def get_top_vacancies(vacancies, top_n):
        return vacancies[:top_n]

    @staticmethod
    def print_vacancies(vacancies):
        for vacancy in vacancies:
            print(f"Name: {vacancy['name']}, Salary: {vacancy['salary']}, URL: {vacancy['url']}")


# Main code

