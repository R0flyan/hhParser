import psycopg2
from psycopg2 import sql

def get_connection():
    connection = psycopg2.connect(
        dbname="postgres",
        user="postgres",
        password="Barca5020pgsql",
        host="localhost"
    )
    return connection
def create_table():
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS vacancies (
            id SERIAL PRIMARY KEY,
            title VARCHAR(255),
            company VARCHAR(255),
            location VARCHAR(255),
            link TEXT,
            salary VARCHAR(255),
            requirement TEXT
        );
        """
    )
    connection.commit()
    cursor.close()
    connection.close()
    
    if __name__ == '__main__':
        create_table()