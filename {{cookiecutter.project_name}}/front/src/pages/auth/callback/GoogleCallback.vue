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

  export default {
    name: 'GoogleCallback',
    mounted() {
      const code = this.$route.query.code;
      const state = this.$route.query.state;
      auth.authorizeGoogle(code, state);
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