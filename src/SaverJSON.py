from src.Saver import Saver
import json


class SaverJSON(Saver):
    def __init__(self, filename="vacancies.json"):
        """ Конструктор класса """
        super().__init__(filename)

    def write_data(self, vacancies):
        """ Запись данных в json """
        data = self.get_data()
        data.extend(vacancies)

        with open(self._Saver__filename, "a", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

    def get_data(self):
        """ Получение данных json """
        try:
            with open(self._Saver__filename, "r", encoding="utf-8") as file:
                return json.load(file)
        except FileNotFoundError:
            return []

    def del_data(self):
        """ Удаление данных из файла """
        with open(self._Saver__filename, "w", encoding="utf-8") as file:
            json.dump([], file, ensure_ascii=False, indent=4)
