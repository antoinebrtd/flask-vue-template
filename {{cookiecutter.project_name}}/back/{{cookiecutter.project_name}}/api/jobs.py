from flask_restful import Resource
from rq.registry import StartedJobRegistry, FailedJobRegistry

from {{cookiecutter.project_name}}.api import api
from {{cookiecutter.project_name}}.auth import authenticated
from {{cookiecutter.project_name}}.core import queue, broker


class Jobs(Resource):
    @authenticated
    def get(self):
        pending = queue.get_job_ids()

        registry = StartedJobRegistry('default', connection=broker)
        started = registry.get_job_ids()

        fail_queue = FailedJobRegistry(connection=broker)
        failed = fail_queue.get_job_ids()

        return {"jobs": started + pending, "failed": failed}


class Job(Resource):
    @authenticated
    def get(self, job_id):
        job = queue.fetch_job(job_id)
        answer = {"failed": job.is_failed, "meta": job.meta}
        if job.is_failed and job.exc_info is not None:
            answer['error'] = 'Error: {}'.format(job.exc_info.split('\n')[-2])
        return answer


api.add_resource(Jobs, '/jobs')
api.add_resource(Job, '/jobs/<job_id>')
