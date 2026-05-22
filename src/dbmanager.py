import psycopg2

class DBManager:
    """Класс, который будет подключаться в БД PostgreSQL"""
    def __init__(self, host, database, user, port, password):
        """Инициализация атрибутов"""
        self.params = {
            "host":host,
            "dbname":database,
            "user":user,
            "port":port,
            "password":password
        }
        self.conn = psycopg2.connect(**self.params)


    def get_companies_and_vacancies_count (self):
        """Получает список всех компаний и количество вакансий у каждой компеании"""
        pass