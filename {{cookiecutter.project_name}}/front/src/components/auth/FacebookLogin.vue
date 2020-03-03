<template>
    <div>
        {% raw %}
        <v-btn block class="login" @click="login()" color="#3B5998">
            <img src="../../assets/logos/facebook.png" alt="facebook-login-icon" class="facebook-logo">
            <v-spacer style="max-width: 8%"></v-spacer>
            Log in with Facebook
        </v-btn>
        {% endraw %}
    </div>
</template>

<script>
    import auth from "@/modules/auth";

    export default {
        name: "FacebookLogin",
        methods: {
            login() {
                auth.loginWithFacebook()
            }
        }
    }
</script>

<style scoped>
    .login {
        text-transform: None !important;
        color: white
    }

    .facebook-logo {
        width: 24px;
    }
</style>