from src.funcs import HH, SaverJSON, Vacations, VacancyManager

hh_api = HH("vacancies.json")

# Получение вакансий с hh.ru в формате JSON
hh_vacancies = hh_api.load_vacancies("Python")

# Преобразование набора данных из JSON в список объектов
json_saver = SaverJSON(hh_vacancies)
vacancies_list = json_saver.cast_to_object_list(hh_vacancies)



# Сохранение информации о вакансиях в файл
#json_saver.write_data([vacancy.__dict__])
#json_saver.del_data(vacancy.__dict__.get('id'))

# Функция для взаимодействия с пользователем
def user_interaction():
    platforms = ["HeadHunter"]
    search_query = input("Введите поисковый запрос: ")
    top_n = int(input("Введите количество вакансий для вывода в топ N: "))
    filter_words = input("Введите ключевые слова для фильтрации вакансий: ").split()
    salary_range = input("Введите диапазон зарплат: ")  # Пример: 100000 - 150000

    filtered_vacancies = VacancyManager.filter_vacancies(vacancies_list, filter_words)
    ranged_vacancies = VacancyManager.get_vacancies_by_salary(filtered_vacancies, salary_range)
    sorted_vacancies = VacancyManager.sort_vacancies(ranged_vacancies)
    top_vacancies = VacancyManager.get_top_vacancies(sorted_vacancies, top_n)
    VacancyManager.print_vacancies(top_vacancies)

if __name__ == "__main__":
    user_interaction()