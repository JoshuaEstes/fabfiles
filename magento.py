from fabric.api import *

@task
def reindexall():
  with cd(env.deploy_to):
    run('php shell/indexer.php reindexall')

@task
def log_status():
  with cd(env.deploy_to):
    run('php shell/log.php status')

@task log_clean():
  with cd(env.deploy_to):
    run('php shell/log.php clean')


