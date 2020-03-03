import axios from "axios";
import router from '@/modules/router'
import notifications from '@/modules/notifications'
import {checkAuth, logout, user} from './util'

function loginWithEmail(context) {
    return new Promise((resolve, reject) => {
        axios.post(process.env.VUE_APP_EMAIL_AUTH_URL + '/login', {
            email: context.email,
            password: context.password
        }).then(response => {
            if (response.status === 200) {
                localStorage.setItem('access_token', response.data.access_token);
                localStorage.setItem('auth_type', 'email');
                checkAuth().then(() => {
                    if (context.token) {
                        activateAccount(context.token).then(() => {
                            router.push('/home');
                            resolve()
                        }).catch(error => {
                            router.push('/home');
                            resolve()
                        })
                    } else {
                        router.push('/home');
                        resolve();
                    }
                }).catch(error => {
                    notifications.addNotification('An error occurred while logging in');
                    logout()
                });
            } else {
                notifications.addNotification('An error occurred while logging in');
                reject();
            }
        }).catch(function (error) {
            if (error.response) {
                reject(new Error(error.response.data.error));
            } else {
                notifications.addNotification('An error occurred while logging in');
                reject()
            }
        });
    })
}

function signUpWithEmail(context) {
    return new Promise((resolve, reject) => {
        axios.post(process.env.VUE_APP_EMAIL_AUTH_URL + '/sign-up', {
            email: context.email,
            password: context.password,
            first_name: context.firstName,
            last_name: context.lastName,
        }).then(response => {
            if (response.status === 200) {
                localStorage.setItem('access_token', response.data.access_token);
                localStorage.setItem('auth_type', 'email');
                checkAuth().then(() => {
                    notifications.addNotification(
                        `An email to activate your account has been sent to ${context.email}`
                    );
                    router.push('/home');
                    resolve()
                }).catch(error => {
                    notifications.addNotification('An error occurred while signing in');
                    logout();
                    reject()
                });
            } else {
                notifications.addNotification('An error occurred while signing in');
                reject();
            }
        }).catch(function (error) {
            if (error.response) {
                reject(new Error(error.response.data.error));
            } else {
                notifications.addNotification('An error occurred while signing in');
                reject()
            }
        });
    })
}

function activateAccount(token) {
    return new Promise((resolve, reject) => {
        axios.post(process.env.VUE_APP_EMAIL_AUTH_URL + `/confirm-email/${token}`).then(response => {
            if (response.status === 200) {
                notifications.addNotification(response.data);
                user.accountActivated = true;
                resolve()
            } else {
                reject()
            }
        }).catch(error => {
            notifications.addNotification(error.response.data.error);
            reject();
        })
    })
}

export {
    loginWithEmail,
    signUpWithEmail,
    activateAccount
}