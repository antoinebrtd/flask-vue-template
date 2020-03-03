 import axios from 'axios';

let store = {
  jobs: []
};

function addJob(job_id)  {
  return new Promise(function(resolve) {
    let job = {};
    job.id = job_id;
    job.progress = 0;
    job.title = 'Waiting for job';
    job.interval = setInterval(() => {
      getJob(job).then((job) => {
        if (job.meta.progress >= 100) {
          resolve(job);
        }
      });
    }, 2000);

    store.jobs.push(job);
  });
}

function getJob(job) {
  return new Promise(function(resolve) {
    axios.get(process.env.VUE_APP_API_URL + '/jobs/' + job.id).then((response) => {
      let progress = response.data.meta.progress;
      if (progress > 0) {
        job.progress = progress;
        job.title = response.data.meta.title;
        job.color = 'primary';
      } else {
        job.progress = 0;
        job.title = 'Waiting for job';
      }

      if (job.progress >= 100) {
        clearInterval(job.interval);
        job.title = 'Finished';
        setTimeout(() => {
          removeJob(job)
        }, 5000);
      }

      if (response.data.failed) {
        clearInterval(job.interval);
        job.title = 'Failed';
        job.color = 'error';
      }

      resolve(response.data);
    });
  });
}

function removeJob(job) {
  clearInterval(job.interval);
  store.jobs = store.jobs.filter(j => j !== job);
}

function removeAllJobs() {
  store.jobs.forEach((job) => {
    clearInterval(job.interval);
  });
  store.jobs = [];
}

function getJobs() {
  axios.get(process.env.VUE_APP_API_URL + '/jobs').then((response) => {
    store.jobs = [];
    response.data.jobs.forEach((job_id) => {
      addJob(job_id);
    });
  });
}

function retrieveJobById(job_id) {
  return store.jobs.find(j => j.id === job_id);
}

export default {
  addJob,
  getJob,
  getJobs,
  removeAllJobs,
  retrieveJobById,
  store
}