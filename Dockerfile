FROM python:3.5.3
ADD . /payments

WORKDIR /payments
RUN chmod +x /payments/run.sh

RUN apt-get update && apt-get install -y \
  netcat

RUN /bin/bash -c "pip3 install -r /payments/requirements/base.txt"
