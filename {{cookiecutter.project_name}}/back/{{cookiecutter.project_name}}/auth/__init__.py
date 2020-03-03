{%- if cookiecutter.email_login == 'y' %}
from .email_login import *
{%- endif %}
{%- if cookiecutter.facebook_login == 'y' %}
from .facebook_login import *
{%- endif %}
{%- if cookiecutter.google_login == 'y' %}
from .google_login import *
{%- endif %}
from .utils import authenticated
