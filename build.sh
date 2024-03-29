#!/usr/bin/env bash
# exit on error
set -o errexit
python -m pip install --upgrade pip

python -m pip install -r requirements.txt
python -m pip install --force-reinstall -U setuptools

python manage.py collectstatic --no-input
python manage.py makemigrations
python manage.py migrate

#python manage.py starter --username caio --password oficinag3 --noinput --email caiomarinho8@gmail.com
#python manage.py starter --username admin --password Admin123! --noinput --email admin@gmail.com
#python manage.py starter --username araly --password ciacimento --noinput --email ciadocimento@gmail.com