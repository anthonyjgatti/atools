
# TODO: Add logging.

# Load base modules.
import errno
import os
import shutil

# Load third-party modules.
import docker

class ContainerEnv(object): 

	def __init__(self, app_name, client, obj_dict, clean_flag):
		'''
		:param string app_name: Name of container application.
		:param client: Container client SDK object for building container images.
		:param bool clean_flag: Delete working directory without warning if True, warn otherwise.
		'''

		# Set conatiner application parameters.
		self.app_name = app_name
		self.client = client
		self.obj_dict = obj_dict

		# Set up working environment.
		self.workenvsetup(clean_flag)

	def workenvsetup(self, clean_flag):
		'''Helper function to set up container application working environment.'''

		self.clean_flag = clean_flag
		self.build_path = os.path.join(
			self.obj_dict['full_application_path'], 
			self.app_name
		)

		exit = False if os.path.exists(self.build_path) else True

		if exit:
			print('[WARN]: Project directory', self.build_path, 
				  'does not currently exist. It will be created.')
			self.clean_flag = True

		elif not exit and self.clean_flag:
			shutil.rmtree(self.build_path)

		else:
			message = 'The directory ' + self.build_path + ' is about to be deleted. Proceed (Y/N)?: '
			while not exit:	
				proceed = input(message)
				if proceed == 'Y':
					print('OK, removing directory ', self.build_path)
					shutil.rmtree(self.build_path)
					self.clean_flag = True; exit = True
				elif proceed == 'N':
					print('OK, please reconfigure your working directory and resubmit application.')
					exit = True
				else:
					print('Invalid input, please try again.')

		if self.clean_flag:
			try:
				os.makedirs(self.build_path)
			except OSError as exc:
				if exc.errno != errno.EEXIST:
					raise
				pass

	def dockerbuild(self):
		'''Build container image using Docker daemon if specified as container engine.'''

		if self.obj_dict['container_engine'] != 'docker':
			raise ValueError('Container engine is not specified to be Docker. Can\'t build image.')

		if 'build_path' not in self.__dict__:
			raise KeyError('Build path not specified, can\'t built image.')

		with open(os.path.join(self.build_path, 'Dockerfile'), 'w') as f:
			f.write(repr(self))

		self.client.images.build(
			path = self.build_path, 
			tag = self.app_name, 
			rm = True
		)

	def __repr__(self):
		'''Define object representation based on container engine. Use this to call ``repr(self)``
		in order to write out properly formated container file.'''

		if self.obj_dict['container_engine'] == 'docker':
			return '\n\n'.join([value[0] + ' ' + value[1] for value in self.obj_dict['_templateVars']])

