- [MyShop](#myshop)
    + [Some ecommerce app](#some-ecommerce-app)
      - [Django project for Otus Python Basic course](#django-project-for-otus-python-basic-course)
  * [Features](#features)
- [Install](#install)
  * [Bare metal install](#bare-metal-install)
    + [Setup services:](#setup-services)
    + [Setup environment](#setup-environment)
    + [Run application](#run-application)
    + [Configure](#configure)
  * [Docker install](#docker-install)
    + [Setup services](#setup-services)
    + [Setup docker environment](#setup-docker-environment)
    + [Build image](#build-image)
    + [Migrate](#migrate)
    + [Run docker containers](#run-docker-containers)
    + [Create superuser](#create-superuser)
- [Develop](#develop)
  * [Bare metal install and setup services](#bare-metal-install-and-setup-services)
  * [Setup environment with an active django debug](#setup-environment-with-an-active-django-debug)
  * [Run application](#run-application-1)
  * [Configure](#configure-1)
- [Testing](#testing)
  * [Bare metal install](#bare-metal-install-1)
  * [Test project](#test-project)
  * [Test project with verbosity](#test-project-with-verbosity)
  * [Run coverage with verbosity 2](#run-coverage-with-verbosity-2)
  * [Look at the coverage report](#look-at-the-coverage-report)
  * [Look at the coverage html report](#look-at-the-coverage-html-report)
  * [Create the coverage xml report](#create-the-coverage-xml-report)
  * [Check if coverage under 100](#check-if-coverage-under-100)

<small><i><a href='http://ecotrust-canada.github.io/markdown-toc/'>Table of contents generated with markdown-toc</a></i></small>


# MyShop
[![Python application](https://github.com/avoevodin/otus_python_basic_project/actions/workflows/black.yml/badge.svg)](https://github.com/avoevodin/otus_python_basic_project/actions/workflows/black.yml)
[![Python application](https://github.com/avoevodin/otus_python_basic_project/actions/workflows/python-app.yml/badge.svg)](https://github.com/avoevodin/otus_python_basic_project/actions/workflows/python-app.yml)
[![codecov](https://codecov.io/gh/avoevodin/otus_python_basic_project/branch/master/graph/badge.svg?token=FzzJX0nCoA)](https://codecov.io/gh/avoevodin/otus_python_basic_project)

### Some ecommerce app
#### Django project for Otus Python Basic course

This app is the simple ecommerce sample, which helps you to go through the main points of 
the Django Web Development topic.
---

## Features
* Products list and detail views
* Session stored Customer Cart
* Order placement
* Custom auth models and views
* Delayed tasks with celery, rmq-broker and redis result backend
* Uwsgi application
* GitHub workflow and GitLab CI
* etc...
---

# Install

* Clone the rep:
```shell
git clone git@github.com:avoevodin/otus_python_basic_project.git
```

## Bare metal install

1. Create the venv:
```shell
python3 -m venv venv
```
2. Activate the venv
```shell
source venv/bin/activate
```
3. Install dependencies:
```shell
pip install -r requirements.txt
```

### Setup services:

1. Postgres
* create .env-postgres file with initial db options
```shell

cat > .env-postgres <<_EOF
POSTGRES_DB=myshop
POSTGRES_USER=myshop
POSTGRES_PASSWORD=secret
_EOF
```
* create docker instance

```shell
docker run -d --name myshop-postgres \
        --hostname myshop-postgres \
        -p 5432:5432 --env-file .env-postgres \
        postgres:14-alpine
```
2. RabbitMQ
* create .env-rmq file with initial rmq options
```shell
cat > .env-rmq <<_EOF
RABBITMQ_DEFAULT_USER=admin
RABBITMQ_DEFAULT_PASS=adminsecret
RABBITMQ_DEFAULT_VHOST=celery
_EOF
```
* create docker instance
```shell
docker run -d --name myshop-rmq \
        --hostname myshop-rmq \
        -p 5672:5672 -p 15672:15672 \
        --env-file .env-rmq \
        rabbitmq:3.10.7-management-alpine
```
3. Memcached
* create docker instance
```shell
docker run -d --name myshop-memcached \
        --hostname myshop-memcached \
        -p 11211:11211 \
        memcached:alpine
```
4. Redis
* create docker instance
```shell
docker run -d --name myshop-redis \
        --hostname myshop-redis \
        -p 6379:6379 \
        redis:7-alpine
```

### Setup environment
* create common .env file for the project
```shell
cat > .env <<_EOF
POSTGRES_DB=myshop
POSTGRES_USER=myshop
POSTGRES_PASSWORD=secret
POSTGRES_HOST=127.0.0.1
POSTGRES_PORT=5432
EMAIL_HOST=127.0.0.1
EMAIL_PORT=1025
EMAIL_HOST_USER=None
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
RABBITMQ_HOST=127.0.0.1
RABBITMQ_PORT=5672
RABBITMQ_DEFAULT_USER=admin
RABBITMQ_DEFAULT_PASS=adminsecret
RABBITMQ_DEFAULT_VHOST=celery
CACHE_BACKEND=django.core.cache.backends.memcached.MemcachedCache
CACHE_LOCATION=127.0.0.1:11211
REDIS_RESULTS_BACKEND=redis://127.0.0.1:6379/0
DJANGO_SETTINGS_MODULE=myshop.settings
DJANGO_DEBUG=False
_EOF
```
* export env vars
```shell
export $(cat .env)
```

### Run application
1. Apply migrations
```shell
cd myshop
python3 manage.py migrate --no-input
```
2. Collect static
```shell
# notice that you must be in the myshop/myshop directory
python3 manage.py collectstatic --no-input
```
3. Run uwsgi server
```shell
uwsgi --ini uwsgi.ini
```
4. Run celery worker
> notice that you must be in the myshop/myshop directory,
> python venv must be activated, env vars must be exported.
```shell
celery -A worker.app worker
```
### Configure
* Create superuser.
> Notice that you must be in the myshop/myshop directory,
> python venv must be activated, env vars must be exported.
```shell
python3 manage.py createsuperuser
```

## Docker install

### Setup services

[Setup services](#setup-services)

### Setup docker environment
> Create common .env file for the project. IP address just for example,
> find out your current address before configuring.
```shell
cat > .env <<_EOF
POSTGRES_DB=myshop
POSTGRES_USER=myshop
POSTGRES_PASSWORD=secret
POSTGRES_HOST=192.168.1.46
POSTGRES_PORT=5432
EMAIL_HOST=192.168.1.46
EMAIL_PORT=1025
EMAIL_HOST_USER=None
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
RABBITMQ_HOST=192.168.1.46
RABBITMQ_PORT=5672
RABBITMQ_DEFAULT_USER=admin
RABBITMQ_DEFAULT_PASS=adminsecret
RABBITMQ_DEFAULT_VHOST=celery
CACHE_BACKEND=django.core.cache.backends.memcached.MemcachedCache
CACHE_LOCATION=192.168.1.46:11211
REDIS_RESULTS_BACKEND=redis://192.168.1.46:6379/0
DJANGO_SETTINGS_MODULE=myshop.settings
DJANGO_DEBUG=False
_EOF
```

### Build image
```shell
docker build -f Dockerfile -t myshop-django ./
```

### Migrate
```shell
docker run --name myshop-migrations \
        --hostname myshop-migrations \
        --rm -ti --env-file .env \
        myshop-django \
        python3 manage.py migrate --no-input
```

### Run docker containers
1. Run uwsgi container:
```shell
docker run --name myshop-uwsgi \
        --hostname myshop-uwsgi \
        -d -p 8000:8000 --env-file .env \
        myshop-django
```
2. Run celery container:
```shell
docker run --name myshop-celery \
        --hostname myshop-celery \
        -d --env-file .env \
        myshop-django \
        celery -A worker.app worker
```
### Create superuser
```shell
docker run --name myshop-createsuperuser \
        --hostname myshop-createsuperuser \
        --rm -ti --env-file .env \
        myshop-django \
        python3 manage.py createsuperuser
```
---

# Develop

## Bare metal install and setup services
1. Install dev dependencies:
```shell
pip install -r requirements-dev.txt
```
2. [Bare metal install](#bare-metal-install)
3. [Setup services:](#setup-services)
4. Add Maildev for email tasks debugging
* create docker instance
```shell
docker run -d --name myshop-maildev \
        --hostname myshop-maildev \
        -p 1025:1025 -p 1080:1080 \
        maildev/maildev
```

## Setup environment with an active django debug
* create common .env file for the project
```shell
cat > .env <<_EOF
POSTGRES_DB=myshop
POSTGRES_USER=myshop
POSTGRES_PASSWORD=secret
POSTGRES_HOST=127.0.0.1
POSTGRES_PORT=5432
EMAIL_HOST=127.0.0.1
EMAIL_PORT=1025
EMAIL_HOST_USER=None
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
RABBITMQ_HOST=127.0.0.1
RABBITMQ_PORT=5672
RABBITMQ_DEFAULT_USER=admin
RABBITMQ_DEFAULT_PASS=adminsecret
RABBITMQ_DEFAULT_VHOST=celery
CACHE_BACKEND=django.core.cache.backends.memcached.MemcachedCache
CACHE_LOCATION=127.0.0.1:11211
REDIS_RESULTS_BACKEND=redis://127.0.0.1:6379/0
DJANGO_SETTINGS_MODULE=myshop.settings
DJANGO_DEBUG=True
_EOF

# export env vars
export $(cat .env)
```

## Run application
1. Apply migrations
```shell
cd myshop
python3 manage.py migrate --no-input
```
2. Run server
```shell
python3 manage.py runserver 0:8000
```
3. Run celery worker
> notice that you must be in the myshop/myshop directory,
> python venv must be activated, env vars must be exported.
```shell
celery -A worker.app worker
```
4. Make sure that [Django Debug Toolbar](https://django-debug-toolbar.readthedocs.io/en/latest/installation.html)
is configured correctly.

## Configure
1. Create superuser.
> Notice that you must be in the myshop/myshop directory,
> python venv must be activated, env vars must be exported.
```shell
python3 manage.py createsuperuser
```
2. To init filling db with fake data run:
```shell
python manage.py fill_db_with_fake_data
```
---

# Testing

## Bare metal install

1. [Bare metal install](#bare-metal-install)

## Test project
> notice that you must be in the myshop/myshop directory,
> python venv must be activated, env vars must be exported.
```shell
python3 manage.py test
```

## Test project with verbosity
> notice that you must be in the myshop/myshop directory
```shell
python3 manage.py test -v 2
```

## Run coverage with verbosity 2
> notice that you must be in the myshop/myshop directory
```shell
coverage run --source='.' manage.py test --verbosity=2
```

## Look at the coverage report
> notice that you must be in the myshop/myshop directory
```shell
coverage report -m
```

## Look at the coverage html report
> notice that you must be in the myshop/myshop directory
```shell
coverage html
open htmlcov/index.html
```

## Create the coverage xml report
> notice that you must be in the myshop/myshop directory
```shell
coverage xml
```

## Check if coverage under 100
> notice that you must be in the myshop/myshop directory
```shell
coverage report --fail-under=100
```

* Profit
