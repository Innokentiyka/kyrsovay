import psycopg2


class DBManager:
    def __init__(self, db_params):
        self.conn = psycopg2.connect(**db_params)
        self.cursor = self.conn.cursor()

    def get_companies_and_vacancies_count(self):
        self.cursor.execute(
            "SELECT c.company_name, COUNT(v.vacancy_id) FROM Companies c JOIN Vacancies v ON c.company_id = v.company_id GROUP BY c.company_name;")
        return self.cursor.fetchall()

    def get_all_vacancies(self):
        self.cursor.execute(
            "SELECT c.company_name, v.vacancy_name, v.salary, v.link FROM Companies c JOIN Vacancies v ON c.company_id = v.company_id;")
        return self.cursor.fetchall()

    def get_avg_salary(self):
        self.cursor.execute("SELECT AVG(salary) FROM Vacancies WHERE salary IS NOT NULL;")
        return self.cursor.fetchone()[0]

    def get_vacancies_with_higher_salary(self):
        avg_salary = self.get_avg_salary()
        self.cursor.execute(f"SELECT v.vacancy_name, v.salary, v.link FROM Vacancies v WHERE v.salary > {avg_salary};")
        return self.cursor.fetchall()

    def get_vacancies_with_keyword(self, keyword):
        self.cursor.execute(
            f"SELECT v.vacancy_name, v.salary, v.link FROM Vacancies v WHERE LOWER(v.vacancy_name) LIKE '%{keyword.lower()}%';")
        return self.cursor.fetchall()