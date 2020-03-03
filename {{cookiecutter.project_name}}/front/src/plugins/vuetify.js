import Vue from 'vue';
import Vuetify from 'vuetify/lib';

Vue.use(Vuetify);

export default new Vuetify({
  icons: {
    iconfont: 'mdi',
  },
  theme:{
    themes: {
      light: {
        primary: "#41B883",
        secondary: "#34495E",
        tertiary: "#42A5F5",
        error: '#ff7a73',
      }
    }
  }
});
