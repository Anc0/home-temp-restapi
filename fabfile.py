from fabric.api import sudo, run, env, prefix, task
from fabric.contrib.project import rsync_project

production_pi = '192.168.1.14'

env.user = 'pi'
env.hosts = [production_pi]

@task
def production_api():
    env.remote_dir = '/home/pi/home-temp-restapi/source/'
    env.local_dir = '/home/andraz/Projects/home_temp_restapi/'
    env.supervisor = 'home-temp-restapi.production.conf'
    env.nginx = 'home-temp-restapi.production.conf'

@task
def production_mqtt_worker():
    env.remote_dir = '/home/pi/home-temp-restapi/source/'
    env.local_dir = '/home/andraz/Projects/home_temp_restapi/'
    env.supervisor = 'mqqt-worker.production.conf'
    env.nginx = 'home-temp-restapi.production.conf'

@task
def deploy(requirements=False, supervisor=False, nginx=False):
    """
    Take local project, upload it to the server with the right configuration. Then check flags and install requirements,
    update supervisor configuration and update nginx configuration.
    """
    rsync_project(remote_dir=env.remote_dir, local_dir=env.local_dir)

    if requirements:
        with prefix('source ~/.virtualenvs/home-temp-restapi/bin/activate'):
            run('pip install -r ~/home-temp-restapi/source/requirements.txt')

    if supervisor:
        sudo('cp /home/pi/home-temp-restapi/source/conf/supervisor.{} /etc/supervisor/conf.d'.format(env.supervisor))
        sudo('supervisorctl reread')
        sudo('supervisorctl update')

    if nginx:
        sudo('cp /home/pi/home-temp-restapi/source/conf/nginx.{} /etc/nginx/'.format(env.nginx))
        sudo('nginx -s reload')
