from celery import Celery

class CelerySingleton:
    celery = None
    def __init__(self, app = None):
        if CelerySingleton.celery is None:
            CelerySingleton.celery = Celery(
                app.import_name,
                broker = app.config["BROKER_URI"],
                results = app.config["BROKER_URI"]
            )

            class ContextClass(CelerySingleton.celery.Task):
                def __call__(self, *args,**kwargs):
                    with app.app_context():
                        return self.run(*args, **kwargs)
            
            CelerySingleton.celery.Task = ContextClass
            print(CelerySingleton.celery)
    
    def get_celery(self):
        return self.celery