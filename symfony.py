"""
"""
from fabric.api import *

# Define as many applications as you want here
env.apps = ['frontend']

@task(alias='cc')
def cache_clear():
  """
  Clear the symfony cache
  """
  with cd(env.deploy_to):
    run('./symfony cache:clear')

@task
def deploy():
  """
  Runs project:deploy on your local machine
  Then migrates, optimizes the project, and clears the cache on the remote machines
  """
  project_disable()
  local("./symfony project:deploy production --go --rsync-options=\"-azvC --force --delete --progress\"")
  cache_clear()
#  doctrine_migrate()
  project_permissions()
  plugin_publish_assets()
  project_optimize()
  project_enable()

@task
def doctrine_migrate(version=0):
  """
  Migrate the database
  """
  with cd(env.deploy_to):
    if version > 0 and version.isdigit():
      run('./symfony doctrine:migrate %s' % version)
    else:
      run('./symfony doctrine:migrate')

@task
def plugin_publish_assets():
  """
  Runs plugin:publish-assets
  """
  with cd(env.deploy_to):
    run('./symfony plugin:publish-assets')

@task
def project_clear_controllers():
  with cd(env.deploy_to):
    run("./symfony project:clear-controllers")

@task
def project_disable():
  """
  Disables the project
  """
  with cd(env.deploy_to):
    for app in env.apps:
      run("./symfony project:disable prod %s" % app)

@task
def project_enable():
  """
  Enable the project
  """
  with cd(env.deploy_to):
    for app in env.apps:
      run("./symfony project:enable prod %s" % app)

@task
def project_optimize():
  """
  Optimizes the project
  """
  with cd(env.deploy_to):
    for app in env.applications:
      run("./symfony project:optimize prod %s" % app)

@task
def project_permissions():
  """
  Runs the permissions task
  """
  with cd(env.deploy_to):
    run('./symfony project:permissions')

@task
def test_all():
  """
  Runs the test suite
  """
  with cd(env.deploy_to):
    run('./symfony test:all')
