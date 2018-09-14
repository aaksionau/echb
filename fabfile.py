from fabric.api import task, env, run, cd, local, settings, abort
from fabric.operations import prompt, put
from fabric.context_managers import prefix
from fabric.contrib.console import confirm


env.use_ssh_config = True
env.hosts = ["webfaction"]
env.remote_app_dir = '/home/paloni/webapps/echb_project/echb/'
env.remote_app_static_dir = '/home/paloni/webapps/echb_static/'
env.remote_apache_dir = '/home/paloni/webapps/echb_project/apache2/'

@task
def deploy():
    test_results = test()
    commit()
    push()
    if test_results:
        deploy_to_server()

def test():
    with settings(warn_only=True):
        result = local("python manage.py test --settings=echb.settings.test")
        if result.failed and not confirm("Tests failed. Continue?"):
            abort("Aborted at user request.")
            return False
        else:
            return True
    
def push():
    local("git push origin master")

def commit():
    message = prompt("Enter a git commit message: ")
    local('git add . && git commit -am "{}"'.format(message))


def deploy_to_server():
    with cd(f'{env.remote_app_dir}'):
        run('git pull origin master')
        run('python manage.py collectstatic')

    run(f'cd {env.remote_app_dir}/echb/echb/; touch wsgi.py;')