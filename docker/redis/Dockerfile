#
# docker build -t user_search_redis -f docker/redis/Dockerfile .
#

FROM ubuntu:xenial

ADD ./docker/common/sources.list /etc/apt/sources.list
RUN apt-get -y update --fix-missing && apt-get -y update

RUN apt-get install -y redis-server
