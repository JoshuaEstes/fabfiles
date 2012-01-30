"""
Symfony 1.4 fabfile

1) Make sure you run the task setup for your first deploy. After that you will
   not need to run setup again.

"""
from fabric.api import *
from fabric.contrib.project import rsync_project
from os import getcwd

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
def setup():
  """
  This needs to be ran first before you start using deploy, once you have ran this
  once, then you can use deploy as much as you want.
  """
  rsync_symfony()
  setup_databases_yml()
  doctrine_build_db()
  doctrine_migrate()
  plugin_publish_assets()

def setup_databases_yml():
  """
  This will setup the databases.yml file
  """
  dbhost = prompt('Database Hostname: ',default="127.0.0.1")
  dbname = prompt('Database Name: ',default='symfony')
  username = prompt('Database Username: ', default='root')
  password = prompt('Database Passowrd: ', default='root')
  with cd(env.deploy_to):
    run('./symfony configure:database "mysql:host=%s;dbname=%s" "%s" "%s"' % (dbhost, dbname, username, password))

@task
def deploy():
  """
  Runs project:deploy on your local machine
  Then migrates, optimizes the project, and clears the cache on the remote machines
  """
  project_disable()
  rsync_symfony()
  cache_clear()
#  doctrine_migrate()
  project_permissions()
  plugin_publish_assets()
  project_optimize()
  project_enable()

def rsync_symfony():
  """
  This will rsync the project
  """
  rsync_project(env.deploy_to,getcwd() + '/',[],True,"-pthrvzLaC --exclude-from='" + getcwd() + "/config/rsync_exclude.txt'")

@task
def doctrine_build(options):
  """
  This will run the task doctrine:build with the options that you have given
  """
  with cd(env.deploy_to):
    run('./symfony doctrine:build %s' % options)

def doctrine_build_db():
  """
  Build the database
  """
  with cd(env.deploy_to):
    run('./symfony doctrine:build-db')

def doctrine_drop_db():
  """
  Drop the database
  """
  with cd(env.deploy_to):
    run('./symfony doctrine:drop-db')

@task
def doctrine_migrate(version=0):
  """
  Migrate the database

  Usage:

    fab doctrine_migrate

    fab doctrine_migrate:12

  The first example will migrate to the current version. The second example
  shows how you can migrate to a specific version.
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
    for app in env.apps:
      run("./symfony project:optimize %s prod" % app)

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
