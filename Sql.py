SQL Код для Создания Таблиц

CREATE TABLE Companies (
    company_id INT PRIMARY KEY,
    company_name VARCHAR NOT NULL
);

CREATE TABLE Vacancies (
    vacancy_id INT PRIMARY KEY,
    company_id INT,
    vacancy_name VARCHAR NOT NULL,
    salary INT,
    link VARCHAR NOT NULL,
    FOREIGN KEY (company_id) REFERENCES Companies(company_id)
);