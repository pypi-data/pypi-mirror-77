=====
Usage
=====


Building YAML configuration modules
-----------------------------------

The whole point of `gaeconf` is just creating a smart YAML parser that allows the user
using multiple inheritance in YAML hashes/dictionaries. Under the hood `gaeconf` parses
the yaml configuration module and builds Python classes out of the defined services.


*staging.yaml example file:*

.. code-block:: yaml

    services:
        StagingConfig:
            subnetwork_name: eme-staging
            env_variables:
                DJANGO_DEBUG: "False"
                SESSION_COOKIE_SECURE: "True"
                ALLOWED_HOSTS: '*.mydomain.com,*.mydomain.com'
                DB_HOST: 10.0.0.1
                DB_PORT: "6432"
                DB_NAME: mydb
                DB_USER: postgres
        BackendConfig:
            env: flex
            entrypoint: bash -c 'python3 manage.py migrate --noinput && gunicorn -w 8
            -b :$PORT server.wsgi --capture-output'
        BackendStagingConfig:
            inherits_from:
            - BackendConfig
            - StagingConfig
            service: backend-staging
            automatic_scaling:
                max_num_instances: 5
                min_num_instances: 1
        CeleryStagingConfig:
            inherits_from:
            - BackendConfig
            - StagingConfig
            service: celery-staging
            entrypoint: bash -c 'celery -A myapp worker'
            instance_tag: celery-staging
            automatic_scaling:
                max_num_instances: 1
                min_num_instances: 1


Selecting the GAE runtime environment
+++++++++++++++++++++++++++++++++++++

The runtime environment is specified using `env` key (standard|flex):

.. code-block:: yaml

    BackendConfig:
        env: flex


Defining mixins
+++++++++++++++

If you specify dictionary without a `service` key `gaeconf` will create a
Python class that can be used as a mixin for other subclases (take a look at 
`StagingConfig` in the example above).


Creating GAE yaml files
-----------------------

.. code-block:: bash

    gaeconf -m staging.yaml -s backend-staging


Exposing host environment variables in GAE yaml files
-----------------------

.. code-block:: bash

    gaeconf -m staging.yaml -s backend-staging -e CI_COMMIT_SHA


*extract of resulting yaml*

.. code-block:: yaml

    env_variables:
        ALLOWED_HOSTS: '*.mydomain.com,*.mydomain.com'
        CI_COMMIT_SHA: some-value
        DB_HOST: 10.0.0.1
        DB_NAME: mydb
        DB_PORT: '6432'
        DB_USER: postgres
        DJANGO_DEBUG: 'False'
        SESSION_COOKIE_SECURE: 'True'
