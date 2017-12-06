# from atools import kube

import jinja2

# def repcontroller(image, version = 'v1', replicas = 1, outport = 8080):

path = "/home/anthony/code/python/lebackup/atools/resources"
env = jinja2.Environment(
    loader = jinja2.FileSystemLoader(searchpath = path)
)
#env = jinja2.Environment( loader = jinja2.PackageLoader('atools', 'templates') )

# PUT THIS IN RESOURCE FILE?
service_lookup = {
    'mysql': {
        'port': 3306,
        'pvc': True,
        'frontend': False
    },
    'sdc': {
        'port': 18630,
        'pvc': True,
        'frontend': True
    }
}

def build(services, version = 'v1'):

    service_yaml = [srv(version, service) for service in services]
    pvc_yaml =
    for s in service_yaml:
        print(s)

    '''
    for service in services:

        # Build service.
        srv(version = version, service = service,  )

        # Build pvc if necessary, determined by pvc variable in service lookup.
        if service_lookup[service]['pvc']:
            SET_STORAGE_SHOMEHOW = '2Gi'
            pvc(version = version, name = service, storage = SET_STORAGE_SHOMEHOW)
    '''


def srv(version, service):

    servicetemplate = env.get_template( 'kube-service.jinja' )
    templateVars = {
        'version': version,
        'name': service,
        'port': service_lookup[service]['port'],
        'frontend': service_lookup[service]['frontend']
    }
    output = servicetemplate.render( templateVars )
    return output + '\n---'


def pvc(version, name, storage):

    pvctemplate = env.get_template( 'kube-pvc.jinja' )
    templateVars = {
        'version': version,
        'name': name,
        'storage': storage
    }
    output = pvctemplate.render( templateVars )
    return output + '\n---'


if __name__ == '__main__':

    services = ['sdc', 'mysql']
    build(services)
