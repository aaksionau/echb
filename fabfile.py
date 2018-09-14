from fabric.api import task, env, run, cd, local, settings, abort
from fabric.operations import prompt, put
from fabric.context_managers import prefix
from fabric.contrib.console import confirm

@task
def prepare():
    test()
    commit()
    push()

def test():
    with settings(warn_only=True):
        result = local("python manage.py test --settings=echb.settings.test")
    if result.failed and not confirm("Tests failed. Continue?"):
        abort("Aborted at user request.")

def push():
    local("git push origin master")


def commit():
    message = prompt("Enter a git commit message: ")
    local('git add . && git commit -am "{}"'.format(message))

env.use_ssh_config = True
env.hosts = ["webfaction", "github"]
env.remote_app_dir = '/home/paloni/webapps/echb_project/echb/'
env.remote_app_static_dir = '/home/paloni/webapps/echb_static/'
env.remote_apache_dir = '/home/paloni/webapps/echb_project/apache2/'

@task
def restart_server():
    run(f'{env.remote_apache_dir}/bin/restart')


@task
def deploy():
    with cd(f'{env.remote_app_dir}'):
        run('git pull origin master')

    put('static/css/styles.min.css', f'{env.remote_app_static_dir}/css/')
    put('static/js/', env.remote_app_static_dir)

    run(f'cd {env.remote_app_dir}/echb/echb/; touch wsgi.py;')