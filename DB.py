import os
import psycopg2

# Чтение переменных окружения
db_host = os.getenv("DB_HOST")
db_name = os.getenv("DB_NAME")
db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")

# Подключение к PostgreSQL
db = psycopg2.connect(
    host=db_host,
    database=db_name,
    user=db_user,
    password=db_password,
    port=5432
)

# Создание таблицы
cursor = db.cursor()
cursor.execute("CREATE TABLE users3 (id SERIAL PRIMARY KEY, name VARCHAR(255));")
cursor.close()

# Закрытие соединения
cursor.close()
