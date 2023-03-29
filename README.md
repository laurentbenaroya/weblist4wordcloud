# Générer des nuages de mots à partir d'une liste qui est entrée par l'utilisateur

## docker 
$ docker build -t myapp .
$ docker run -p 8080:8080 -d myapp
the -d permits to detach the docker (stop with docker stop). -p permits to create a bound between the inside and the outside ports of docker container
to see active process
$ docker ps

## set server
$ sudo apt install nginx
$ sudo nano /etc/nginx/sites-available/weblist4wordcloud
$ sudo ln -s /etc/nginx/sites-available/weblist4wordcloud /etc/nginx/sites-enabled
$ sudo nginx -t
$ sudo nano /etc/nginx/nginx.conf
$ sudo nginx -t
$ sudo service nginx restart

 server {
    listen 80;
    server_name muysiteurl.xxx;
    location / {
        proxy_pass http://127.0.0.1:8080;
    }
}

run locally
$ gunicorn --bind 0.0.0.0:8080 main_basic:app --access-logfile ./log_gunicorn/access.log --workers 1
 