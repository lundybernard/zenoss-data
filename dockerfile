FROM python:3.8-alpine
ADD . /opt/zendat
WORKDIR /opt/zendat
RUN pip install -r requirements.txt

# install the module
RUN python setup.py develop
# setup Environment variables
ENV ZENDAT_CONFIG=./config.yaml

# Run unittests, fails the build on failing tests
RUN python -m unittest discover zendat.tests -p '*_test.py'

# Use zendat cli to start the service
CMD ["zendat", "start"]
