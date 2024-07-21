from src.funcs import HH, SaverJSON, Vacancy

def main():

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
    saver = SaverJSON('vacancies.json')

    saver.write_data(vacancies)
    print("Данные записаны в json-файл")

if __name__ == '__main__':
    main()