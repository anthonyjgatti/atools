
import functools
from atools.container.container_base import ContainerBase
from atools.pyutils.generative import Generative, _generative

class Definition(ContainerBase, Generative):
    """
    Define the contents of a Dockerfile. Build them up through successive calls
    of ``commandbuilder`` which is decorated by _generative, indicating that
    successive calls of this method return updated instances of ``Definition``.
    """

    full_application_path, container_engine, container_orchestrator = None, None, None
    _valid_commands = {'base','run', 'entrypoint', 'cmd', 'env', 'user', 'workdir'}
    _templateVars = []

    def __init__(self, app_path, engine = 'docker', orchestrator = 'kubernetes'):

        # Set initial variables.
        self.full_application_path = app_path
        self.container_engine = engine
        self.container_orchestrator = orchestrator

        # Validate input path and set up environment.

    @property
    def render(self):
        """Create output Dockerfile string as property."""

        return self._templateVars

    @render.setter
    def render(self, value):
        """Setter for Dockerfile output that is called by class API."""

        self._templateVars.append(value)

    @_generative
    def base(self, command):
        """For base calls, reset the _templateVars list."""

        self._templateVars = []
        self.render = ('FROM', command)

    @_generative
    def _commandbuilder(self, method, command):
        """Build the sequence of commands in the Docker file."""

        self.render = (method.upper(), command)

    @_generative
    def env(self, variable, value):
        """Override default behavior of "env" for API consistency."""

        self._templateVars.append(('ENV', variable + ' ' + value))

    def __getattr__(self, name):
        """For all valid method calls not explicitly defined, pass invocation to
        ``commandbuilder`` as a partial method call, which carries the arguments
        (i.e. the "command") to the ``commandbuilder`` method.
        """

        if name in self._valid_commands:
            return functools.partial(self._commandbuilder, name)
        else:
            raise ValueError('Valid inputs are: ' + ', '.join(c for c in self.valid_commands))

    def __repr__(self):
        """Represent internal state like the Dockerfile format."""

        return '\n'.join([value[0] + ' ' + value[1] for value in self.render])
