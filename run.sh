#!/bin/bash


 python manage.py makemigrations
 python manage.py migrate
 python manage.py createsuperuser --username USER1 --email 'anya.starovoytova@inbox.ru' --noinput
exec python manage.py runserver 0.0.0.0:8000