<template>
    <div class="my-account">
        {% raw %}
        <v-img src="../assets/grey_background.jpeg" alt="background" class="background"></v-img>
        <v-container class="container" v-if="loaded">
            <modify-account
                    v-if="$data.$_profile.id.toString() === $route.params.id"
                    :user="user"
                    @update="updateUser"
            ></modify-account>
            <view-account
                    v-else
                    :user="user"
            ></view-account>
        </v-container>
        {% endraw %}
    </div>
</template>

<script>
    import axios from 'axios';
    import notifications from '@/modules/notifications';
    import auth from '@/modules/auth';
    import ModifyAccount from "../components/account/ModifyAccount";
    import ViewAccount from "../components/account/ViewAccount";

    export default {
        name: "Account",
        components: {ViewAccount, ModifyAccount},
        data() {
            return {
                loaded: false,
                user: null
            }
        },
        mounted() {
            this.getUser()
        },
        methods: {
            getUser() {
                axios.get(process.env.VUE_APP_API_URL + `/users/${this.$route.params.id}`).then(response => {
                    if (response.data.msg === 'success') {
                        this.user = response.data.user;
                        this.loaded = true
                    }
                }).catch(error => {
                    if (error.response) {
                        notifications.addNotification(error.response.data.error);
                    } else {
                        notifications.addNotification('We\'re sorry, an error occurred')
                    }
                })
            },
            updateUser(user) {
                this.user = user;
                auth.getUserInfo()
            }
        }
    }
</script>

<style scoped>
    .my-account {
        width: 100%;
        text-align: center;
        height: 100%;
        padding-top: 60px;
    }

    .container {
        width: 100%;
        text-align: center;
        height: 100%;
    }

    .background {
        width: 100vw;
        margin: auto;
        height: 100vh;
        opacity: 1;
        position: fixed;
        top: 0
    }
</style>