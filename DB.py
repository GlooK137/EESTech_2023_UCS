import json
import os
import time

import psycopg2
import config
# # Чтение переменных окружения
# db_host = os.getenv("DB_HOST")
# db_name = os.getenv("DB_NAME")
# db_user = os.getenv("DB_USER")
# db_password = os.getenv("DB_PASSWORD")
#
# # Подключение к PostgreSQL
# db = psycopg2.connect(
#     host=db_host,
#     database=db_name,
#     user=db_user,
#     password=db_password,
#     port=5432
# )
#
# # Создание таблицы
# cursor = db.cursor()
# cursor.execute("CREATE TABLE users3 (id SERIAL PRIMARY KEY, name VARCHAR(255));")
# db.commit()
# cursor.close()
#
# # Закрытие соединения
# db.close()




class DBConnect():

    def __init__(self):
        # Чтение переменных окружения
        db_host = os.getenv("DB_HOST")
        db_name = os.getenv("DB_NAME")
        db_user = os.getenv("DB_USER")
        db_password = os.getenv("DB_PASSWORD")

        # Подключение к PostgreSQL
        self.db = psycopg2.connect(
            host=db_host,
            database=db_name,
            user=db_user,
            password=db_password,
            port=5432
        )

        self.db.autocommit = True

        self.cursor = self.db.cursor()

        self.create_db()

    def create_db(self):

        # Создание таблицы

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
              id SERIAL PRIMARY KEY,
              name TEXT
            );
        """)

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS events (
              id SERIAL PRIMARY KEY,
              name TEXT,
              video TEXT,
              data INTEGER
            );
        """)

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS question_db (
              id SERIAL PRIMARY KEY,
              question TEXT,
              genre_id INTEGER,
              answer TEXT,
              correct_answer TEXT,
              points INTEGER
            );
        """)

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS users_quiz (
              id_user INTEGER,
              id_question INTEGER,
              point INTEGER,
              FOREIGN KEY (id_user) REFERENCES users(id),
              FOREIGN KEY (id_question) REFERENCES question_db(id)
            );
        """)



        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS genre_table (
              genre_id SERIAL PRIMARY KEY,
              genre TEXT
            );
        """)

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS reg_for_event (
              id_user INTEGER,
              id_event INTEGER,
              FOREIGN KEY (id_user) REFERENCES users(id),
              FOREIGN KEY (id_event) REFERENCES events(id)
            );
        """)

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS quests_table (
              id_user INTEGER,
              id_question INTEGER,
              points INTEGER,
              FOREIGN KEY (id_user) REFERENCES users(id),
              FOREIGN KEY (id_question) REFERENCES question_db(id)
            );
        """)


    def register_user(self, name):

        self.cursor.execute("INSERT INTO users (name) VALUES (%s);", (name,))

    def register_new_genre(self, new_genre):
        self.cursor.execute("""INSERT INTO genre_table (genre) 
                SELECT %s 
                WHERE NOT EXISTS (
                  SELECT 1 FROM genre_table WHERE genre = %s
                );
                """, (new_genre,new_genre))


    def register_qustion(self, question, genre_id, answer, correct_answer, points):
        self.cursor.execute("INSERT INTO question_db (question, genre_id, answer, correct_answer, points) VALUES (%s, %s, %s, %s, %s);", (question, genre_id, answer, correct_answer, points))
        # user_id = self.cursor.fetchone()[0]
        # return user_id

    def register_miro(self, name, video, data):
        self.cursor.execute("INSERT INTO events (name, video, data) VALUES (%s, %s, %s);", (name, video, data))
        # user_id = self.cursor.fetchone()[0]
        # return user_id

    def close(self):
        self.db.commit()
        self.cursor.close()
        self.db.close()

    # cursor.execute("CREATE TABLE users3 (id SERIAL PRIMARY KEY, name VARCHAR(255));")
    # db.commit()
    # cursor.close()

    # Закрытие соединения
    # db.close()


if __name__ == '__main__':
    db_conn = DBConnect()
    db_conn.register_new_genre('Безопасность1')
    db_conn.register_qustion('Что нельзя засовывать в розетку?', 0, json.dumps(['Чайник', "Принтер", "Пальцы"]), 2, 1)

    db_conn.register_miro('Мир', 'video/mir.mp4', time.time() + 24*60*60*6)


    db_conn.close()