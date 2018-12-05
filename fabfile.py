from fabric.api import abort, cd, env, local, run, settings, task
from fabric.contrib.console import confirm
from fabric.operations import prompt
import os
from termcolor import colored

env.use_ssh_config = True
env.hosts = ["webfaction"]
env.remote_app_dir = '/home/paloni/webapps/echb_project/echb/'
env.remote_app_static_dir = '/home/paloni/webapps/echb_static/'
env.remote_apache_dir = '/home/paloni/webapps/echb_project/apache2/'

command = "python manage.py {} --settings=echb.settings.local"


@task
def runserver():
    local(command.format('runserver'))


@task
def makemigrations():
    local(command.format('makemigrations'))


@task
def migrate():
    local(command.format('migrate'))


@task
def bem(css_class):
    base_path = os.path.dirname(os.path.realpath(__file__))
    css_blocks_path = os.path.join(base_path, 'echb', 'static', 'css', 'blocks')
    css_new_class_path = os.path.join(css_blocks_path, css_class)
    sass_file_path = os.path.join(css_new_class_path, f'{css_class}.sass')
    local(f'md {css_new_class_path}')

    local(f'echo .{css_class} > {sass_file_path}')
    print(colored(f'Folder and sass file were successfuly created here: {sass_file_path}', 'green'))


@task
def deploy():
    """Runing tests
    Deploy to the server
    """

    test_results = test()
    if test_results:
        deploy_to_server()


@task
def cmt():
    """Commits and push changes to the git server after running tests
    """

    test_results = test()
    if test_results:
        commit()
        push()


def test():
    with settings(warn_only=True):
        result = local("python manage.py test --settings=echb.settings.test")
        if result.failed and not confirm("Tests failed. Continue?"):
            abort("Aborted at user request.")
            return False
        else:
            return True


def push():
    local("git push origin HEAD")


def commit():
    message = prompt("Enter a git commit message: ")
    local('git add . && git commit -am "{}"'.format(message))


def deploy_to_server():
    with cd(f'{env.remote_app_dir}'):
        run('git pull origin master')

    manage_py = f'cd {env.remote_app_dir}/echb/; python3.6 manage.py'

    run(f'{manage_py} migrate --settings=echb.settings.production')
    run(f'{manage_py} collectstatic --settings=echb.settings.production --noinput')

    run(f'cd {env.remote_app_dir}/echb/echb/; touch wsgi.py;')
