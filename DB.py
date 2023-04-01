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
              points INTEGER,
              foto TEXT
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
              id_genre INTEGER,
              points INTEGER,
              FOREIGN KEY (id_user) REFERENCES users(id),
              FOREIGN KEY (id_genre) REFERENCES genre_table(genre_id)
            );
        """)


    def register_user(self, name):

        self.cursor.execute("INSERT INTO users (name) VALUES (%s);", (name,))

    def cash(self, user_id):
        self.cursor.execute("SELECT SUM(point)*7 FROM users_quiz WHERE id_user=%s;", (user_id,))
        quests = self.cursor.fetchone()[0]
        print(quests)
        if quests:
            quests = quests
        else:
            quests = 0

        self.cursor.execute("SELECT SUM(points) FROM quests_table WHERE id_user=%s;", (user_id,))
        points = self.cursor.fetchone()[0]
        if quests:
            points = points
        else:
            points = 0

        return {
            'cash_quests':quests,
            'cash_points': points,
            'cash_all': quests + points,
        }

    def genre_get(self):

        self.cursor.execute("SELECT * FROM genre_table;")
        data = self.cursor.fetchall()
        out = {}
        for key, element in data:
            out[key] = element

        return out


    def register_new_genre(self, new_genre):
        self.cursor.execute("""INSERT INTO genre_table (genre) 
                SELECT %s 
                WHERE NOT EXISTS (
                  SELECT 1 FROM genre_table WHERE genre = %s
                );
                """, (new_genre,new_genre))


    def register_qustion(self, question, genre_id, answer, correct_answer, points, foto):
        self.cursor.execute("INSERT INTO question_db (question, genre_id, answer, correct_answer, points, foto) VALUES (%s, %s, %s, %s, %s, %s);", (question, genre_id, answer, correct_answer, points, foto))
        # user_id = self.cursor.fetchone()[0]
        # return user_id


    def get_question(self, is_user, genre_id):
        query = """SELECT id, question, answer, correct_answer FROM question_db 
                   WHERE genre_id = %s 
                   AND id NOT IN (SELECT id_question FROM users_quiz WHERE id_user = %s) 
                   ORDER BY random() LIMIT 1;"""

        self.cursor.execute(query, (genre_id, is_user))
        random_question = self.cursor.fetchone()
        print(random_question)

        if random_question:
            return {
                "info": True,
                'question_id': random_question[0],
                'question': random_question[1],
                'answer': json.loads(random_question[2]),
                'correct_answer':random_question[3]
            }
        else:
            print(is_user, genre_id, 47)
            self.cursor.execute(
                "INSERT INTO quests_table (id_user, id_genre, points) VALUES (%s, %s, %s);",
                (is_user, genre_id, 47))

            return {
                "info": False,
                'status': "All questions are gone. Earn extra points"
            }
    
    
    def put_answer(self, user_id, qustion_id, status):

        self.cursor.execute("INSERT INTO users_quiz (id_user, id_question, point) VALUES (%s, %s, %s);", (user_id, qustion_id, status))

        # query = """SELECT id, question, answer, correct_answer FROM question_db
        #            WHERE genre_id = %s
        #            AND id NOT IN (SELECT id_question FROM users_quiz WHERE id_user = %s)
        #            ORDER BY random() LIMIT 1;"""
        # genre_id = 0
        # is_user = 1
        # self.cursor.execute(query, (genre_id, is_user))
        # random_question = self.cursor.fetchone()
        # print(random_question)
        #
        # if random_question:
        #     return {
        #         "info": True,
        #         'question_id': random_question[0],
        #         'question': random_question[1],
        #         'answer': json.loads(random_question[2]),
        #         'correct_answer':random_question[3]
        #     }
        # else:
        #     return {
        #         "info": False,
        #         'status': "the questions are over"
        #     }

    
    def register_miro(self, name, video, data):
        self.cursor.execute("INSERT INTO events (name, video, data) VALUES (%s, %s, %s);", (name, video, data))
        # user_id = self.cursor.fetchone()[0]
        # return user_id


    def drop(self):
        self.cursor.execute("DROP TABLE IF EXISTS reg_for_event, quests_table, users_quiz, question_db, genre_table, events, users;")

    def close(self):
        self.db.commit()
        self.cursor.close()
        self.db.close()

    # cursor.execute("CREATE TABLE users3 (id SERIAL PRIMARY KEY, name VARCHAR(255));")
    # db.commit()
    # cursor.close()

    # Закрытие соединения
    # db.close()



def start_db():
    DBConnect().drop()
    db_conn = DBConnect()


    db_conn.register_user('Nikita')

    db_conn.register_new_genre('Безопасность')
    db_conn.register_new_genre('Политика компании')
    db_conn.register_new_genre('Безопасность')
    db_conn.register_new_genre('Интересы компании')



    db_conn.register_qustion('Что нельзя засовывать в розетку?', 1, json.dumps(['Чайник', "Принтер", "Пальцы", "Руки"]),
                             2, 1, 'foto/ava.jpg')

    db_conn.register_qustion('Вопрос 2', 1, json.dumps(['Чайник', "Принтер", "Пальцы", "Руки"]), 2,
                             1, 'foto/ava.jpg')

    db_conn.register_qustion('Вопрос 3', 1, json.dumps(['Чайник', "Принтер", "Пальцы", "Руки"]), 2,
                             1, 'foto/ava.jpg')

    db_conn.register_qustion('Вопрос 4', 1, json.dumps(['Чайник', "Принтер", "Пальцы", "Руки"]), 2,
                             1, 'foto/ava.jpg')

    db_conn.register_qustion('Вопрос 5', 1, json.dumps(['Чайник', "Принтер", "Пальцы", "Руки"]), 2,
                             1, 'foto/ava.jpg')

    db_conn.register_qustion('Что нельзя засовывать в розетку?', 2, json.dumps(['Чайник', "Принтер", "Пальцы", "Руки"]),
                             2, 1, 'foto/ava.jpg')

    db_conn.register_qustion('Вопрос 2', 2, json.dumps(['Чайник', "Принтер", "Пальцы", "Руки"]), 2,
                             1, 'foto/ava.jpg')

    db_conn.register_qustion('Вопрос 3', 2, json.dumps(['Чайник', "Принтер", "Пальцы", "Руки"]), 2,
                             1, 'foto/avajpg')

    db_conn.register_qustion('Вопрос 4', 2, json.dumps(['Чайник', "Принтер", "Пальцы", "Руки"]), 2,
                             1, 'foto/ava.jpg')

    db_conn.register_qustion('Вопрос 5', 2, json.dumps(['Чайник', "Принтер", "Пальцы", "Руки"]), 2,
                             1, 'foto/ava.jpg')

    db_conn.register_qustion('Что нельзя засовывать в розетку?', 3, json.dumps(['Чайник', "Принтер", "Пальцы", "Руки"]),
                             2, 1, 'foto/ava.jpg')

    db_conn.register_qustion('Вопрос 2', 3, json.dumps(['Чайник', "Принтер", "Пальцы", "Руки"]), 2,
                             1, 'foto/ava.jpg')

    db_conn.register_qustion('Вопрос 3', 3, json.dumps(['Чайник', "Принтер", "Пальцы", "Руки"]), 2,
                             1, 'foto/ava.jpg')

    db_conn.register_qustion('Вопрос 4', 3, json.dumps(['Чайник', "Принтер", "Пальцы", "Руки"]), 2,
                             1, 'foto/ava.jpg')

    db_conn.register_qustion('Вопрос 5', 3, json.dumps(['Чайник', "Принтер", "Пальцы", "Руки"]), 2,
                             1, 'foto/ava.jpg')

    db_conn.register_miro('Мир', 'video/mir.mp4', time.time() + 24 * 60 * 60 * 6)


if __name__ == '__main__':
    pass


    # status = 0
    # # status = 1
    #
    # if status:
    #
    #     pass
    #
    #
    #
    #
    # else:
    #     # db_conn.drop()
    #
    #
    # # db_conn.close()