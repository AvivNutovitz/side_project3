# Docker file for a slim Ubuntu-based Python3 image

FROM ubuntu:latest
MAINTAINER fnndsc "dev@babymri.org"

RUN apt-get update \
  && apt-get install -y python3-pip python3-dev \
  && cd /usr/local/bin \
  && ln -s /usr/bin/python3 python

RUN pip3 install pydicom keras google-cloud-storage numpy setuptools pandas argparse Pillow sklearn boto3 tensorflow seaborn jupyter

EXPOSE 9999/tcp

COPY noteobok.ipynb /tmp/noteobok.ipynb
COPY Zebra-448c2dd529a7.json /tmp/Zebra-448c2dd529a7.json
