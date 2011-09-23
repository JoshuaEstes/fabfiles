from fabric.api import task,run

code_dir = '/home/sfproject/symfony'

@task(alias='cc')
def cache_clear():
  with cd(code_dir):
    run('./symfony cache:clear')

@task
def doctrine_migrate(version=0):
  with cd(code_dir):
    if version > 0:
      run('./symfony doctrine:migrate %s' % version)
    else:
      run('./symfony doctrine:migrate')

@task
def project_optimize():
  with cd(code_dir):
    run('./symfony project:optimize')

@task
def deploy():
  local('./symfony project:deploy --go production')
  doctrine_migrate()
  project_optimize()
  cache_clear()

