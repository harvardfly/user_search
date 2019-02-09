#
# docker build -t user_search_nginx -f docker/nginx/Dockerfile .
#
FROM ubuntu:xenial

ADD ./docker/common/sources.list /etc/apt/sources.list
RUN apt-get -y update --fix-missing && apt-get -y update

RUN apt-get install -y nginx
