import axios from "axios";
import router from '@/modules/router'
import notifications from '@/modules/notifications'
import {checkAuth, logout} from './util'

function loginWithGoogle() {
    axios.get(process.env.VUE_APP_GOOGLE_AUTH_URL + '/login').then(response => {
        if (response.status === 200) {
            window.location.replace(response.data.url);
        } else {
            raiseError()
        }
    }).catch(error => {
        raiseError()
    });
}

function authorizeGoogle(code, state) {
    axios.get(process.env.VUE_APP_GOOGLE_AUTH_URL + '/authorize?code=' + code + '&state=' + state)
        .then(response => {
            if (response.status === 200) {
                localStorage.setItem('access_token', response.data.access_token);
                localStorage.setItem('auth_type', 'google');
                checkAuth().then(() => {
                    router.push('/home');
                }).catch(error => {
                    logout();
                    raiseError()
                });
            } else {
                raiseError()
            }
        })
        .catch(error => {
            if (error.response) {
                notifications.addNotification(error.response.data.error)
                router.replace('/')
            } else {
                raiseError()
            }
        });
}

function raiseError() {
    notifications.addNotification('An error occurred while logging in with Google');
    if (router.name !== '/') {
        router.replace('/')
    }
}

export {
    loginWithGoogle,
    authorizeGoogle
}