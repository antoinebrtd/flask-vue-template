from {{cookiecutter.project_name}}.core import logger
from {{cookiecutter.project_name}} import create_app

app = create_app()

if __name__ == '__main__':
    logger.info('Starting Template API ...')
    app.run(host='0.0.0.0', port=5000, threaded=True{%- if cookiecutter.enable_https == 'y' %}, ssl_context=('certs/localhost.pem', 'certs/localhost-key.pem'){%- endif %})
    logger.info('End of Template')
