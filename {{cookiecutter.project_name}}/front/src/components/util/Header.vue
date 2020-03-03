<template>
  <div class="header">
    {% raw %}
    <v-toolbar fixed :class="transparentHeader ? 'menu-header-transparent elevation-0' : 'menu-header elevation-5'">

      <v-toolbar-items>
        <router-link to="/home" class="px-3 py-2">
          <v-img src="../../assets/logos/vue.png" alt="logo" class="logo"></v-img>
        </router-link>
      </v-toolbar-items>

      <v-spacer></v-spacer>

      <v-toolbar-items v-if="$data.$_profile">
        <v-scroll-x-reverse-transition v-for="link in links" :key="link.text">
          <v-btn
                  v-if="displayMenu"
                  text
                  class="px-4 main-menu pt-1"
                  :to="link.route"
                  :class="transparentHeader ? 'white--text' : ''"
                  :color="$route.path === link.route ? 'tertiary' : ''"
          >
            {{ link.text }}
          </v-btn>
        </v-scroll-x-reverse-transition>
        <v-scroll-x-reverse-transition>
          <v-btn
                  v-if="displayMenu"
                  class="px-4 main-menu pt-1"
                  color="primary"
                  to="/Contact"
                  text>
            Contact
          </v-btn>
        </v-scroll-x-reverse-transition>
      </v-toolbar-items>

      <v-toolbar-items class="pr-4 ml-2">
        <profile-menu :transparentHeader="transparentHeader"></profile-menu>
      </v-toolbar-items>
    </v-toolbar>

    <jobs v-if="jobs"></jobs>

    <v-snackbar v-model="activationReminder" :timeout="0" color="primary">
      Seems like you haven't activated your account yet!
      <v-btn text @click="resendEmail" style="text-transform: none; text-decoration: underline">Resend email</v-btn>
      <v-tooltip right>
        <template v-slot:activator="{ on }">
          <v-btn color="primary" text icon @click="activationReminder = false" v-on="on">
            <v-icon color="white">clear</v-icon>
          </v-btn>
        </template>
        <span>Close</span>
      </v-tooltip>
    </v-snackbar>
    {% endraw %}
  </div>
</template>

<script>
  import axios from 'axios';
  import notifications from "@/modules/notifications";
  import auth from "@/modules/auth";


  import Jobs from './Jobs';
  import ProfileMenu from "./ProfileMenu";

  export default {
    name: 'Header',
    components: {ProfileMenu, Jobs},
    data() {
      return {
        user: auth.user,
        jobs: false,
        activationReminder: false,
        scrolled: false,
        displayMenu: false,
        links: [
          {text: 'Api', route: '/api'},
          {text: 'On PyCharm', route: '/pycharm'},
          {text: 'About your app', route: '/about'},
        ]
      }
    },
    computed: {
      transparentHeader() {
        return !this.scrolled;
      }
    },
    created() {
      window.addEventListener('scroll', this.handleScroll);
    },
    mounted() {
      if (!this.user.accountActivated && !this.user.firstLogin) {
        setTimeout(() => this.activationReminder = true, 5000)
      }
      setTimeout(() => this.displayMenu = true, 200)
    },
    destroyed() {
      window.removeEventListener('scroll', this.handleScroll);
    },
    methods: {
      resendEmail() {
        this.activationReminder = false;
        axios.post(process.env.VUE_APP_EMAIL_AUTH_URL + '/resend-email').then(response => {
          notifications.addNotification(response.data)
        }).catch(error => {
          notifications.addNotification(error.response.data.error)
        })
      },
      handleScroll() {
        this.scrolled = window.scrollY > 10;
      }
    }
  }
</script>

<style scoped>
  .menu-header {
    position: fixed;
    top: 0;
    z-index: 15;
    width: 100%
  }

  .menu-header-transparent {
    position: fixed;
    top: 0;
    z-index: 15;
    background: transparent !important;
    width: 100%
  }
  .logo {
    height: 50px;
    width: 60px
  }

  .main-menu {
    transition: all 0.5s ease;
    text-transform: none !important;
  }
</style>

<style>
  .v-toolbar__content {
    padding: 0 !important;
  }

  .v-btn--active::before {
    opacity: 0 !important;
  }
</style>
