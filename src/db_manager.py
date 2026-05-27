import psycopg2


class DBManager:
    """Класс, который будет подключаться в БД PostgreSQL"""

    def __init__(self, host, database, user, port, password):
        """Инициализация атрибутов"""
        self.params = {
            "host": host,
            "dbname": database,
            "user": user,
            "port": port,
            "password": password
        }
        self.conn = psycopg2.connect(**self.params)

    def get_companies_and_vacancies_count(self):
        """Получает список всех компаний и количество вакансий у каждой компании"""
        with self.conn.cursor() as cur:
            cur.execute("SELECT e.employer_name, COUNT(v.vacancy_id) FROM employers e "
                        "LEFT JOIN vacancies v ON e.employer_id = v.employer_id "
                        "GROUP BY e.employer_name")
            return cur.fetchall()

    def get_all_vacancies(self):
        """Получает список всех вакансий с указанием названия компании,
         названия вакансии и зарплаты и ссылки на вакансию."""
        with self.conn.cursor() as cur:
            cur.execute("""
                SELECT e.employer_name, v.vacancy_title, v.vacancy_salary_from, v.vacancy_alternate_url 
                FROM vacancies v 
                JOIN employers e ON e.employer_id = v.employer_id
            """)
            return cur.fetchall()

    def get_avg_salary(self):
        """Получает среднюю зарплату по вакансиям"""
        with self.conn.cursor() as cur:
            cur.execute("SELECT AVG(salary_from) FROM vacancies WHERE salary_from > 0")
            return cur.fetchone()[0]

    def get_vacancies_with_higher_salary(self):
        """Получает список всех вакансий, у которых зарплата выше средней по всем вакансиям"""
        with self.conn.cursor() as cur:
            cur.execute("""
            SELECT * FROM vacancies 
            WHERE salary > (SELECT AVG(salary) FROM vacancies WHERE salary > 0)
            """)
            return cur.fetchall()

    def get_vacancies_with_keyword(self, keyword: str):
        """Получает список всех вакансий, в названии которых содержатся переданные в метод слова"""
        with self.conn.cursor() as cur:
            query = "SELECT * FROM vacancies WHERE vacancy_title ILIKE %s"
            cur.execute(query, (f"%{keyword}%",))
            return cur.fetchall()
