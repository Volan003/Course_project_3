# import requests
# from typing import List
# import json

# def get_vacancies_data(employer_ids: List[str]):
#     """Получаем данные из HH.ru по списку работодателей"""
#     all_vacancies = []
#
#     for employer_id in employer_ids:
#         print(f"Получаем вакансии для работодателя ID: {employer_id}")
#
#         params = {
#             'employer_id': employer_id,
#             'area': 1,
#             'per_page': 100
#         }
#
#         response = requests.get("https://api.hh.ru/vacancies", params=params).json()
#         total_pages = response.get("pages", 1)
#
#         for page in range(min(total_pages, 10)):
#             params["page"] = page
#             try:
#                 items = requests.get("https://api.hh.ru/vacancies", params=params).json().get("items", [])
#
#                 for item in items:
#                     vacancy = Vacancy(
#                         id=item.get("id"),
#                         name=item.get("name"),
#                         salary=item.get("salary"),
#                         url=item.get("alternate_url")
#                     )
#                     all_vacancies.append(vacancy)
#             except Exception as e:
#                 print(f"Ошибка запроса для ID {employer_id}: {e}")
#
#     return all_vacancies
#

import json
from typing import Dict, List


def load_data_from_json(file_path: str = "data/data.json") -> Dict[str, List[Dict]]:
    """Загрузка данных из локального JSON‑файла"""
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        print("Данные успешно загружены:")
        print(data)
        return data
