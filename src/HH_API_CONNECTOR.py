from src.Parser import Parser
import requests


class HH(Parser):
    """
    Класс для работы с API HeadHunter
    Класс Parser является родительским классом, который вам необходимо реализовать
    """

    def __init__(self):
        self.__url = "https://api.hh.ru/vacancies"
        self.__headers = {"User-Agent": "HH-User-Agent"}
        self.params = {"text": "", "per_page": "", "only_with_salary": True}

    def __get_response(self, keyword, per_page) -> requests.Response:
        self.params["text"] = keyword
        self.params["per_page"] = per_page
        response = requests.get(self.__url, params=self.params, headers=self.__headers)

        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")
            return None
        except Exception as err:
            print(f"Other error occurred: {err}")
            return None

        return response

    def get_vacancies(self, keyword: str, per_page: int):
        response = self.__get_response(keyword, per_page)
        if response:
            return response.json().get("items", [])
        else:
            return []
