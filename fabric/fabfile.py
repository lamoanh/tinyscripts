from fabric.api import *

SALT_MASTER = '192.168.36.23'
GUEST_NAME = "ubun2"
MY_USER = ""
MY_PASSWD = ""
#env.user = ''
#env.password = ''

def myhost():
    env.hosts = ["192.168.32.9" + str(i) for i in range(1,4)] + [SALT_MASTER]


def master():
    env.hosts = [SALT_MASTER]

def copyssh():
    for host in env.hosts:
        local("ssh-copy-id " + MY_USER + "@" + host)

def change_hostname(hostname):
    sudo("echo %s > /etc/hostname" % hostname)
    sudo("sed -i 's/127.0.1.1.*/127.0.1.1\t%s/' /etc/hosts" % hostname)

def salt_bootstrap():
    sudo('wget -O - http://bootstrap.saltstack.org | sudo sh')

def salt_restart():
    sudo('service salt-minion restart')

def salt_rmkey():
    sudo('rm -f /etc/salt/pki/minion/minion_master.pub')

def salt_config():
    sudo("sed -i 's/[#]*master:.*/master: %s/g' /etc/salt/minion" % SALT_MASTER)
    salt_restart()

def create_sudo():
    with settings(warn_only=True):
        sudo("useradd " + MY_USER + " -G sudo,adm -s /bin/bash -m")
        sudo("echo -e '%s\n%s' | passwd %s" % (MY_PASSWD, MY_PASSWD, MY_USER))

def fix_apt():
    sudo('rm -r /var/lib/apt/lists')
    sudo('mkdir -p /var/lib/apt/lists/partial')
