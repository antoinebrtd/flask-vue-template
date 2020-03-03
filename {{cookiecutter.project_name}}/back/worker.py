from rq.worker import Worker

from {{cookiecutter.project_name}} import create_app
from {{cookiecutter.project_name}}.core import db


class AdvancedWorker(Worker):
    def __init__(self, *args, **kwargs):
        self.app = create_app(api=False)
        super(AdvancedWorker, self).__init__(*args, **kwargs)

    def work(self, *args, **kwargs):
        with self.app.app_context():
            return super(AdvancedWorker, self).work(*args, **kwargs)

    @db.connection_context()
    def execute_job(self, *args, **kwargs):
        return super(AdvancedWorker, self).execute_job(*args, **kwargs)
