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

@task
def install(version="1.6.1.0",localhost=False):
    """
    This task will install magento on the server

    Usage:

        fab production magento.install:version="1.6.1.0"

    To install on your localhost, run this command:

        fab magento.install:localhost=True
    """
    print 'All questions have defaults, update them if you want to change them'
    install_str = ''
    license_agreement_accepted = prompt('license_agreement_accepted',default='yes')
    install_str += ' --license_agreement_accepted %s' % license_agreement_accepted
    locale = prompt('locale',default='en_US')
    install_str += ' --locale %s' % locale
    timezone = prompt('timezone',default='America/Chicago')
    install_str += ' --timezone %s' % timezone
    default_currency = prompt('default_currency',default='USD')
    install_str += ' --default_currency %s' % default_currency
    db_host = prompt('db_host',default='localhost')
    install_str += ' --db_host %s' % db_host
    db_model = prompt('db_model',default='mysql4')
    install_str += ' --db_model %s' % db_model
    db_name = prompt('db_name',default='magento')
    install_str += ' --db_name %s' % db_name
    db_user = prompt('db_user',default='root')
    install_str += ' --db_user %s' % db_user
    db_pass = prompt('db_pass',default='root')
    install_str += ' --db_pass %s' % db_pass
    db_prefix = prompt('db_prefix')
    if db_prefix:
        install_str += ' --db_prefix %s' % db_prefix
    session_save = prompt('session_save (files|db)',default='files')
    install_str += ' --session_save %s' % session_save
    admin_frontname = prompt('admin_frontname',default='admin')
    install_str += ' --admin_frontname %s' % admin_frontname
    url = '';
    while len(url) <= 0:
        url = prompt('url')
    install_str += ' --url "%s"' % url
    skip_url_validation = prompt('skip_url_validation',default='yes')
    install_str += ' --skip_url_validation %s' % skip_url_validation
    use_rewrites = prompt('use_rewrites',default='yes')
    install_str += ' --use_rewrites %s' % use_rewrites
    use_secure = prompt('use_secure',default='no')
    install_str += ' --use_secure %s' % use_secure
    secure_base_url = prompt('secure_base_url')
    install_str += ' --secure_base_url "%s"' % secure_base_url
    use_secure_admin = prompt('use_secure_admin',default='no')
    install_str += ' --use_secure_admin "%s"' % use_secure_admin
    enable_charts = prompt('enable_charts',default='no')
    install_str += ' --enable_charts %s' % enable_charts
    admin_lastname = prompt('admin_lastname',default='admin')
    install_str += ' --admin_lastname %s' % admin_lastname
    admin_firstname = prompt('admin_firstname',default='admin')
    install_str += ' --admin_firstname %s' % admin_firstname
    admin_email = prompt('admin_email',default='admin@localhost.com')
    install_str += ' --admin_email "%s"' % admin_email
    admin_username = prompt('admin_username',default='admin')
    install_str += ' --admin_username %s' % admin_username
    admin_password = prompt('admin_password',default='magentoadmin123')
    install_str += ' --admin_password "%s"' % admin_password
    encryption_key = prompt('encryption_key')
    if encryption_key:
        install_str += ' --encryption_key "%s"' % encryption_key
    if localhost:
        local('wget http://www.magentocommerce.com/downloads/assets/%s/magento-%s.tar.gz' % (version, version))
        local('tar -zxvf magento-%s.tar.gz' % version)
        local('mv magento/* magento/.htaccess .')
        local('chmod o+w var var/.htaccess app/etc')
        local('chmod -R o+w media')
        local('rm -rf magento/ magento-%s.tar.gz' % version)
        local('rm -rf index.php.sample .htaccess.sample php.ini.sample LICENSE.txt STATUS.txt')
        local('php install.php -- %s' % install_str)
        local('rm install.php')
        if prompt('Would you like to download a .gitignore file?', default=False):
            local('wget --no-check-certificate -O .gitignore https://raw.github.com/github/gitignore/master/Magento.gitignore')
    else:
        run('wget http://www.magentocommerce.com/downloads/assets/%s/magento-%s.tar.gz' % (version, version))
        run('tar -zxvf magento-%s.tar.gz' % version)
        run('mv magento/* magento/.htaccess .')
        run('chmod o+w var var/.htaccess app/etc')
        run('chmod -R o+w media')
        run('rm -rf magento/ magento-%s.tar.gz' % version)
        run('rm -rf index.php.sample .htaccess.sample php.ini.sample LICENSE.txt STATUS.txt')
        run('php install.php -- %s' % install_str)
        run('rm install.php')