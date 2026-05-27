import sys
from typing import Any

import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT


def create_database(database_name, params):
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')

    conn_db = None
    conn_tables = None

    conn_params = {**params, 'client_encoding': 'UTF8'}

    try:
        conn_db = psycopg2.connect(dbname='postgres', **conn_params)
        conn_db.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

        with conn_db.cursor() as cur:
            cur.execute("""
                SELECT pg_terminate_backend(pid)
                FROM pg_stat_activity
                WHERE datname = %s
                AND pid <> pg_backend_pid();
            """, (database_name,))
            print(f"Завершены активные подключения к БД {database_name}")

            cur.execute(f"DROP DATABASE IF EXISTS {database_name}")
            print(f"База данных {database_name} удалена (если существовала)")

            cur.execute(f"CREATE DATABASE {database_name} WITH ENCODING = 'UTF8'")
            print(f"База данных '{database_name}' успешно создана.")

        conn_tables = psycopg2.connect(dbname=database_name, **conn_params)
        conn_tables.autocommit = False

        with conn_tables.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS employers (
                    employer_id INTEGER PRIMARY KEY,
                    employer_name VARCHAR(255) NOT NULL,
                    employer_url VARCHAR(255)
                );
            """)

            cur.execute("""
                CREATE TABLE IF NOT EXISTS vacancies (
                    employer_id INTEGER REFERENCES employers(employer_id),
                    vacancy_id INTEGER PRIMARY KEY,
                    vacancy_title VARCHAR(255) NOT NULL,
                    vacancy_salary_from INTEGER,
                    vacancy_alternate_url VARCHAR(255)
                );
            """)

        conn_tables.commit()
        print("Таблицы успешно созданы.")

    except Exception as e:
        safe_err = str(e).encode('utf-8', errors='replace').decode('utf-8')
        print(f"Ошибка: {safe_err}")
    finally:
        if conn_db is not None:
            conn_db.close()
        if conn_tables is not None:
            conn_tables.close()


def save_data_to_database(data: list[dict[str, Any]], database_name: str, params: dict) -> None:
    conn = psycopg2.connect(dbname=database_name, **params)
    with conn.cursor() as cur:
        processed_employers = set()

        for item in data:
            emp = item["employer"]
            if emp["id"] not in processed_employers:
                cur.execute("INSERT INTO employers VALUES (%s, %s, %s) ON CONFLICT DO NOTHING",
                            (emp["id"], emp["name"], emp["alternate_url"]))
                processed_employers.add(emp["id"])

            salary = item["salary"]["from"] if item["salary"] and item["salary"]["from"] else 0
            cur.execute("""
                INSERT INTO vacancies (employer_id, vacancy_id, vacancy_title, vacancy_salary_from, vacancy_alternate_url)
                VALUES (%s, %s, %s, %s, %s) ON CONFLICT DO NOTHING""",
                        (emp["id"], item["id"], item["name"], salary, item["alternate_url"])
                        )
    conn.commit()
    conn.close()