
from abc import ABCMeta, abstractmethod, abstractproperty

class ContainerBase(object):
    """
    Base container object that defines an entire container application.
    """

    __metaclass__ = ABCMeta

    @abstractproperty
    def container_engine(self):
        """
        :return: the container orchestrator.
        :rtype: unicode
        """
        raise NotImplementedError()

    @abstractproperty
    def container_orchestrator(self):
        """
        :return: the container orchestrator.
        :rtype: unicode
        """
        raise NotImplementedError()

    @abstractproperty
    def full_application_path(self):
        """
        :return: The absolute path to the directory that contains the application definition.
        :rtype: unicode
        """
        raise NotImplementedError()
