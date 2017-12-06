
# Import third-party SDKs.
import docker

# Import custom orchestration modules.
from atools.container.docker import dockerfile
from atools.container.client_libs import SdcFactory

# Instantiate Docker client and define application path.
client = docker.from_env()
app_path = '/Users/anthony/code/working_output_dir'

# 0. Create base Dockerfile definition object.
df = dockerfile.Definition(app_path)

# 1. Define Vue Dockerfile and build image.
vue = df.base('node:slim') \
        .run('npm install -g vue-cli@latest') \
        .entrypoint('vue', '-h')

vue.build(stack_name = 'vue', 
	      docker_client = client, 
	      force_clean = True)

# 2. Define StreamSets Data Collector image.

# Define variables to pass to Dockerfile definition.
sdc_version = '2.7.2.0'
libs = ['jdbc', 'mongodb']

# Define Dockerfile.
sdc = df.base('streamsets/datacollector:' + sdc_version) \
		.user('root') \
		.runlist([SdcFactory.libinstaller(lib, sdc_version) for lib in libs]) \
		.run(SdcFactory.jdbcinstaller('mysql', '5.1.44')) \
		.run(SdcFactory.makeextras(sdc_version)) \
		.cmd('dc', '-exec')

print(sdc)


# NEED TO ADD SOME SAFETY AROUND ORDERING HERE.
# Right now I have to call build on an object before redefining it.
# This isn't really ideal. Maybe just lose the generative approach?
