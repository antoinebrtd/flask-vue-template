<template>
    <div>
        {% raw %}
        <v-btn outlined block class="login" @click="login()">
            <img src="../../assets/logos/google.png" alt="google-login-icon" class="google-logo">
            <v-spacer style="max-width: 8%"></v-spacer>
            Log in with Google
        </v-btn>
        {% endraw %}
    </div>
</template>

<script>
    import auth from "@/modules/auth";

    export default {
        name: "GoogleLogin",
        methods: {
            login() {
                auth.loginWithGoogle();
            }
        }
    }
</script>

<style scoped>
    .login {
        text-transform: None !important;
    }

    .google-logo {
        width: 28px;
     }
</style>