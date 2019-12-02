from .worker import CelerySingleton

celery_app = CelerySingleton().get_celery()


@celery_app.task(name="add_two_numbers")
def add_two_numbers(x, y):
    return x + y
    