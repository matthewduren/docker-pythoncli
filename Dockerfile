FROM ubuntu:14.04
MAINTAINER Matt Duren <matthewduren@gmail.com>

RUN echo "deb http://archive.ubuntu.com/ubuntu trusty main universe" > /etc/apt/sources.list && \
    apt-get update && \
    apt-get -y dist-upgrade

RUN apt-get -y install python \
                       python-mysqldb \
					   python-pip

RUN pip install boto3

WORKDIR /app/

ADD run.sh /usr/sbin/run.sh
ADD python.py /usr/sbin/python.py

ENTRYPOINT ["bash", "/usr/sbin/run.sh"]
