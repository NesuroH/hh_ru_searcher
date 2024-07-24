from abc import ABC, abstractmethod


class Saver(ABC):
    def __init__(self, filename):
        self.__filename = filename

    @abstractmethod
    def write_data(self, vacancies):
        pass

    @abstractmethod
    def get_data(self):
        pass

    @abstractmethod
    def del_data(self):
        pass
