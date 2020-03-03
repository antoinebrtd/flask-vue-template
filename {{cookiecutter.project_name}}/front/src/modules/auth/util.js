import axios from "axios";
import router from '@/modules/router'

let user = {
    authenticated: false,
    profile: undefined,
    accountActivated: false,
    firstLogin: false
};


function checkAuth() {
    return new Promise((resolve, reject) => {
        const jwt = localStorage.getItem('access_token');
        if (jwt !== null) {
            axios.defaults.headers.common['Authorization'] = 'Bearer ' + jwt;
            getUserInfo().then(() => {
                user.authenticated = true;
                resolve()
            }).catch(error => {
                reject()
            })
        } else {
            user.authenticated = false;
            reject();
        }
    });
}

function getUserInfo() {
    return new Promise((resolve, reject) => {
        axios.get(process.env.VUE_APP_API_URL + '/me').then(response => {
            if (response.status === 200) {
                user.profile = response.data.profile;
                user.accountActivated = response.data.account_activated;
                user.firstLogin = response.data.first_login;
                localStorage.setItem('profile', JSON.stringify(user.profile));
                resolve();
            } else {
                reject();
            }
        }).catch(function (error) {
            reject();
        });
    })
}

function logout() {
    if (router.currentRoute.name !== 'login') {
        router.replace('/');
    }
    localStorage.removeItem('access_token');
    localStorage.removeItem('profile');
    localStorage.removeItem('auth_type');
    axios.defaults.headers.common['Authorization'] = '';
    user.authenticated = false;
    user.profile = null;
    user.accountActivated = false;
}

export {
    user,
    checkAuth,
    logout,
    getUserInfo
}