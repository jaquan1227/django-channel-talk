for run server

pip install -r requirements.txt

python manage.py makemigrations

python manage.py migrate

in urls.py add this line

expire_checker(100,repeat=10, repeat_until=None) #first arg is ttl (sec) for message, and every 10 sec checkit, 

run redis (port : 6379)

python manage.py process_tasks &

python manage.py runserver

APIDOC: https://goo.gl/hvQo5T

to make admin user

python manage.py createsuperuser