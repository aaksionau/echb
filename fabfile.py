from fabric.api import abort, cd, env, local, run, settings, task, prefix
from fabric.contrib.console import confirm
from fabric.operations import prompt
import os
from termcolor import colored

env.use_ssh_config = True
env.hosts = ["webfaction"]
env.remote_app_dir = '/home/paloni/webapps/echb/echb/'
env.remote_app_static_dir = '/home/paloni/webapps/echb_static/'
env.remote_apache_dir = '/home/paloni/webapps/echb/apache2/'

manage_py = f'cd {env.remote_app_dir}echb/; python manage.py'

command = "python manage.py {} --settings=echb.settings.local"

VIRTUAL_ENV_BIN_DIR = "/home/paloni/.local/share/virtualenvs/echb-dkHc5E87/bin/"
UPDATE_PYTHON_PATH = r'PATH="{}:$PATH"'.format(VIRTUAL_ENV_BIN_DIR)


@task
def runserver():
    local(command.format('runserver'))


@task
def makemigrations():
    local(command.format('makemigrations'))


@task
def migrate():
    local(command.format('migrate'))

# to use in command console: fab ben:css_class
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
def testing():
    test()


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


def _get_latest_source():
    run(f'cd {env.remote_app_dir}; git pull origin master')


def with_venv(func, *args, **kwargs):
    "Use Virtual Environment for the command"

    def wrapped(*args, **kwargs):
        with prefix(UPDATE_PYTHON_PATH):
            return func(*args, **kwargs)

    wrapped.__name__ = func.__name__
    wrapped.__doc__ = func.__doc__
    return wrapped


@with_venv
def _update_virtualenv():
    run(f'cd {env.remote_app_dir}; pipenv install')


@with_venv
def _update_static_files():
    run(f'{manage_py} collectstatic --settings=echb.settings.production --noinput')


@with_venv
def _update_database():
    run(f'{manage_py} migrate --settings=echb.settings.production')


def _restart_server():
    run(f'cd {env.remote_app_dir}/echb/echb/; touch wsgi.py;')


def deploy_to_server():
    _get_latest_source()
    _update_virtualenv()
    _update_static_files()
    _update_database()
    _restart_server()
