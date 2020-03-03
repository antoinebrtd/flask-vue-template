<template>
    <div class="reset-password" v-if="loaded">
        {% raw %}
        <v-img src="../../assets/grey_background.jpeg" alt="banner" class="banner"></v-img>
        <v-container class="reset-password">
            <v-layout row justify-center align-center fill-height>
                <v-flex xs12 sm6>
                    <v-hover v-slot:default="{ hover }">
                        <v-card flat id="card" class="pa-5 expand-transition" :elevation="hover ? 12 : 5">
                            <v-card-text class="subtitle-1 pt-2 pb-0">Type new password for {{ email }}:</v-card-text>
                            <v-card-text primary-title class="pt-3 pb-0 mb-2">
                                <v-form ref="form" lazy-validation>
                                    <v-text-field
                                            v-model="password"
                                            :append-icon="showPassword ? 'visibility_off' : 'visibility'"
                                            :rules="[rules.emptyPassword, rules.passwordLength, rules.samePassword]"
                                            :type="showPassword ? 'text' : 'password'"
                                            name="input-10-1"
                                            label="Password"
                                            hint="At least 8 characters"
                                            counter outline
                                            @click:append="showPassword = !showPassword"
                                            required
                                    ></v-text-field>
                                    <v-text-field
                                            :disabled="password.length < 8"
                                            v-model="confirmPassword"
                                            :append-icon="showConfirmPassword ? 'visibility_off' : 'visibility'"
                                            :rules="[rules.match]"
                                            :type="showConfirmPassword ? 'text' : 'password'"
                                            name="input-10-1"
                                            label="Confirm password"
                                            outline
                                            @click:append="showConfirmPassword = !showConfirmPassword"
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
        name: "ResetPassword",
        data() {
            return {
                loaded: false,
                showPassword: false,
                showConfirmPassword: false,
                errorMessage: null,
                email: null,
                password: '',
                confirmPassword: '',
                rules: {
                    passwordLength: v => v.length >= 8 || 'Min 8 characters',
                    emptyPassword: v => !!v || 'Please enter your password',
                    match: v => v === this.password || "Passwords don't match",
                    samePassword: () => {
                        if (this.errorMessage) return this.errorMessage;
                        else return false
                    },
                }
            }
        },
        watch: {
            password() {
                this.errorMessage = null
            }
        },
        created() {
            this.checkToken()
        },
        methods: {
            validate() {
                if (this.$refs.form.validate()) {
                    axios.post(process.env.VUE_APP_EMAIL_AUTH_URL + `/reset-password/${this.$route.params.token}`, {
                        password: this.password
                    })
                        .then(response => {
                            notifications.addNotification(response.data);
                            this.$router.replace('/')
                        })
                        .catch(error => {
                            if (error.response) {
                                if (error.response.status === 404) {
                                    notifications.addNotification(error.response.data.error);
                                    this.$router.replace('/')
                                } else {
                                    this.errorMessage = error.response.data.error;
                                    this.$refs.form.validate()
                                }
                            } else {
                                notifications.addNotification('An error occurred');
                            }
                        })
                }
            },
            checkToken() {
                axios.get(process.env.VUE_APP_EMAIL_AUTH_URL + `/check-reset-token/${this.$route.params.token}`).then(response => {
                    this.email = response.data.email;
                    this.loaded = true;
                }).catch(error => {
                    notifications.addNotification(error.response.data.error);
                    this.$router.replace('/')
                })
            }
        }
    }
</script>

<style scoped>
    .reset-password {
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