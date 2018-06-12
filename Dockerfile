FROM python:3.5-jessie
MAINTAINER nanamachi

COPY ./dependencies.dat /
RUN pip3 install -U pip &&\
    pip install -r /dependencies.dat
COPY  ./ /UtakoSite/
