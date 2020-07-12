FROM python:3.5-jessie
LABEL MAINTAINER="nanamachi<7machi@nanamachi.net>"

RUN mkdir /UtakoSite
WORKDIR /UtakoSite

RUN pip3 install pipenv
COPY ./Pipfile ./Pipfile.lock /UtakoSite/
RUN pipenv install --system --deploy

COPY  ./ /UtakoSite/

ENTRYPOINT ["gunicorn"]
CMD ["UtakoSite.wsgi", "--bind", ":8193"]
ENV TZ="Asia/Tokyo"
