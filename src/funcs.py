import requests
from abc import ABC, abstractmethod


class Parser(ABC):

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


class Vacations():

    def __init__(self, name, url, salary, description):
        self.name = name
        self.url = url
        self.description = description
        self.salary = self.validate_salary(salary)

    def validate_salary(self, salary):
        if not isinstance(salary, (int, float)) or salary <= 0 or not salary:
            return "Зарплата не указана"

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


