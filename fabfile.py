from __future__ import with_statement
from fabric.api import *
from fabric.contrib import files

from contextlib import contextmanager as _contextmanager

# For virtualenv and Fabric
env.hosts = ['ec2-23-20-147-141.compute-1.amazonaws.com']
env.user = 'ubuntu'
env.directory = '/home/ubuntu/shopplyEnv'
env.activate = 'source /home/ubuntu/shopplyEnv/bin/activate'

# For gunicorn process
env.remote_workdir = '/home/ubuntu/elasticAPI'
env.gunicorn_wsgi_app = 'webapp:app'

@_contextmanager
def virtualenv():
    with cd(env.directory):
        with prefix(env.activate):
            yield

def test():
    local("nosetests")

def commit():
    local("git add -p && git commit")

def push():
    local("git push")

def prepare_deploy():
    test()
    commit()
    push()

def stop_gunicorn():
    with settings(warn_only=True):
        if files.exists("%s/gunicorn.pid" % env.remote_workdir):
            run("kill -9 `cat %s/gunicorn.pid`" % env.remote_workdir)

def restart_gunicorn():
    stop_gunicorn()

    with virtualenv():
        run("cd %s && gunicorn -k egg:gunicorn#tornado webapp:app --pid=%s/gunicorn.pid" % (env.remote_workdir, env.remote_workdir))

def deploy_server():
    with settings(warn_only=True):
        if run("nosetests %s" % env.remote_workdir).failed:
            run("git clone git://github.com/burningion/elasticAPI.git %s" % env.remote_workdir)
    with cd(env.remote_workdir):
        run("git pull")
    with virtualenv():
        run("pip install -U -r %s/requirements.txt" % env.remote_workdir)
    restart_gunicorn()

    

