# Zenoss Data Client
python Client and consumer microservice for zenoss data API's

[![Build Status](https://travis-ci.org/lundybernard/zenoss-data.svg?branch=main)](https://travis-ci.org/lundybernard/zenoss-data)

## Installation
install in developer mode from source

```
python setup.py develop
```

## Run Functional tests

### Manually
start the web server on local host

```
zendat start
```

run tests against the web server

```
python -m unittest functional_tests/service_test.py
pytest functional_tests/service_test.py
```

### Run the service and tests via CLI
Install the package

```
python setup.py install
python setup.py develop
```

start webserver with cli

```
zendat start
```

Run functional tests

```
zendat test service
pytest functional_tests/service_test.py
```

### Run Container tests
to validate the docker container works properly, and docker-compose works

#### Manual Test
Run the container with docker-compose and test it with functional_tests

```
docker-compose build
docker-compose up
pytest functional_tests/service_test.py
```

#### Automatic test
container_test will run docker-compose before each test case,
and execute the test against the running container

```
python -m unittest container_tests/container_test.py
pytest container_tests/container_test.py

```

CLI

```
zendat run_container_tests



## rebuild local containers
sometimes necessary if container tests are failing
```
docker-compose down --rmi local
docker-compose build
```
