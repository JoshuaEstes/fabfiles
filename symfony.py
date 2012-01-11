from fabric.api import *

@task(alias='cc')
def cache_clear():
  """
  Clear the symfony cache
  """
  with cd(env.deploy_to):
    run('./symfony cache:clear')

@task
def doctrine_migrate(version=0):
  """
  Migrate the database
  """
  with cd(env.deploy_to):
    if version > 0:
      run('./symfony doctrine:migrate %s' % version)
    else:
      run('./symfony doctrine:migrate')

@task
def project_optimize():
  """
  Optimizes the project
  """
  with cd(env.deploy_to):
    run('./symfony project:optimize frontend prod')

@task
def project_permissions():
  """
  Runs the permissions task
  """
  with cd(env.deploy_to):
    run('./symfony project:permissions')

@task
def deploy():
  """
  Runs project:deploy on your local machine
  Then migrates, optimizes the project, and clears the cache on the remote machines
  """
  local('./symfony project:deploy --go production')
  doctrine_migrate()
  project_permissions()
  plugin_publish_assets()
  project_optimize()
  cache_clear()

@task
def test_all():
  """
  Runs the test suite
  """
  with cd(env.deploy_to):
    run('./symfony test:all')

@task
def plugin_publish_assets():
  """
  Runs plugin:publish-assets
  """
  with cd(env.deploy_to):
    run('./symfony plugin:publish-assets')
