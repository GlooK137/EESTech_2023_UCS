from flask import Flask, render_template, request, jsonify, send_from_directory
import json
import DB
import os

DB.start_db()

db_connect = DB.DBConnect()

app = Flask(__name__, static_folder='video')

@app.route('/')
def index():
    return """API"""



@app.route('/register', methods=['POST'])
def register():
    user_name = request.form.get('name')
    print(user_name)
    db_connect.register_user(user_name)
    # return jsonify({'user_id': user_id})
    return jsonify({"out":True})



@app.route('/genre', methods=['GET'])
def genre_get():
    data = db_connect.genre_get()
    # return jsonify({'user_id': user_id})
    return jsonify(data)


@app.route('/question', methods=['POST'])
def question():
    user_id = request.form.get('user_id')
    genre_id = request.form.get('genre_id')

    rez = db_connect.get_question(user_id, genre_id)
    # print(user_name)
    # db_connect.register_user(user_name)z
    # return jsonify({'user_id': user_id})
    return jsonify(rez)




@app.route('/cash', methods=['POST'])
def cash():
    user_id = request.form.get('user_id')

    rez = db_connect.cash(user_id)
    # print(user_name)
    # db_connect.register_user(user_name)z
    # return jsonify({'user_id': user_id})
    return jsonify(rez)


@app.route('/answer', methods=['POST'])
def answer():
    user_id = request.form.get('user_id')
    qustion_id = request.form.get('qustion_id')
    answer = request.form.get('answer')
    correct_answer = request.form.get('correct_answer')

    if answer == correct_answer:
        status = 1
    else:
        status = 0

    rez = db_connect.put_answer(user_id, qustion_id, status)
    # print(user_name)
    # db_connect.register_user(user_name)z
    # return jsonify({'user_id': user_id})
    return jsonify({'status': status})





@app.route('/videos/<path:filename>')
def download_file_video(filename):
    # Получаем путь к файлу из переменной окружения BASE_DIR
    directory = os.environ.get('BASE_DIR', '/path/to/your/app')
    # Объединяем путь к директории с видео и запрашиваемое имя файла
    path = os.path.join(directory, 'video', filename)
    # Используем функцию send_from_directory для отправки файла пользователю
    return send_from_directory(directory=path, filename=filename)



@app.route('/foto/<path:filename>')
def download_file_foto(filename):
    # Получаем путь к файлу из переменной окружения BASE_DIR
    directory = os.environ.get('BASE_DIR', '/path/to/your/app')
    # Объединяем путь к директории с видео и запрашиваемое имя файла
    path = os.path.join(directory, 'video', filename)
    # Используем функцию send_from_directory для отправки файла пользователю
    return send_from_directory(directory=path, filename=filename)


if __name__ == '__main__':
    try:
        app.run(debug=True)
    except Exception as ex:
        print(ex)
    finally:
        db_connect.close()
