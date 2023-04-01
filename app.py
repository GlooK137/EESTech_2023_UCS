from flask import Flask, render_template, request, jsonify, send_from_directory
import json
import DB
import os

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

@app.route('/question', methods=['POST'])
def question():
    user_id = request.form.get('user_id')
    genre_id = request.form.get('genre_id')

    rez = db_connect.get_question(user_id, genre_id)
    # print(user_name)
    # db_connect.register_user(user_name)
    # return jsonify({'user_id': user_id})
    return jsonify(rez)


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
