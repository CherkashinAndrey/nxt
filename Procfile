#web: /home/user/work_files/NXT_LVL/venv/bin/python manage.py runserver
#web: /usr/bin/gunicorn NXT.wsgi:application --pythonpath /home/user/work_files/NXT_LVL/venv/lib/python2.7/site-packages/ --log-file -
web: gunicorn NXT.wsgi_wn:application --log-file - --timeout 30 --graceful-timeout 30
worker: celery -A NXT worker -l debug