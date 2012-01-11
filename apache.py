"""
Apache2 tasks
"""
from fabric.api import *

@task
def restart():
    """
    Restart apache
    """
    sudo('/etc/init.d/apache2 restart')