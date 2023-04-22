web: gunicorn --pythonpath ims ims.wsgi --log-file -
worker: celery -A ims.ims worker --loglevel=info
celery_beat: celery -A ims.ims beat --loglevel=info
