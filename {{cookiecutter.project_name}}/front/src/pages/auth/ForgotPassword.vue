<template>
    <div class="forgot-password">
        {% raw %}
        <v-img src="../../assets/grey_background.jpeg" alt="banner" class="banner"></v-img>
        <v-container class="forgot-password">
            <v-layout row justify-center align-center fill-height>
                <v-flex xs12 sm6>
                    <v-hover v-slot:default="{ hover }">
                        <v-card flat id="card" class="pa-5 expand-transition" :elevation="hover ? 12 : 5">
                            <v-card-text class="subtitle-1 pt-2 pb-0">Send instructions to:</v-card-text>
                            <v-card-text primary-title class="pt-2 pb-0 mb-2">
                                <v-form ref="form" lazy-validation>
                                    <v-text-field
                                            :rules="[rules.emptyEmail, rules.emailNotValid]"
                                            outline
                                            label="Email"
                                            append-icon="mail"
                                            v-model="email"
                                            required
                                    ></v-text-field>
                                </v-form>
                            </v-card-text>
                            <v-card-text class="mt-5">
                                <v-layout row>
                                    <v-btn class="button mx-3" to="/login" color="error" text>Cancel</v-btn>
                                    <v-spacer></v-spacer>
                                    <v-btn class="button mx-3" @click="validate()" color="primary">Send</v-btn>
                                </v-layout>
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
    import axios from 'axios';
    import notifications from '@/modules/notifications'

    export default {
        name: "ForgotPassword",
        data() {
            return {
                email: null,
                rules: {
                    emptyEmail: v => !!v || 'Please enter your email',
                    emailNotValid: v => /.+@.+/.test(v) || 'This email is not valid',
                }
            }
        },
        watch: {
            email() {
                this.$refs.form.resetValidation();
            }
        },
        methods: {
            validate() {
                if (this.$refs.form.validate()) {
                    axios.post(process.env.VUE_APP_EMAIL_AUTH_URL + '/forgot-password', {email: this.email})
                        .then(response => {
                            notifications.addNotification(response.data);
                            this.$router.replace('/')
                        })
                        .catch(error => {
                            notifications.addNotification('An error occurred')
                        })
                }
            }
        }
    }
</script>

<style scoped>
    .forgot-password {
        width: 100%;
        height: 100%
    }

    #card {
        margin: 4em;
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

    .button {
        text-transform: None !important;
    }
</style>