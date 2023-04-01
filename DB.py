 import os
import psycopg2

# Чтение переменных окружения
db_host = os.getenv("DB_HOST")
db_name = os.getenv("DB_NAME")
db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")

# Подключение к PostgreSQL
conn = psycopg2.connect(
    host=db_host,
    database=db_name,
    user=db_user,
    password=db_password
)

# Создание таблицы
cur = conn.cursor()
cur.execute("CREATE TABLE users (id SERIAL PRIMARY KEY, name VARCHAR(255));")
cur.close()

# Закрытие соединения
conn.close()
