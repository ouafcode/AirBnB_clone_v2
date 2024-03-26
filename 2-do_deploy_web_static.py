#!/usr/bin/python3
# Fabric script that generates a .tgz archive from the
# using the function do_pack
import os
from fabric.api import run, put, env

env.hosts = ['54.173.247.174', '100.24.72.14']
env.user = "ubuntu"


def do_deploy(archive_path):
    """Create a tar gzipped archive"""
    if os.path.exists(archive_path) is False:
        return False
    try:
        file_n = archive_path.split("/")[-1]
        no_ext = file_n.split(".")[0]
        path = "/data/web_static/releases/"
        put(archive_path, '/tmp/')
        run('mkdir -p {}{}/'.format(path, no_ext))
        run('tar -xzf /tmp/{} -C {}{}/'.format(file_n, path, no_ext))
        run('rm /tmp/{}'.format(file_n))
        run('mv {0}{1}/web_static/* {0}{1}/'.format(path, no_ext))
        run('rm -rf {}{}/web_static'.format(path, no_ext))
        run('rm -rf /data/web_static/current')
        run('ln -s {}{}/ /data/web_static/current'.format(path, no_ext))
        return True

    except Exception:
        return False
