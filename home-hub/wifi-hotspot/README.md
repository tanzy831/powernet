# How to run WiFi portal

Python 2.7 and Django 1.11 is used for this portal.

```
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver 0.0.0.0:8000
```
The WiFi portal will be available at port 8000.
