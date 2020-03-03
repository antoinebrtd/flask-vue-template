import {user, checkAuth, getUserInfo, logout} from './util'
{%- if cookiecutter.facebook_login == 'y' %}
import {authorizeFacebook, loginWithFacebook} from './facebook'
{%- endif %}
{%- if cookiecutter.google_login == 'y' %}
import {authorizeGoogle, loginWithGoogle} from './google'
{%- endif %}
{%- if cookiecutter.email_login == 'y' %}
import {loginWithEmail, signUpWithEmail, activateAccount} from './email'
{%- endif %}

export default {
  user,
  {%- if cookiecutter.email_login == 'y' %}
  loginWithEmail,
  signUpWithEmail,
  activateAccount,
  {%- endif %}
  {%- if cookiecutter.google_login == 'y' %}
  loginWithGoogle,
  authorizeGoogle,
  {%- endif %}
  {%- if cookiecutter.facebook_login == 'y' %}
  loginWithFacebook,
  authorizeFacebook,
  {%- endif %}
  checkAuth,
  logout,
  getUserInfo
}