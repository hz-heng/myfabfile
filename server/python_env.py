# -*- coding:utf-8 -*-
from fabric.api import env, settings, cd, run

#服务器ssh登录信息
env.hosts = []
env.user = ""
env.password = ""

#安装Python3.5
def _install_python():
    print('install Python3.5')
    run('yum -y groupinstall "Development Tools"')
    run('yum -y install openssl-devel bzip2-devel zlib-devel ncurese-devel sqlite-devel readline-devel')
    with settings(warn_only=True):
        if run('type wget').failed:
            run('yum -y install wget')
        run('wget -O /tmp/Python.tgz https://www.python.org/ftp/python/3.5.1/Python-3.5.1.tgz')
    run('tar -zxvf /tmp/Python.tgz -C /tmp/')
    with cd('/tmp/Python'):
        run('./configure --prefix=/var/python3')
        run('make && make install')
    run('rm -f /tmp/Python.tgz')
    run('rm -rf /tmp/Python')

#安装virtualenv
def _install_virtualenv():
    print('install virtualenv')
    with settings(warn_only=True):
        if run('type pip').failed:
            run('yum -y install python-setuptools')
            run('easy_install pip')
        run('pip install virtualenv')

#主任务
def task():
    _install_python()
    _install_virtualenv()
