from fabric.api import task,run,cd

@task(alias='cc')
def cache_clear():
  with cd(env.deploy_to):
    run('./symfony cache:clear')

@task
def doctrine_migrate(version=0):
  with cd(env.deploy_to):
    if version > 0:
      run('./symfony doctrine:migrate %s' % version)
    else:
      run('./symfony doctrine:migrate')

@task
def project_optimize():
  with cd(env.deploy_to):
    run('./symfony project:optimize')

@task
def deploy():
  local('./symfony project:deploy --go production')
  doctrine_migrate()
  project_optimize()
  cache_clear()

