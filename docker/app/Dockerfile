#
# docker build -t user_search -f docker/app/Dockerfile .
#

FROM ubuntu:xenial

ADD ./docker/common/sources.list /etc/apt/sources.list
RUN apt-get -y update --fix-missing && apt-get -y update

# PYTHON环境
WORKDIR /proj
ADD requirements.txt /proj
RUN apt-get install -y python python-dev python3 python3-dev python3-pip
RUN apt-get install -y libmysqlclient-dev libssl-dev
RUN pip3 install -i https://pypi.doubanio.com/simple/ -r requirements.txt