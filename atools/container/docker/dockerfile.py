
# TODO: Add logging.

# Load base modules.
import functools
import os

# Import third-party modules.
import docker

# Load custom modules.
from atools.container.containerbase import ContainerBase
from atools.container.workenv import ContainerEnv
from atools.pyutils.generative import Generative, _generative

class Definition(ContainerBase, Generative):
    '''
    Define the contents of a Dockerfile. Build them up through successive calls
    of ``commandbuilder`` which is decorated by _generative, indicating that
    successive calls of this method return updated instances of ``Definition``.
    '''

    full_application_path, container_engine, container_orchestrator = '', '', ''
    _valid_commands = {'build','base','run','runlist','entrypoint','cmd','env','user','workdir'}
    _templateVars = []

    def __init__(self, app_path, engine = 'docker', orchestrator = 'kubernetes'):

        # Set initial variables.
        self.full_application_path = app_path
        self.container_engine = engine
        self.container_orchestrator = orchestrator

    @_generative
    def _commandbuilder(self, method, *command):
        '''Build the sequence of commands in the Docker file.
        For ``base`` calls, reset the base _templateVars object.'''

        if method == 'base':
            self._templateVars = [('FROM', command[0])]
        elif method in ['entrypoint','cmd']:
            self._templateVars.append(
                (method.upper(), '["' + '", "'.join(c for c in command) + '"]')
            )
        else:
            self._templateVars.append((method.upper(), command[0]))

    @_generative
    def env(self, variable, value):
        '''Override default behavior of "env" for API consistency'''

        self._templateVars.append(('ENV', variable + ' ' + value))

    @_generative
    def runlist(self, iterable: list):
        '''Takes a Python iterable and puts each of its contents one single 
        RUN command in the output Dockerfile, using && and \.'''

        if isinstance(iterable, list):
            command = ' && \\\n  '.join(iterable)
            self._templateVars.append(('RUN', command))
        else:
            raise TypeError('runlist must be called with list object.')

    @_generative
    def build(self, stack_name, docker_client, force_clean = False):
        '''
        Flush template vars to Dockerfile and call docker build through Docker SDK. The goal 
        is to allow callers of this method to pass their own homebaked container environment.  

        :param stack_name: Name given to container, both in build and in directory structure.
        :param docker_client: Instance of ``DockerClient`` class from ``docker`` package. 
        '''

        if isinstance(docker_client, docker.DockerClient):      
            env = ContainerEnv(stack_name, docker_client, self.__dict__, force_clean)
            env.dockerbuild()
        else:
            raise ValueError('Param docker_client must be an instance of docker.DockerClient.')

    def __getattr__(self, name):
        '''For all valid method calls not explicitly defined, pass invocation to
        ``commandbuilder`` as a partial method call, which carries the arguments
        (i.e. the "command") to the ``commandbuilder`` method.
        '''

        if name in self._valid_commands:
            return functools.partial(self._commandbuilder, name)
        else:
            raise ValueError('Valid inputs are: ' + ', '.join(c for c in self._valid_commands))

    def __repr__(self):
        '''Represent internal state like the Dockerfile format.'''

        return '\n\n'.join([value[0] + ' ' + value[1] for value in self._templateVars])
