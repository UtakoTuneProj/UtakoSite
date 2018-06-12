FROM ubuntu:xenial
MAINTAINER nanamachi

RUN apt update &&\
    apt install -y python3 python3-dev python3-pip libmysqlclient-dev
COPY ./dependencies.dat /
RUN pip3 install -U pip &&\
    pip install -r /dependencies.dat
COPY  ./ /UtakoSite/
