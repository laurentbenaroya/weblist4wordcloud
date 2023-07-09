FROM arm32v7/python:3.7.10-buster

COPY . /app

RUN pip install --upgrade pip

# next line is probably unecessary
COPY requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip install Flask-Caching==2.0.2
RUN pip install --index-url=https://www.piwheels.org/simple --no-cache-dir -r requirements.txt

RUN apt update
RUN apt -y install libatlas-base-dev

EXPOSE 8080

CMD ["gunicorn", "--bind", "0.0.0.0:8080", "main_basic:app", "--access-logfile", "./log_gunicorn/access.log", "--workers", "1"]
