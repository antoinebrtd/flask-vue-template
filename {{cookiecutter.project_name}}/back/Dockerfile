FROM python:3.6

RUN mkdir -p /app/config
WORKDIR /app

ADD requirements.txt .
RUN pip install -r requirements.txt

ADD config/tree.json /app/config/tree.json
ADD config/config.prod.json /app/config/config.json
{%- if cookiecutter.google_login == 'y' %}
ADD config/google.json /app/config/google.json
{%- endif %}
{%- if cookiecutter.facebook_login == 'y' %}
ADD config/facebook.json /app/config/facebook.json
{%- endif %}
ENV TREE_FILE /app/config/tree.json
ENV CONFIG_FILE /app/config/config.json
{%- if cookiecutter.google_login == 'y' %}
ENV GOOGLE_CONFIG_FILE /app/config/google.json
{%- endif %}
{%- if cookiecutter.facebook_login == 'y' %}
ENV FACEBOOK_CONFIG_FILE /app/config/facebook.json
{%- endif %}

ADD run.py /app/
ADD worker.py /app/

ADD {{cookiecutter.project_name}} /app/template

CMD ["gunicorn","-w","1","--bind","0.0.0.0:8000","run:app"]
