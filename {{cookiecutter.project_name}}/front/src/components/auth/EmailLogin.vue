<template>
    {% raw %}
    <v-layout column align-center>
        <v-card class="expand-transition" style="background-color: transparent" elevation="0"
                :height="signUp ? 380 : 230">
            <v-layout row wrap justify-center fill-height align-center>
                <v-flex xs12>
                    <v-form ref="form" lazy-validation>
                        <v-layout row wrap>
                            <v-fade-transition hide-on-leave>
                                <v-flex xs12 v-if="signUp">
                                    <v-card-text class="py-0 mt-3">
                                        <v-text-field
                                                class="my-0 py-0"
                                                :rules="[rules.emptyFirstName]"
                                                outline
                                                label="First name"
                                                append-icon="person"
                                                v-model="firstName"
                                                required
                                        ></v-text-field>
                                    </v-card-text>
                                </v-flex> { enter: number, leave: number },
                            </v-fade-transition>
                            <v-fade-transition hide-on-leave>
                                <v-flex xs12 v-if="signUp">
                                    <v-card-text class="py-0 mt-3">
                                        <v-text-field
                                                class="my-0 py-0"
                                                :rules="[rules.emptyLastName]"
                                                outline
                                                label="Last name"
                                                append-icon="person"
                                                v-model="lastName"
                                                required
                                        ></v-text-field>
                                    </v-card-text>
                                </v-flex>
                            </v-fade-transition>
                            <v-flex xs12>
                                <v-card-text class="py-0 mt-3">
                                    <v-text-field
                                            class="mb-0 pb-0"
                                            :rules="[rules.emptyEmail, rules.emailNotValid, rules.emailIssue]"
                                            outline
                                            label="Email"
                                            append-icon="mail"
                                            v-model="email"
                                            required
                                    ></v-text-field>
                                </v-card-text>
                            </v-flex>
                            <v-flex xs12>
                                <v-card-text class="py-0 mt-2">
                                    <v-text-field
                                            v-if="!signUp"
                                            v-model="password"
                                            :rules="[rules.emptyPassword, rules.wrongPassword]"
                                            :append-icon="showPassword ? 'visibility_off' : 'visibility'"
                                            :type="showPassword ? 'text' : 'password'"
                                            name="input-10-1"
                                            label="Password"
                                            outline
                                            @click:append="showPassword = !showPassword"
                                            required
                                    ></v-text-field>
                                    <v-text-field
                                            v-else
                                            class="my-0 py-0"
                                            v-model="password"
                                            :append-icon="showPassword ? 'visibility_off' : 'visibility'"
                                            :rules="[rules.emptyPassword, rules.passwordLength]"
                                            :type="showPassword ? 'text' : 'password'"
                                            name="input-10-1"
                                            label="Password"
                                            hint="At least 8 characters"
                                            counter outline
                                            @click:append="showPassword = !showPassword"
                                            required
                                    ></v-text-field>
                                </v-card-text>
                            </v-flex>
                            <v-layout justify-end row>
                                <v-slide-y-transition hide-on-leave>
                                    <v-btn text class="button mr-5" color="error" x-small v-if="forgotPassword"
                                           to="/auth/email/forgot-password">
                                        Forgot password?
                                    </v-btn>
                                </v-slide-y-transition>
                            </v-layout>
                            <v-fade-transition hide-on-leave>
                                <v-flex xs12 v-if="signUp">
                                    <v-card-text class="py-0">
                                        <v-text-field
                                                class="my-0 py-0"
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
                                    </v-card-text>
                                </v-flex>
                            </v-fade-transition>
                        </v-layout>
                    </v-form>
                </v-flex>
                <v-flex xs11>
                    <v-btn v-if="!signUp" color="primary" block class="login-btn mt-5" @click="validate()">Log in
                    </v-btn>
                    <v-btn v-else color="primary" block class="login-btn mt-5" @click="validate()">Sign up</v-btn>
                </v-flex>
            </v-layout>
        </v-card>
        <v-btn v-if="!signUp" text class="button mt-2" color="primary" @click="changeView">
            Don't have an account ? Sign up!
        </v-btn>
        <v-btn v-else text class="button mt-2" color="primary" @click="changeView">
            Already have an account ? Log in.
        </v-btn>
    </v-layout>
    {% endraw %}
</template>

<script>
    import axios from 'axios';
    import auth from '@/modules/auth';
    import notifications from '@/modules/notifications';

    export default {
        name: "EmailLogin",
        props: {
            token: String
        },
        data() {
            return {
                signUp: false,
                errorType: null,
                errorMessage: null,
                showPassword: false,
                showConfirmPassword: false,
                forgotPassword: false,
                firstName: '',
                lastName: '',
                email: null,
                password: '',
                confirmPassword: '',
                rules: {
                    emptyEmail: v => !!v || 'Please enter your email',
                    emailNotValid: v => /.+@.+/.test(v) || 'This email is not valid',
                    emptyPassword: v => !!v || 'Please enter your password',
                    emptyFirstName: v => !!v || 'Please enter your first name',
                    emptyLastName: v => !!v || 'Please enter your last name',
                    passwordLength: v => v.length >= 8 || 'Min 8 characters',
                    match: v => v === this.password || "Passwords don't match",
                    wrongPassword: () => {
                        if (this.errorType === 'password') return this.errorMessage;
                        else return false
                    },
                    emailIssue: () => {
                        if (this.errorType === 'email') return this.errorMessage;
                        else return false
                    }
                }
            }
        },
        watch: {
            email() {
                this.$refs.form.resetValidation();
                this.errorType = null;
                this.errorMessage = null;
            },
            password() {
                if (this.errorType === 'password') {
                    this.errorType = null;
                    this.errorMessage = null
                }
            }
        },
        created() {
            if (this.token) {
                this.checkToken()
            }
        },
        methods: {
            validate() {
                if (this.$refs.form.validate()) {
                    if (this.signUp) {
                        auth.signUpWithEmail(this).then(() => {
                        }).catch(error => {
                            this.errorMessage = error.message;
                            this.errorType = 'email';
                            this.$refs.form.validate()
                        })
                    } else {
                        auth.loginWithEmail(this).then(() => {
                        }).catch(error => {
                            this.errorMessage = error.message;
                            if (this.errorMessage === 'Wrong password') {
                                this.forgotPassword = true;
                                this.errorType = 'password'
                            } else {
                                this.errorType = 'email'
                            }
                            this.$refs.form.validate()
                        })
                    }
                }
            },
            checkToken() {
                axios.get(process.env.VUE_APP_EMAIL_AUTH_URL + `/check-activation-token/${this.token}`).then(response => {
                    this.email = response.data.email;
                    notifications.addNotification('Please login to confirm your email address')
                }).catch(error => {
                    notifications.addNotification(error.response.data.error);
                    this.$router.replace('/')
                })
            },
            changeView() {
                this.password = '';
                this.confirmPassword = '';
                this.errorMessage = null;
                this.errorType = null;
                this.showPassword = false;
                this.showConfirmPassword = false;
                this.forgotPassword = false;
                this.signUp = !this.signUp;
                this.$refs.form.resetValidation();
            }
        }
    }
</script>

<style scoped>
    .login-btn {
        border-radius: 4px;
        text-transform: none !important;
    }

    .button {
        text-transform: None !important;
        text-decoration: underline;
    }

    .expand-transition {
        -webkit-transition: height 0.2s;
        transition: height 0.2s;
    }
</style>