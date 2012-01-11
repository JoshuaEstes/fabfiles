"""
Magento.py

This file will take care of setting your magento project up and deploying it to
your beta and production servers. Please see the README file for information on
how to use this file.

To view how to use any of these tasks, run fab -d COMMAND
"""
from fabric.api import *
from fabric.contrib.project import rsync_project
from os import getcwd

@task
def deploy():
    "deploy the code to servers yeah!"
    rsync_project(env.deploy_to,getcwd() + '/',["media","var",".git",".gitignore","app/etc/local.xml","*.py*","sitemap"],True,"-pthrvzL")

@task
def indexer(status=False,mode=False,mode_realtime=False,mode_manual=False,reindex=False):
    """
    Run index.php with your options

    Options:
          status='<indexer>'            Show Indexer(s) Status
          mode='<indexer>'              Show Indexer(s) Index Mode
          mode_realtime='<indexer>'     Set index mode type "Update on Save"
          mode_manual='<indexer>'       Set index mode type "Manual Update"
          reindex='<indexer>'           Reindex Data

    Usage:

        fab production status:status='catalog_url'
    """
    with cd(env.deploy_to):
        if status:
            run('php shell/indexer.php --status %s' % status)
        if mode:
            run('php shell/indexer.php --mode %s' % mode)
        if mode_realtime:
            run('php shell/indexer.php --mode-realtime %s' % mode_realtime)
        if mode_manual:
            run('php shell/indexer.php --mode-manual %s' % mode_manual)
        if reindex:
            run('php shell/indexer.php --reindex %s' % reindex)

@task
def indexer_info():
    """
    Show allowed indexers
    """

@task
def indexer_reindexall():
  """
  Reindex Data by all indexers
  """
  with cd(env.deploy_to):
    run('php shell/indexer.php reindexall')

@task
def log_status():
  """
  Display statistics per log tables
  """
  with cd(env.deploy_to):
    run('php shell/log.php status')

@task
def log_clean(days=0):
  """
  Clean Logs

  Usage:

      fab production magento.log_clean

  If you want to save the log files, you can pass the number of days to save the
  log files, for example:

      fab production magento.log_clean:7
  """
  with cd(env.deploy_to):
    if days > 0 and days.isdigit():
        run('php shell/log.php clean --days %s' % days)
    else:
        run('php shell/log.php clean')

@task
def compiler_state():
    """
    Show Compilation State
    """

@task
def compiler_compile():
    """
    Run Compilation Process
    """

@task
def compiler_clear():
    """
    Disable Compiler include path and Remove compiled files
    """

@task
def compiler_enable():
    """
    Enable Compiler include path
    """

@task
def compiler_disable():
    """
    Disable Compiler include path
    """
