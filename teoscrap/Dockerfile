FROM python:3.6
MAINTAINER Piotr Zieliński

RUN apt-get -y update
RUN apt-get -y install --no-install-recommends \ 
    netcat-openbsd cron

COPY ./src /srv/src
COPY ./requiments.txt /srv

RUN pip install -r /srv/requiments.txt

EXPOSE 8080

WORKDIR /srv/src

COPY ./tools/entrypoint.sh /
RUN chmod +x /entrypoint.sh

COPY ./tools/wait-for-postgres.sh /
RUN chmod +x /wait-for-postgres.sh

COPY ./tools/cron-scrap.sh /
RUN chmod +x /cron-scrap.sh

RUN echo "@daily /srv/src/cron-scrap.sh" | crontab
