from fabric.api import sudo, run, env, prefix, task
from fabric.contrib.project import rsync_project

production_pi = '192.168.1.14'

env.user = 'pi'
env.hosts = [production_pi]
env.start_mqtt = False

@task
def production_api():
    env.remote_dir = '/home/pi/home-temp-restapi/source/'
    env.local_dir = '/home/andraz/Projects/home-temp-restapi/'

    env.supervisor = 'home-temp-restapi/source/conf/supervisor.home-temp-restapi.production.conf'
    env.supervisor_file = 'home-temp-restapi'

    env.nginx = 'home-temp-restapi/source/conf/nginx.home-temp-restapi.production.conf'
    env.nginx_file = 'nginx.home-temp-restapi.production.conf'

    env.virtual_env = '/home/pi/.virtualenvs/home-temp-restapi/bin/activate'
    env.requirements = '/home/pi/home-temp-restapi/source/requirements.txt'

@task
def production_mqtt_worker():
    env.remote_dir = '/home/pi/home-temp-mqtt-worker/source/'
    env.local_dir = '/home/andraz/Projects/home-temp-restapi/'

    env.supervisor = 'home-temp-mqtt-worker/source/conf/supervisor.mqtt-worker.production.conf'
    env.supervisor_name = 'mqtt-worker'

    env.nginx = 'home-temp-mqtt-worker/source/conf/nginx.home-temp-restapi.production.conf'
    env.nginx_file = 'nginx.home-temp-restapi.production.conf'

    env.virtual_env = '/home/pi/.virtualenvs/home-temp-mqtt-worker/bin/activate'
    env.requirements = '/home/pi/home-temp-mqtt-worker/source/requirements.txt'

    env.start_mqtt = True

@task
def deploy(requirements=False, supervisor=False, nginx=False):
    """
    Take local project, upload it to the server with the right configuration. Then check flags and install requirements,
    update supervisor configuration and update nginx configuration.
    """
    rsync_project(remote_dir=env.remote_dir, local_dir=env.local_dir)

    if requirements:
        with prefix('source {}'.format(env.virtual_env)):
            run('pip install -r {}'.format(env.requirements))

    if supervisor:
        sudo('cp /home/pi/{} /etc/supervisor/conf.d'.format(env.supervisor))
        sudo('supervisorctl reread')
        sudo('supervisorctl update')

    sudo('supervisorctl restart {}'.format(env.supervisor_name))

    if nginx:
        sudo('cp /home/pi/{} /etc/nginx/sites-available/'.format(env.nginx))
        try:
            sudo('rm /etc/nginx/sites-enabled/{}'.format(env.nginx_file))
        except:
            print("Nginx configuration is not linked... proceeding.")

        sudo('ln -s /etc/nginx/sites-available/{} /etc/nginx/sites-enabled/'.format(env.nginx_file))
        sudo('nginx -s reload')
        sudo('nginx -t')

    # Subscribe to temperature topics if deploying mqtt worker
    if env.start_mqtt:
        with prefix('source /home/pi/.virtualenvs/home-temp-mqtt-worker/bin/activate'):
            with prefix('cd /home/pi/home-temp-mqtt-worker/source/'):
                run('python /home/pi/home-temp-mqtt-worker/source/scripts/start_mqtt_listener.py')
