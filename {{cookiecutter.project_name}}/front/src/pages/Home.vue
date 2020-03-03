<template>
  <div class="main">
    {% raw %}
    <v-container fluid class="pa-0">
      <v-row no-gutters justify="center" align="center">

        <v-col cols="12">
          <welcome-screen></welcome-screen>
        </v-col>

        <v-col cols="12">
          <v-card class="elevation-0 mt-5" color="transparent">
            <v-card-text class="text-center display-1 font-weight-bold">
              Launch your app in less than an hour!
            </v-card-text>
            <v-card-text>
              <main-stack v-for="stack in mainStacks" :key="stack.name" :stack="stack"></main-stack>
            </v-card-text>
          </v-card>
        </v-col>

        <v-col cols="12">
          <v-parallax dark src="../assets/grey_background.jpeg" class="mb-5 slant" height="800">
            <v-container fluid>
              <v-row dense align="center" justify="center">
                <v-col cols="12" align-self="center" class="mb-5 pb-5">
                  <v-row justify="center" class="display-1">The backend stacks</v-row>
                </v-col>
                <v-col class="text-center mt-5" cols="2" v-for="stack in backendStacks" :key="stack.name">
                  <backend-stack :stack="stack"></backend-stack>
                </v-col>
              </v-row>
            </v-container>
          </v-parallax>
        </v-col>

        <v-col cols="12" style="margin-bottom: 5em">
          <v-card class="elevation-0 mt-5 mb-5" color="transparent">
            <v-card-text class="text-center display-1 font-weight-bold">
              Already secure
            </v-card-text>
            <v-row align="center" justify="center">
              <v-col cols="2" v-for="auth in auths">
                <auth-type :auth="auth"></auth-type>
              </v-col>
            </v-row>
          </v-card>
        </v-col>

      </v-row>
    </v-container>
    {% endraw %}
  </div>
</template>

<script>
  import WelcomeScreen from "../components/home/WelcomeScreen";
  import MainStack from "../components/home/MainStack";
  import BackendStack from "../components/home/BackendStack";
  import AuthType from "../components/home/AuthType";

  export default {
    name: 'Main',
    components: {AuthType, BackendStack, MainStack, WelcomeScreen},
    data() {
      return {
        mainStacks: [
          {
            name: 'VueJs',
            caption: 'VueJs for performance and handiness',
            description: 'An incrementally adoptable ecosystem that scales between a library and a full-featured framework',
            logo: require('../assets/logos/vue.png'),
            link: 'https://vuejs.org/',
            reverse: false
          },
          {
            name: 'Vuetify',
            caption: 'Vuetify for design and user experience',
            description: 'A Vue UI Library with beautifully handcrafted Material Components. No design skills required — everything you need to create amazing applications is at your fingertips',
            logo: 'https://cdn.vuetifyjs.com/images/logos/v-alt.svg',
            link: 'https://vuetifyjs.com/en/',
            reverse: true
          },
          {
            name: 'Flask',
            caption: 'Flask for speed and completeness',
            description: 'A well designed Python framework that offers a wide range of possibilities to build an efficient api that meets your needs',
            logo: 'http://flask.palletsprojects.com/en/1.1.x/_static/flask-icon.png',
            link: 'http://flask.palletsprojects.com/en/1.1.x/',
            reverse: false
          }
        ],
        backendStacks: [
          {
            name: 'Elasticsearch',
            description: 'You know, for search — and logging, and analytics, and more',
            logo: require('../assets/logos/elastic.png'),
            link: 'https://www.elastic.co/'
          },
          {
            name: 'PostgreSQL',
            description: 'The World\'s Most Advanced Open Source Relational Database',
            logo: require('../assets/logos/postgre.png'),
            link: 'https://www.postgresql.org/'
          },
          {
            name: 'Redis',
            description: 'An open source in-memory data structure store',
            logo: require('../assets/logos/redis.png'),
            link: 'https://redis.io/'
          },
          {
            name: 'Minio',
            description: 'A pioneering high performance object storage',
            logo: require('../assets/logos/minio.png'),
            link: 'https://min.io/'
          }
        ],
        auths: [
          {name: 'Facebook', logo: require('../assets/logos/facebook_blue.png')},
          {name: 'Google', logo: require('../assets/logos/google.png')},
          {name: 'Email', logo: require('../assets/logos/email.png')}
        ]
      }
    }
  }
</script>

<style scoped>
  .main{
    width: 100%;
    height: 100%
  }

  .slant {
    position: relative;
    overflow: hidden;
    z-index: 0;
    -webkit-clip-path: polygon(0 0, 100% 15%, 100% 80%, 0 100%);
    clip-path: polygon(0 0, 100% 15%, 100% 80%, 0 100%);
  }
</style>