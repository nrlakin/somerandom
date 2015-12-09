#!venv/bin/python
from celery import Celery
from datetime import timedelta
from app import app

CELERYBEAT_SCHEDULE = {
    'update_followers': {
        'task': 'somerando.follow_back',
        'schedule' : timedelta(seconds=30),
        'args' : ()
    }
}
def make_celery(app):
    celery = Celery(app.import_name, broker=app.config['CELERY_BROKER_URL'])
    celery.conf.update(app.config)
    return celery
    # TaskBase = celery.Task
    # class ContextTask(TaskBase):
    #     abstract = True
    #     def __call__(self, *args, **kwargs):
    #         with app.app_context():
    #             return TaskBase.__call__(self, *args, **kwargs)
    #     celery.Task = ContextTask
    #     return celery
