<template>
  <div class="login" v-if="loaded">
    {% raw %}
    <v-img src="../../assets/grey_background.jpeg" alt="banner" class="banner"></v-img>
    <v-container class="login">
      <v-layout row justify-center align-center fill-height>
        <v-flex xs12 sm6>
          <v-hover v-slot:default="{ hover }">
              <v-card flat id="card" class="pa-5 expand-transition" :elevation="hover ? 12 : 5">
                <v-card-text class="title">Log in or sign up to explore!</v-card-text>
                <v-card-text primary-title>
    {% endraw %}
    {%- if cookiecutter.email_login == 'y' %}
                  <email-login :token="$route.params.token"></email-login>
    {%- endif %}
    {%- if cookiecutter.email_login == 'y' and (cookiecutter.google_login == 'y' or cookiecutter.facebook_login == 'y') %}
                  <v-card-text class="mt-2">
                    <span>Or</span>
                  </v-card-text>
    {%- endif %}
    {%- if cookiecutter.google_login == 'y' %}
                  <google-login></google-login>
    {%- endif %}
    {%- if cookiecutter.facebook_login == 'y' %}
                  <facebook-login class="mt-3"></facebook-login>
    {%- endif %}
    {% raw %}
                </v-card-text>
              </v-card>
          </v-hover>
        </v-flex>
      </v-layout>
     </v-container>
    {% endraw %}
  </div>
</template>

<script>
  import auth from "@/modules/auth";
  import GoogleLogin from "../../components/auth/GoogleLogin";
  import EmailLogin from "../../components/auth/EmailLogin";
  import FacebookLogin from "../../components/auth/FacebookLogin";

  export default {
    name: 'Login',
    components: {FacebookLogin, EmailLogin, GoogleLogin},
    data() {
      return {
        loaded: false,
        token: this.$route.params.token
      }
    },
    created() {
      auth.checkAuth().then(() => {
        if (this.$route.params.token) {
          auth.activateAccount(this.$route.params.token).then(() => {
            this.$router.replace('/home');
          }).catch(error => {
            this.$router.replace('/home');
          })
        } else {
          this.$router.replace('/home');
        }
      }).catch(() => {
        this.loaded = true;
      });
    }
  }
</script>

<style scoped>
  .login {
    width: 100%;
    text-align: center;
    height: 100%
  }

  #card {
    margin: 0 5em 0 5em;
    border-radius: 8px;
    background-color: rgba(255, 255, 255, 0.70);
  }

  .banner {
    width: 100vw;
    margin: auto;
    position: fixed;
    height: 100vh;
    top: 0
  }
</style>