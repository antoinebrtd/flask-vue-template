import Vue from "vue";
import Router from "vue-router";

const Login = () => import("../../pages/auth/Login");
const ForgotPassword = () => import("../../pages/auth/ForgotPassword");
const ResetPassword = () => import("../../pages/auth/ResetPassword");
const GoogleCallback = () => import("../../pages/auth/callback/GoogleCallback");
const FacebookCallback = () => import("../../pages/auth/callback/FacebookCallback");
const Main = () => import("../../pages/Home");
const About = () => import("../../pages/About");
const Account = () => import("../../pages/Account");

Vue.use(Router);

export default new Router({
  routes: [

    {
      path: '*',
      redirect: '/login'
    },
    {
      path: "/login",
      name: "login",
      meta: {
        hideHeader: true,
        transparentFooter: true
      },
      component: Login
    },
    {
      path: "/auth/email/forgot-password",
      name: "forgot-password",
      meta: {
        hideHeader: true,
        transparentFooter: true
      },
      component: ForgotPassword
    },
    {
      path: "/auth/email/reset-password/:token",
      name: "reset-password",
      meta: {
        hideHeader: true,
        transparentFooter: true
      },
      component: ResetPassword
    },
    {
      path: "/login/:token",
      name: "activate-account",
      meta: {
        hideHeader: true,
        transparentFooter: true
      },
      component: Login
    },
    {
      path: "/auth/google/callback",
      name: "google-callback",
      meta: {
        hideHeader: true,
        transparentFooter: true
      },
      component: GoogleCallback
    },
    {
      path: "/auth/facebook/callback",
      name: "facebook-callback",
      meta: {
        hideHeader: true,
        transparentFooter: true
      },
      component: FacebookCallback
    },
    {
      path: "/home",
      name: "home",
      meta: {},
      component: Main
    },
    {
      path: "/about",
      name: "about",
      meta: {},
      component: About
    },
    {
      path: "/accounts/:id",
      name: "account",
      meta: {
        transparentFooter: true
      },
      component: Account
    }
  ]
});