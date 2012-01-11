Fabfiles
========

This is a library of files that allow you to use fabric with various projects you already have

Installation
============

    cd ~
    git clone git://github.com/JoshuaEstes/fabfiles.git
    cd /var/www/website
    ln -s ~/fabfiles/magento.py ~+/

The above example is for magento projects. Next you will need to create a fabfile.py

    vi fabfile.py

Now enter some content in fabfile.py

    from fabric.api import *
    import magento

    # The path we use to push code to
    env.deploy_to = '/path/to/magento';

    @task
    def beta():
        "Set the servers"
        env.hosts = ['username@beta.example.com:port']

    @task
    def production():
        "Set the production servers"
        env.hosts = ['username@example.com:port']

Now save and exit vim, run fab -l to view a list
