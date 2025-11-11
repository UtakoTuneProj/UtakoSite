FROM python:3.12-trixie
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
