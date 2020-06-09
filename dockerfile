FROM python:3.4-alpine
ADD . /opt/zendat
WORKDIR /opt/zendat
RUN pip install -r requirements.txt

# install the module
RUN python setup.py develop
# Run unittests, fails the build on failing tests
RUN python -m unittest discover zendat.tests -p '*_test.py'

# Use zendat cli to start the service
CMD ["zendat", "start"]
