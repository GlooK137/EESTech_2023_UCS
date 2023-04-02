import json
import os
import time

import psycopg2
import config




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
            CREATE TABLE IF NOT EXISTS logs (
            id SERIAL PRIMARY KEY,
            user_id INTEGER REFERENCES users(id),
            log_txt TEXT,
            log_time INTEGER
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


    # Регистрация юзера
    def register_user(self, name):
        self.cursor.execute("INSERT INTO users (name) VALUES (%s);", (name,))

        self.cursor.execute("SELECT id FROM users")
        user_id = self.cursor.fetchall()[-1][0]
        # логи юзера
        self.cursor.execute("INSERT INTO logs (user_id, log_txt, log_time) VALUES (%s, %s, %s);", (
            user_id,
            'Создание аккаунта',
            time.time()
        ))
        return user_id



    # Регистрация юзера на мероприятие
    def register_miro_user(self, id_user, id_event):
        self.cursor.execute("INSERT INTO reg_for_event (id_user, id_event) VALUES (%s, %s);", (id_user, id_event))
        self.cursor.execute("INSERT INTO logs (user_id, log_txt, log_time) VALUES (%s, %s, %s);", (
            id_user,
            f'Регистрация на мероприятие {id_event}',
            time.time()
        ))



    # Запрос баллов юзера
    def cash(self, user_id):
        # Запрос баллов за викторину
        self.cursor.execute("SELECT SUM(point)*7 FROM users_quiz WHERE id_user=%s;", (user_id,))
        quests = self.cursor.fetchone()[0]
        print(quests)
        if quests:
            quests = quests
        else:
            quests = 0

        # Баллы за полностью пройденную тему
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


    # Запрос тем для викторины
    def genre_get(self):

        self.cursor.execute("SELECT * FROM genre_table;")
        data = self.cursor.fetchall()
        out = {}
        for key, element in data:
            out[key] = element

        return out


    # Запррос мироприятий
    def miro_get(self):

        self.cursor.execute("SELECT * FROM events;")
        data = self.cursor.fetchall()
        out = {}
        for key, name, video, date in data:
            out[key] = {
                "id_event": key,
                "name":name,
                "video":video,
                "date": date
            }

        return out



    # Запрос логов юзера
    def get_logs(self, user_name):

        self.cursor.execute("SELECT log_txt, log_time FROM logs WHERE user_id=%s;", (user_name))
        data = self.cursor.fetchall()
        out = []
        for log_txt, log_time in data:
            out.append({
                "log_txt": log_txt,
                "log_time":log_time
            })

        return out



    # Регистрация юзера на мероприятие
    def register_new_genre(self, new_genre):
        self.cursor.execute("""INSERT INTO genre_table (genre) 
                SELECT %s 
                WHERE NOT EXISTS (
                  SELECT 1 FROM genre_table WHERE genre = %s
                );
                """, (new_genre,new_genre))



    # Создание нового вопроса для викторины
    def register_qustion(self, question, genre_id, answer, correct_answer, points, foto):
        """
        :param question: Вопрос
        :param genre_id: id темы
        :param answer: ответы
        :param correct_answer: индекс верного ответа
        :param points: баллы
        :param foto: ссылка на фото
        :return: None
        """
        self.cursor.execute("INSERT INTO question_db (question, genre_id, answer, correct_answer, points, foto) VALUES (%s, %s, %s, %s, %s, %s);", (question, genre_id, answer, correct_answer, points, foto))
        # user_id = self.cursor.fetchone()[0]
        # return user_id



    # Запрос нового вопроса для викторины. Выдает рандомный, а также тот что юзер еще не решал
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

            self.cursor.execute("INSERT INTO logs (user_id, log_txt, log_time) VALUES (%s, %s, %s);", (
                is_user,
                'Награда за решение группы заданий',
                time.time()
            ))

            return {
                "info": False,
                'status': "All questions are gone. Earn extra points"
            }




    # Запись ответа юзера
    def put_answer(self, user_id, qustion_id, status):

        self.cursor.execute("INSERT INTO users_quiz (id_user, id_question, point) VALUES (%s, %s, %s);", (user_id, qustion_id, status))
        # Логи юзера
        self.cursor.execute("INSERT INTO logs (user_id, log_txt, log_time) VALUES (%s, %s, %s);", (
            user_id,
            f'Ответ на вопрос {qustion_id}. Результат {bool(status)}',
            time.time()
        ))

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



    # Создание нового мероприятия
    def register_miro(self, name, video, data):
        self.cursor.execute("INSERT INTO events (name, video, data) VALUES (%s, %s, %s);", (name, video, data))
        # user_id = self.cursor.fetchone()[0]
        # return user_id


    # Удаление всех таблиц
    def drop(self):
        self.cursor.execute("DROP TABLE IF EXISTS reg_for_event CASCADE; DROP TABLE IF EXISTS logs CASCADE; DROP TABLE IF EXISTS quests_table CASCADE; DROP TABLE IF EXISTS users_quiz CASCADE; DROP TABLE IF EXISTS question_db CASCADE; DROP TABLE IF EXISTS genre_table CASCADE; DROP TABLE IF EXISTS events CASCADE; DROP TABLE IF EXISTS users CASCADE;")



    # Закрытие соединения с сервером
    def close(self):
        self.db.commit()
        self.cursor.close()
        self.db.close()

    # cursor.execute("CREATE TABLE users3 (id SERIAL PRIMARY KEY, name VARCHAR(255));")
    # db.commit()
    # cursor.close()

    # Закрытие соединения
    # db.close()


# Создание тестовых данных в базе
def start_db():
    DBConnect().drop() # Чистим базу
    db_conn = DBConnect() # Инициализация и создание таблиц


    # Регистрация юзера Nikita
    db_conn.register_user('Nikita')


    # Регистрация тем для викторин
    db_conn.register_new_genre('Безопасность')
    db_conn.register_new_genre('Политика компании')
    db_conn.register_new_genre('Безопасность')
    db_conn.register_new_genre('Интересы компании')



    # регистрация вопросов
    # первый пункт - сам вопрос
    # 2 - id группы genre
    # 3 - Варианты ответов
    # 4 - верный ответ
    # 5 - колличиство баллов за ответ (сейчас сделан 1 балл, так как одна звезда. Но при расчете балоов считается как 7)
    # 6 - ссылка на фото
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




    # Регистрация мероприятия
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
