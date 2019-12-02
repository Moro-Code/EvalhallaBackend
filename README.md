# Evalhalla Backend Repository 

This repo contains the backend application for the Evalhalla project built on Docker, Flask, Gunicorn, NGINX, PostgreSQL, RabbitMQ and Celery. The application is deployed on AWS cloud using Elastic Beanstalk. The purpose of this backend application is to process, store and get data for the Evalhalla Client by means of a REST API. This application is under development, the docs will change.  

## getting it running on your machine 

This project is using docker for development and deployment, as such it should be very simple to start the application on your machine 

### Prequesits

You will need to have docker on your machine and ensure the daemon is running. For linux you can install docker directly, for MacOs and Windows you should install docker desktop.
It is recommended that the daemon have atleast 8gb of memory and if your testing the production environment atleast 2 cpu cores available to it.

### Instructions

All commands will be in bash style, there are not any overly complex commands and as such should be transferable to windows

1. Navigate to the project root directory

```sh
cd ~/EvalhallaBackend
```

2. Access the docker-compose.yml file through your favourite IDE or terminal editor

```sh
nano docker-compose.yml
```

3. Change configuration as needed, If you are testing the production environment you will have to make sure the environment variables mentioned below are included. Here is the configuration needed for the development environment

```yaml
version: "3"

services:
  evalhalla-backend:
    build:
      context: ./app
      dockerfile: Dockerfile
      args:
        APP_ENV: development
    ports:
      - 5000:80
      - 5050:15672
```

4. Run it! If you need to rebuild the image include the ```--build``` option as shown 

```sh
docker-compose up --build 
```


The app should now be running. If you're in the development environment you should be able to access the RabbitMQ management UI at ```localhost:5050```
![Rabbit MQ Management UI](/docs/images/rabbitmq-management.png)


The application should be running on ```localhos:5000```

## Application Variables 

These are devided amongst three files ```default.py```, ```production.py```, ```development.py``` located in [/app/src/configs](/app/src/configs) folder

```default.py```: loaded by default regardless of environment

```development.py```: loaded only when the environment is the development environment. Overrides same name ```default.py``` configs

```production.py```: loaded only when the environment is the production environment. Overrides same name ```default.py``` configs

Most application variables can be set via an environment variable. This should be prepended by ```EVALHALLA_```. Thus, an application variable named ```DATABASE_NAME``` will have an environment variable of ```EVALHALLA_DATABASE_NAME```. 


### Variable Definitions 

```DATABASE_NAME```: The PostgreSQL database name which the application will access. If the database does not exist, the application should be given a user with sufficient privaleges to create it.
Environment Variable: Yes
Mandatory: Yes 

```DATABASE_HOST```: The PostgreSQL resolvable hostname.
Environment Variable: Yes
Mandatory: Yes

```DATABASE_USER```: The PostgreSQL user
Environment Variable: Yes 
Mandatory: Yes 

```DATABASE_PASSWORD```: The password of the PostgreSQL user
Environment Variable: Yes
Mandatory: Yes

Please use common sense when deciding how you set your variables so as to ensure credentials are secure. If you are unsure as how to do that. Grab your nearest technical senior, if that is not available atm, wait until it is or contact the owner of this repo.

