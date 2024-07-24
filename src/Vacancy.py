class Vacancy:
    """ Класс для работы с вакансиями """

    __slots__ = ("name", "alternate_url", "salary_from", "salary_to", "area_name", "requirement", "responsibility")

    def __init__(self, name, alternate_url, salary_from, salary_to, area_name, requirement, responsibility):
        """ Конструктор класса """

        self.name: str = name
        self.alternate_url: str = alternate_url
        self.salary_from: int = salary_from
        self.salary_to: int = self.check_salary(salary_to)
        self.area_name: str = area_name
        self.requirement: str = requirement
        self.responsibility: str = responsibility

    @staticmethod
    def check_salary(salary_to):
        if salary_to == 0:
            return "..."
        else:
            return salary_to

    def __str__(self) -> str:
        """ Строковое представление вакансии """

        return (f"Наименование вакансии: {self.name}\n"
                f"Ссылка на вакансию: {self.alternate_url}\n"
                f"Зарплата: от {self.salary_from} до {self.salary_to}\n"
                f"Место работы: {self.area_name}\n"
                f"Краткое описание: {self.requirement}\n"
                f"{self.responsibility}\n")

    def __lt__(self, other) -> bool:
        """ Метод сравнения от большего к меньшему """

        return self.salary_from < other.salary_from

    @classmethod
    def from_hh_dict(cls, vacancy_data: dict):
        """ Метод возвращает экземпляр класса в виде списка """

        salary = vacancy_data.get("salary")

        return cls(
            vacancy_data["name"],
            vacancy_data["alternate_url"],
            salary.get("from") if salary.get("from") else 0,
            salary.get("to") if salary.get("to") else 0,
            vacancy_data["area"]["name"],
            vacancy_data["snippet"]["requirement"],
            vacancy_data["snippet"]["responsibility"],
        )

    def to_dict(self) -> dict:
        """ Метод возвращает вакансию в виде словаря """

        return {
            "name": self.name,
            "alternate_url": self.alternate_url,
            "salary_from": self.salary_from,
            "salary_to": self.salary_to,
            "area_name": self.area_name,
            "requirement": self.requirement,
            "responsibility": self.responsibility,
        }
