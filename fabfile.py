from __future__ import with_statement
from fabric.api import *
from contextlib import contextmanager as _contextmanager

env.hosts = ['ec2-23-20-147-141.compute-1.amazonaws.com']
env.user = 'ubuntu'
env.directory = '/home/ubuntu/shopplyEnv'
env.activate = 'source /home/ubuntu/shopplyEnv/bin/activate'

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

def deploy_server():
    code_dir = '/home/ubuntu/elasticAPI'
    with settings(warn_only=True):
        if run("nosetests %s" % code_dir).failed:
            run("git clone git://github.com/burningion/elasticAPI.git %s" % code_dir)
    with cd(code_dir):
        run("git pull")
    with virtualenv():
        run("pip install -U -r %s/requirements.txt" % code_dir)
            
        
            
    
    

