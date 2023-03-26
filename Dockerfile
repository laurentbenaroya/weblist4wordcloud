FROM python:3.7.3

COPY . /app

RUN pip install matplotlib pandas pdfminer nltk textblob wordcloud flask flask-session Flask-Caching redis werkzeug numpy wordcloud

WORKDIR /app

EXPOSE 8080

CMD ["python", "gunicorn", "--bind", "0.0.0.0:8080", "main_basic:app", "--access-logfile", "./log_gunicorn/access.log", "--workers", "1"]
