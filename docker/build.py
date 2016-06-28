import subprocess
from setuptools import Command

_docker_build_cmds = '''
docker pull ubuntu
docker create -v /data --name data-store ubuntu
docker run --rm --volumes-from data-store ubuntu mkdir /data/models
docker build -t sysbio-simulate docker/simulate
docker build -t sysbio-plot docker/plot
'''

class DockerBuild(Command):
    """setuptools Command"""
    description = "run my command"
    user_options = []

    def initialize_options(self):
        """init options"""
        pass

    def finalize_options(self):
        """finalize options"""

        pass

    def run(self):
        for cmd in _docker_build_cmds.split('\n'):
            if cmd:
                subprocess.call(cmd, shell=True)

