# Crazy Crane

## Setup
1. Create `.env` from `.env.Exmaple`
2. `pip install -r requirements.txt`

## .env
1. `TELEGRAM_TOKEN` - Get token from [BotFather](https://t.me/botfather)

## Run
### Bot
```
python manage.py migrate
python manage.py bot
```
### Django admin
### First run
```
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```
### Common run
```
python manage.py migrate
python manage.py runserver
```