FROM ubuntu:16.04

MAINTAINER Juan Jose Aparicio <aparicio_juan@hotmail.com>

ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update && apt-get -y upgrade && apt-get install -y \
  git \
  nano \
  python3 \
  python3-dev \
  python3-setuptools \
  python3-pip \
  nginx \
  supervisor \
  sqlite3 && \
  pip3 install -U pip setuptools && \
  rm -rf /var/lib/apt/lists/*

#https://uwsgi.readthedocs.io/en/latest/tutorials/Django_and_nginx.html
RUN pip3 install uwsgi

# setup all the configfiles
RUN echo "daemon off;" >> /etc/nginx/nginx.conf
COPY nginx-app.conf /etc/nginx/sites-available/default
COPY supervisor-app.conf /etc/supervisor/conf.d/

# COPY requirements.txt and RUN pip install BEFORE adding the rest of your code, this
#will cause Docker's caching mechanism
# to prevent re-installing (all your) dependencies
#when you made a change a line or two in your app.
RUN mkdir -p /home/docker/code
VOLUME /home/docker/code

#for work in volume
COPY requirements.txt /home/docker/
RUN pip3 install -r /home/docker/requirements.txt

# add (the rest of) our code, for work test package
#COPY . /home/docker/code/

#little color
ENV TERM="xterm-256color"
ENV GREP_OPTIONS="--color=auto"

EXPOSE 80
EXPOSE 443
CMD ["supervisord", "-n"]
