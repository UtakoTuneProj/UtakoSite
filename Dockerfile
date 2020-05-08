FROM python:3.5-jessie
MAINTAINER nanamachi

COPY ./dependencies.dat /
RUN pip3 install -U pip &&\
    pip install -r /dependencies.dat
COPY  ./ /UtakoSite/

ENV TZ='Asia/Tokyo'
WORKDIR /UtakoSite
ENTRYPOINT ['gunicorn']
CMD ['UtakoSite.wsgi', '--bind', ':8193']
