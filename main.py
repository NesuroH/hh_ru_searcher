from src.HH_API_CONNECTOR import HH
from src.SaverJSON import SaverJSON
from src.Vacancy import Vacancy


def main():
    user_choice = input("Что вы хотите сделать?\n"
                        "Введите '1' если собираетесь найти профессию, '2' если хотите очистить json файл.\n")
    if user_choice == "1":
        keyword = input("Какую профессию ищите?\n").lower()
        per_page = int(input("Сколько профессии вывести?\n"))

        hh_api = HH()
        vacancies = hh_api.get_vacancies(keyword, per_page)
        vacancies = [Vacancy.from_hh_dict(vacancy) for vacancy in vacancies]
        vacancies = sorted(vacancies, reverse=True)

        print("Топ выбранных вакансии с 'HeadHunter' по зарплате: \n")
        for i in sorted(vacancies, reverse=True):
            print(i)

        vacancies = [vacancy.to_dict() for vacancy in vacancies]
        saver = SaverJSON('data/vacancies.json')

        saver.write_data(vacancies)
        print("Данные записаны в json-файл")

    else:
        saver = SaverJSON('data/vacancies.json')
        saver.del_data()
        print("Данные удалены!")


if __name__ == '__main__':
    main()
