<template>
  <div class="jobs">
    {% raw %}
    <v-snackbar v-model="jobs_store.jobs.length > 0" bottom :timeout="0" multi-line class="snackbar-progress">
      <v-layout row wrap>
        <div v-for="job in jobs_store.jobs" :key="job.id" class="jobs-progress">
          <v-flex xs6 class="job-title">
            {{ job.title }}
          </v-flex>
          <v-flex xs6>
            <v-progress-linear v-model="job.progress" :indeterminate="job.progress < 0" :color="job.color">
            </v-progress-linear>
          </v-flex>
        </div>
      </v-layout>
    </v-snackbar>
    {% endraw %}
  </div>
</template>


<script>
  import auth from "@/modules/auth";
  import jobs from '@/modules/jobs';


  export default {
    name: 'Jobs',
    data() {
      return {
        jobs_store: jobs.store,
      }
    },
    mounted() {
      auth.checkAuth().then(() => {
        jobs.getJobs();
      }).catch(error => {
        auth.logout()
      });
    },
    beforeDestroy() {
      jobs.removeAllJobs();
    }
  }
</script>

<style>
  .snackbar-progress {
    bottom: -40px !important;
    height: 48px !important;
    transition: all 0.5s ease;
  }

  .snackbar-progress:hover {
    bottom: 0 !important;
    height: auto !important;
  }

  .snackbar-progress .v-snack__wrapper {
    width: 100%;
  }

  .snackbar-progress .v-snack__content {
    height: auto !important;
    flex-wrap: wrap;
  }

  .v-snack {
    transition: all 0.5s ease;
  }

  .v-snack-transition-leave-to.v-snack.v-snack--bottom {
    bottom: -70px !important;
    transform: none !important;
  }

  .jobs-progress {
    width: 100%;
    display: flex;
  }

  .job-title {
    margin: auto;
  }
</style>