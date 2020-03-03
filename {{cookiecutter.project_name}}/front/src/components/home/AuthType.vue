<template>
    {% raw %}
    <v-card color="transparent" elevation="0">
        <v-layout justify-center column align-center>
            <v-card-text class="title font-weight-bold text-center primary--text">
                {{ auth.name }} login
            </v-card-text>
            <v-img :src="auth.logo" alt="vue" class="logo"></v-img>
        </v-layout>
    </v-card>
    {% endraw %}
</template>

<script>
    export default {
        name: "AuthType",
        props: {
            auth: Object
        }
    }
</script>

<style scoped>
    .logo {
        width: 40px;
        height: 40px
    }
</style>