import os
import shutil

import yaml

MANIFEST = 'manifest.yml'


def delete_resources_for_disabled_features():
    print(os.getcwd())
    with open(MANIFEST) as manifest_file:
        manifest = yaml.load(manifest_file)
        for feature in manifest['features']:
            if feature['enabled'] != 'y':
                print('removing resources for disabled feature {}...'.format(feature['name']))
                for resource in feature['resources']:
                    delete_resource(resource)
    print('cleanup complete, removing manifest...')
    delete_resource(MANIFEST)

    {%- if cookiecutter.facebook_login == 'n' and cookiecutter.google_login == 'n' %}
    delete_resource('../{{cookiecutter.project_name}}/front/src/pages/auth/callback/')
    {%- endif %}
    delete_resource('../.git/')


def delete_resource(resource):
    if os.path.isfile(resource):
        print('removing file: {}'.format(resource))
        os.remove(resource)
    elif os.path.isdir(resource):
        print('removing directory: {}'.format(resource))
        shutil.rmtree(resource)


if __name__ == '__main__':
    delete_resources_for_disabled_features()
