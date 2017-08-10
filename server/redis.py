# -*- coding:utf-8 -*-
from fabric.api import env, settings, cd, run

#服务器ssh登录信息
env.hosts = []
env.user = ""
env.password = ""

#安装redis
def _install_redis():
    print('install Redis')
    run('yum -y install cpp binutils glibc-kernheaders glibc-common glibc-devel gcc make')
    with settings(warn_only=True):
        if run('type wget').failed:
            run('yum -y install wget')
        run('wget -O /tmp/redis.tar.gz http://download.redis.io/releases/redis-4.0.1.tar.gz')
    run('mkdir /tmp/redis && tar -zxvf /tmp/redis.tar.gz -C /tmp/redis --strip-components 1')
    with cd('/tmp/redis'):
        run('make')
    with cd('/tmp/redis/src'):
        run('make install')
    run('rm -f /tmp/redis.tar.gz')

#设置redis为系统服务
def _set_redis_service():
    print('set Redis')
    run('cp /tmp/redis/utils/redis_init_script /etc/rc.d/init.d/redis')
    run('mkdir /etc/redis')
    run('cp /tmp/redis/redis.conf /etc/redis/6379.conf')
    run('sed -i "2a\# chkconfig: 2345 80 90" /etc/rc.d/init.d/redis')
    run('sed -i "/^daemonize/c\daemonize yes" /etc/redis/6379.conf')
    run('sed -i "/^logfile/c\logfile /var/log/redis_6379.log" /etc/redis/6379.conf')
    #run('chkconfig --add redis')
    #run('chkconfig redis on')
    #run('systemctl start redis')
    

#主任务
def task():
    _install_redis()
    _set_redis_service()
