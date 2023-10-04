import psycopg2
import requests
from DB import psycopg2
# Параметры подключения к базе данных
DB_PARAMS = {
    'dbname': 'north',
    'user': 'postgres',
    'password': 'kerik00989A',
    'host': 'localhost'
}

# API Endpoints
COMPANY_API_ENDPOINT = "https://api.hh.ru/employers"
VACANCY_API_ENDPOINT = "https://api.hh.ru/vacancies"

# Идентификаторы интересующих вас компаний
COMPANY_IDS = ["employer_id1", "employer_id2", "employer_id3"]

# Подключение к базе данных
conn = psycopg2.connect(**DB_PARAMS)
cursor = conn.cursor()

def fetch_data(api_endpoint, params=None):
    response = requests.get(api_endpoint, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to fetch data. Status code: {response.status_code}")
        return None

def insert_company(company_id, company_name):
    cursor.execute("INSERT INTO Companies (company_id, company_name) VALUES (%s, %s) ON CONFLICT DO NOTHING;", (company_id, company_name))
    conn.commit()

def insert_vacancy(vacancy_id, company_id, vacancy_name, salary, link):
    cursor.execute("INSERT INTO Vacancies (vacancy_id, company_id, vacancy_name, salary, link) VALUES (%s, %s, %s, %s, %s) ON CONFLICT DO NOTHING;",
                   (vacancy_id, company_id, vacancy_name, salary, link))
    conn.commit()

def main():
    for company_id in COMPANY_IDS:
        company = fetch_data(f"{COMPANY_API_ENDPOINT}/{company_id}")
        if company:
            insert_company(company_id, company['name'])

            # Получение вакансий компании
            params = {"employer_id": company_id}
            vacancies = fetch_data(VACANCY_API_ENDPOINT, params)

            for vacancy in vacancies['items']:
                insert_vacancy(vacancy['id'], company_id, vacancy['name'], vacancy['salary'], vacancy['alternate_url'])


main()
cursor.close()
conn.close()