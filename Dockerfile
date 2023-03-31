FROM python:3.8

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

ENV FLASK_APP=app.py

EXPOSE 5000

# Запускаем команду для запуска Flask приложения внутри контейнера
CMD ["flask", "run", "--host=0.0.0.0"]
