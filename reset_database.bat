@ECHO off

del "db.sqlite3"
del "youtube\migrations\0001_initial.py"
del "feed\migrations\0001_initial.py"
python manage.py makemigrations youtube
python manage.py makemigrations feed
python manage.py migrate
python manage.py createsuperuser