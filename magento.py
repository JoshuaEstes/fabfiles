from fabric.api import *

@task
def reindexall():
  "Reindex Data by all indexers"
  with cd(env.deploy_to):
    run('php shell/indexer.php reindexall')

@task
def log_status():
  "Display statsper log tables"
  with cd(env.deploy_to):
    run('php shell/log.php status')

@task
def log_clean():
  "Clean the log files"
  with cd(env.deploy_to):
    run('php shell/log.php clean')


