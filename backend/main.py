from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests
import psycopg2
import os

app = FastAPI()

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

class SearchRequest(BaseModel):
    keyword: str

def fetch_vacancies(keyword, min_salary=None):
    url = 'https://api.hh.ru/vacancies'
    params = {
        'text': keyword,
        'area': 1,
        'page': 0,
        'per_page': 40
    }

    if min_salary:
        params['salary'] = min_salary
        
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        raise HTTPException(status_code=response.status_code, detail="Unable to fetch vacancies")

def get_connection():
    connection = psycopg2.connect(
        dbname="postgres",
        user="postgres",
        password="Barca5020pgsql",
        host="host.docker.internal"
    )
    return connection
# def get_connection():
#     DATABASE_URL = os.getenv('postgresql://postgres:Barca5020pgsql@<localhost>:5432/postgres')
#     connection = psycopg2.connect(DATABASE_URL)
#     return connection

def clear_table():
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("DELETE FROM vacancies;")
    connection.commit()
    cursor.close()
    connection.close()

def save_to_db(vacancies):
    clear_table()
    connection = get_connection()
    cursor = connection.cursor()
    for vacancy in vacancies['items']:
        cursor.execute(
            "INSERT INTO vacancies (title, company, location, link, salary, requirement) VALUES (%s, %s, %s, %s, %s, %s)",
            (vacancy['name'], vacancy['employer']['name'], vacancy['area']['name'], vacancy['alternate_url'], 
             vacancy['salary']['from'] if vacancy['salary'] else None, 
             vacancy['snippet']['requirement'])
        )
    connection.commit()
    cursor.close()
    connection.close()

@app.post("/vacancies")
def get_vacancies(search: SearchRequest, min_salary: int = None):
    vacancies = fetch_vacancies(search.keyword, min_salary)
    save_to_db(vacancies)
    return vacancies['items']

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)