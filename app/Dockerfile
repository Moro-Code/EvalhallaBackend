FROM  ubuntu:18.04

ARG APP_ENV

ENV APP_ENV = ${APP_ENV}
ENV FLASK_ENV = ${APP_ENV}}

RUN who

# set working directory and copy files in 
WORKDIR /home/root
COPY  . ./


# install python 3.7
RUN apt update  && apt install -y software-properties-common && \
add-apt-repository -y ppa:deadsnakes/ppa && \
apt install -y python3.7 && python3.7 --version


# install rabbitMQ server
RUN apt update && apt install -y curl && \
curl -fsSL https://github.com/rabbitmq/signing-keys/releases/download/2.0/rabbitmq-release-signing-key.asc | apt-key add - && \
apt-get install -y apt-transport-https && \
cp configs/bintray.rabbitmq.list /etc/apt/sources.list.d/bintray.rabbitmq.list && \
apt-get update -y && \
apt-get install rabbitmq-server -y --fix-missing

RUN if [ "$APP_ENV" = "development" ]; then rabbitmq-plugins enable rabbitmq_management ; fi



EXPOSE 15672
