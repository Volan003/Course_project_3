import requests
from typing import List
import time
import json


def get_vacancies_from_one_employer(employer_ids: List[int]):
    """Получаем данные из HH.ru по списку работодателей"""
    all_vacancies = {}

    for employer_id in employer_ids:
        print(f"Получаем вакансии для работодателя ID: {employer_id}")

        params = {
            'employer_id': employer_id,
            'area': 1,
            'per_page': 100,
            'page': 0
        }
        for page in range(10):
            try:
                response = requests.get("https://api.hh.ru/vacancies", params=params)
                data=response.json()
                vacancies = data.get("items", [])

                for vacancie in vacancies:
                    vacancie_id = vacancie.get("id")
                    vacancie_name = vacancie.get("name")
                    vacancie_salary = vacancie.get("salary")
                    vacancie_url = vacancie.get("url")
                    all_vacancies[vacancie_id]=[
                        vacancie_id,
                        vacancie_name,
                        vacancie_salary,
                        vacancie_url
                    ]
            except requests.exceptions.RequestException as e:
                print(f"Ошибка запроса для ID {employer_id}: {e}")

    return all_vacancies

print(get_vacancies_from_one_employer([9694561]))
