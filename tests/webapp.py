
# Import third-party SDKs.
import docker

# Import custom orchestration modules.
from atools.container.docker import dockerfile

# Instantiate Docker client and define application path.
client = docker.from_env()
app_path = '/Users/anthony/code/working_output_dir'

# Create base Dockerfile definition object.
df = dockerfile.Definition(app_path)

# Define Vue Dockerfile and build image.
vue = df.base('node:slim') \
        .run('npm install -g vue-cli@latest') \
        .entrypoint('vue') \
        .cmd('-h')

#vue.build(stack_name = 'vue', 
#	      docker_client = client, 
#	      force_clean = True)

# Define StreamSets Data Collector image.
sdc_version = '2.7.2.0'
sdc = df.base('streamsets/datacollector:' + sdc_version) \
		.user('root')

# Loop through library set to create iterable.
libs = ['jdbc', 'mongodb']
install_base = '/opt/streamsetsdatacollector-' + sdc_version + \
	'/libexec/_stagelibs -install=streamsets-datacollector-'

sdc_lib_install = [install_base + lib for lib in libs]
sdc = sdc.runlist(sdc_lib_install) \
         .runlist('sadfklsdjf')
print(sdc)


# NEED TO ADD SOME SAFETY AROUND ORDERING HERE.
# Right now I have to call build on an object before redefining it.
# This isn't really ideal. Maybe just lose the generative approach?

#mysql = df.base('mysql:latest')

