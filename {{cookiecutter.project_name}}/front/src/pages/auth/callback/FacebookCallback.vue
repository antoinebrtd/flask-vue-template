<template>
  <div class="callback">
    {% raw %}
    <v-container class="text-xs-center" style="height: 100%">
      <v-layout row justify-center fill-height align-center>
        <v-img src="../../../assets/grey_background.jpeg" alt="banner" class="banner"></v-img>
        <v-progress-circular indeterminate color="primary"></v-progress-circular>
      </v-layout>
    </v-container>
    {% endraw %}
  </div>
</template>

<script>
  import auth from "@/modules/auth";
  import router from "@/modules/router";
  import notifications from "@/modules/notifications";

  export default {
        name: 'FacebookCallback',
        mounted() {
            const code = this.$route.query.code;
            const error = this.$route.query.error;
            if (!error) {
                auth.authorizeFacebook(code);
            } else if (error === 'access_denied') {
                router.replace('/')
            } else {
                notifications.addNotification('This link is invalid or has expired. Please try again');
                router.replace('/')
            }
        }
    }
</script>

<style scoped>
  .callback {
    width: 100%;
    height: 100%
  }

  .banner {
    width: 100vw;
    margin: auto;
    position: fixed;
    height: 100vh;
    top: 0
  }
</style>