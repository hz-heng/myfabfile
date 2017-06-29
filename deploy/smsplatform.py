# -*- coding:utf-8 -*-
from fabric.api import env, settings, cd, run

env.hosts = ['']
env.user = ''
env.password = ''


def _git_clone():
    with settings(warn_only=True):
        if run('type git').failed:
            run('yum -y install git')
        with cd('/opt'):
            run('git clone https://github.com/hz-heng/smsplatform.git')

def _build_virtualenv():
    env_dir = '/var/python_env'
    with settings(warn_only=True): 
        if run('test -d %s' % env_dir).failed:
            run('mkdir %s' % env_dir)
        with cd(env_dir):
            run('virtualenv -p /var/python3/bin/python3 --no-site-packages sms_env')

def _install_requirements():
    run('source /var/python_env/sms_env/bin/activate')
    run('pip install -r /opt/smsplatform/requirements.txt')
    run('deactivate')
    
def _db_init():
    run('source /var/python_env/sms_env/bin/activate')
    with cd('/opt/smsplatform'):
        run('python manage.py db init')
        run('python manage.py db migrate')
        run('python manage.py db upgrade')
        run('python manage.py initdata')
    run('source /var/python3/sms_env/bin/activate')

def init():
    _git_clone()
    _build_virtualenv()
    _install_requirements()
    _db_init()
