'''
A collection of classes with static methods to aid the creation of container definition files
with specific commands for general actions of individual clients.
'''

class SdcFactory(object):
	'''
	Set of static methods to configure specific commands for the StreamSets data collector.
	This may be implementable using the SDC SDK.
	'''

	version = '2.7.0.0'

	@staticmethod
	def libinstaller(pkg, version = version):
		'''Return command string to install packages in SDC.'''

		return ('/opt/streamsetsdatacollector-{}/libexec/_stagelibs' + \
			' -install=streamsets-datacollector-{}-lib').format(version, pkg)

	@staticmethod
	def jdbcinstaller(db, db_version):
		'''Return command string to install JDBC driver from selected sources.'''

		# Eventually put this into a resources file.
		lookup = {
	      'mysql': {
		    '5.1.44': {
			  'name': 'mysql-connector-java-5.1.44',
			  'url': 'https://mysql.com/get/Downloads/Connector-J/mysql-connector-java-5.1.44.tar.gz'
			}
		  }
		}

		name = lookup[db][db_version]['name']
		url = lookup[db][db_version]['url']

		return ' \\\n  '.join([
			'mkdir -p /opt/sdc-extras/streamsets-datacollector-jdbc-lib/lib &&',
			'chown -R sdc:sdc /opt/sdc-extras &&',
			'curl -L -o /tmp/{0}',
			'  {1} &&',
			'tar -xf /tmp/{0} -C /tmp &&',
			'cp /tmp/{0}/{0}-bin.jar',
			'  /opt/sdc-extras/streamsets-datacollector-jdbc-lib/lib'
		]).format(name, url)

	@staticmethod
	def makeextras(version = version):
		'''Set extras directory in SDC instance.'''

		return ' \\\n  '.join([
			'echo \'export STREAMSETS_LIBRARIES_EXTRA_DIR=\"/opt/sdc-extras\"\'',
			'>> /opt/streamsets-datacollector-{0}/libexec/sdc-env.sh &&',
			'echo \'export STREAMSETS_LIBRARIES_EXTRA_DIR=\"/opt/sdc-extras\"\'',
			'>> /opt/streamsets-datacollector-{0}/libexec/sdcd-env.sh',
			'echo \'grant codebase \"file:///opt/sdc-extras-\" {{\' >> /etc/sdc/sdc-security.policy',
			'  && echo \'  permission java.security.AllPermission;\' >> /etc/sdc/sdc-security.policy',
			'  && echo \'}};\' >> /etc/sdc/sdc-security.policy' # Better way to do this???
		]).format(version)



