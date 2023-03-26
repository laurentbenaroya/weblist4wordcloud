FROM python:3.7.3

COPY . /app

RUN pip install --upgrade pip

RUN pip install -r requirements.txt
# RUN pip install matplotlib wordcloud flask Flask-Caching redis werkzeug numpy gunicorn

WORKDIR /app

EXPOSE 8080

CMD ["python", "gunicorn", "--bind", "0.0.0.0:8080", "main_basic:app", "--access-logfile", "./log_gunicorn/access.log", "--workers", "1"]
