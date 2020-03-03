import Vue from "vue";
import App from "./App";
import axios from "axios";

import vuetify from './plugins/vuetify';
import router from "./modules/router";
import auth from "./modules/auth";
import notifications from "./modules/notifications";

Vue.config.productionTip = process.env.NODE_ENV === "production";
axios.defaults.withCredentials = true;


new Vue({
  router,
  vuetify,
  render: h => h(App)
}).$mount('#app');


Vue.mixin({
  data() {
    return {
      $_profile: auth.user.profile
    }
  }
});

axios.interceptors.response.use(
  response => response,
  error => {
    if (error.response.status === 401) {
      notifications.addNotification('Session expired');
      auth.logout()
    }
    return Promise.reject(error);
  }
);
