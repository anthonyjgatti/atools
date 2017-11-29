#!/bin/python3

# Import secondary modules.
import jinja2

class Compose(object):

    path = "/home/anthony/code/python/lebackup/atools/resources"
    env = jinja2.Environment(
        loader = jinja2.FileSystemLoader(searchpath = path)
    )
    #env = jinja2.Environment( loader = jinja2.PackageLoader('atools', 'templates') )


    def __init__(self, version = 2, initenv = env):

        self.composetemplate = initenv.get_template( 'docker-compose.jinja' )
        self.templateVars = {
            'version': version,
            'services': []
        }


    def render(self):
        """
        Render docker-compose.yml file from Jinja template.

        """

        self.outputText = self.composetemplate.render( self.templateVars )
        print(self.outputText)

        # Write out file.


    def up(self, d = True, build = True):
        """
        Call ``docker-compose up`` on services defined in generated yaml file.

        :param bool d: Run container in the background (specifies ``-d`` in
            ``docker-compose up`` command.)
        :param bool build: Rebuild specifed images from any changes to Dockerfile
            (specifies ``--build`` flag in ``docker-compose up`` command.)

        """

        # What is the best thing to catch?
        try:
            self.render()
        except:
            print('Rendering problem!')

        # Issue docker compose up -d --build and any other options.


    def _templateBuilder(self, prefix, *args):
        """
        Builds compose template from arguments passed. Called by service
        functions below.

        """
        self.templateVars.update(
            {prefix + arg: args[0][arg] for arg in args[0] if arg != 'self'}
        )


    def mysql(self, containername, volume, rootpassword,
            schemaload = None, servicename = 'db', version = 'latest', outport = 3306):
        """
        Edit template to include mysql container.

        :param string containername: Name of mysql container.
        :param string volume: Local directory to mount as volume to mysql container
            for persistent storage.
        :param string rootpassword: Root password to mysql database in container.
        :param string schemaload: Schema to load on entrypoint to container.
        :param string servicename: Name of mysql container.
        :param string version: Version of mysql image to use.
        :param int outport: port to expose to other containers.

        """

        self.templateVars['services'].append('mysql')
        self._templateBuilder('mysql_', locals())




if __name__ == '__main__':

    compose = Compose()
    compose.mysql(containername = 'mysql_demo', volume = './some/mount',
        rootpassword = 'natty_is_gr8', schemaload = './mysql/init')
    compose.up()

    # How to tear down the container?
    # Delete the compose file?

    #from atools.docker import dockercompose as dc
    #compose = dc.Compose()

    #ISSUES
    #    Handle dependencies etc.
    #    Mysql init stuff.
    #    Container password handling stuff.
