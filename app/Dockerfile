FROM  ubuntu:18.04

ARG APP_ENV
ARG AMQP_USER 
ARG AMQP_PASSWORD 
ARG AMQP_VHOST
ARG EVALHALLA_DATABASE_HOST
ARG EVALHALLA_DATABASE_USER
ARG EVALHALLA_DATABASE_PASSWORD
ARG EVALHALLA_DATABASE_NAME
 


ENV APP_ENV ${APP_ENV}
ENV FLASK_ENV ${APP_ENV}
ENV EVALHALLA_AMQP_USER ${AMQP_USER}
ENV EVALHALLA_AMQP_PASSWORD ${AMQP_PASSWORD}
ENV EVALHALLA_AMQP_VHOST ${AMQP_VHOST}
ENV EVALHALLA_DATABASE_HOST ${EVALHALLA_DATABASE_HOST}
ENV EVALHALLA_DATABASE_USER ${EVALHALLA_DATABASE_USER}
ENV EVALHALLA_DATABASE_NAME ${EVALHALLA_DATABASE_NAME}}
ENV EVALHALLA_DATABASE_PASSWORD ${EVALHALLA_DATABASE_PASSWORD}


RUN who

# install python 3.7
RUN apt update  &&  apt install -y software-properties-common curl && \
add-apt-repository -y ppa:deadsnakes/ppa && \
apt install -y python3.7 && python3.7 --version && apt install -y python3-pip && \
python3.7 -m pip install pip


# install rabbitMQ server
RUN apt update && \
curl -fsSL https://github.com/rabbitmq/signing-keys/releases/download/2.0/rabbitmq-release-signing-key.asc | apt-key add - && \
apt-get install -y apt-transport-https 

# install nginx web server
RUN apt update && \
apt install -y nginx && \
rm /etc/nginx/sites-available/default && \
rm /etc/nginx/sites-enabled/default

# set working directory and copy files in 
WORKDIR /home/root
COPY  . ./

# moving deb configs and install rabbitmq
RUN cp configs/bintray.rabbitmq.list /etc/apt/sources.list.d/bintray.rabbitmq.list && \
apt-get update -y && \
apt-get install rabbitmq-server -y --fix-missing

SHELL ["/bin/bash", "-c"]
RUN cp configs/nginx/default /etc/nginx/sites-enabled/default && nginx -t

# set the permission of the executable which will start the server
RUN chmod 777 configs/scripts/start.sh

# create virtual environment and install depedencies
RUN pip3 install virtualenv --upgrade && \
virtualenv -p /usr/bin/python3.7 venv && \
source venv/bin/activate && \
pip install -r requirements.txt && \
pip install gunicorn

# install celery configuration into init.d
RUN cp configs/etc/default/celeryd /etc/default/celeryd && \
cp configs/etc/init.d/celeryd.sh /etc/init.d/celeryd && \
chmod 777 /etc/init.d/celeryd

ENTRYPOINT [ "/bin/bash", "configs/scripts/start.sh" ]

EXPOSE 80
