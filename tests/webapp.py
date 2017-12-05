
from atools.docker import dockerfile

application_path = '/hello/absolute/path'

df = dockerfile.Definition(application_path)

vue = df.base('node:slim') \
        .run('npm install -g vue-cli@latest') \
        .env('JDBC_LIB','xyz')

mysql = df.base('mysql:latest')

print(vue)

