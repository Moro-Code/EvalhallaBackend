# Evalhalla Backend Repository 

This repo contains the backend application for the Evalhalla project built on Docker, Flask, Gunicorn, NGINX, PostgreSQL, RabbitMQ and Celery. The application is deployed on AWS cloud using Elastic Beanstalk. The purpose of this backend application is to process, store and get data for the Evalhalla Client by means of a REST API. This application is under development, the docs will change.  

[configuring the application](/configuring_the_application.md)

## Getting it running on your machine 

This project is using docker for development and deployment, as such it should be very simple to start the application on your machine 

### Prequesits

You will need to have docker on your machine and ensure the daemon is running. For linux you can install docker directly, for MacOS and Windows you should install docker desktop.
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
    depends_on:
      - postgres
    build:
      context: ./app
      dockerfile: Dockerfile
      args:
        APP_ENV: production
    ports:
      - 5000:80
      - 5050:15672
    environment:
      - EVALHALLA_AMQP_USER=dev_inst
      - EVALHALLA_AMQP_PASSWORD=dev_inst
      - EVALHALLA_AMQP_VHOST=evalhalla
      - EVALHALLA_DATABASE_USER=postgresadmin
      - EVALHALLA_DATABASE_PASSWORD=letmein
      - EVALHALLA_DATABASE_HOST=postgres
      - EVALHALLA_DATABASE_NAME=evalhalla
  postgres:
    image: "postgres:11.6"
    environment:
      - POSTGRES_USER=postgresadmin
      - POSTGRES_PASSWORD=letmein
    volumes:
      - ./postgres:/var/lib/postgresqldata
    ports:
      - 5432:5432
```

Shown above is the default docker-compose configuration provided to you at the base directory. It will start the app in productuion mode. At a minimum, any added functionality
should be tested in the production environment before being deployed to production.


4. Run it! If you need to rebuild the image include the ```--build``` option as shown 

```sh
docker-compose up --build 
```


The app should now be running. If you're in the development environment you should be able to access the RabbitMQ management UI at ```localhost:5050```
![Rabbit MQ Management UI](/docs/images/rabbitmq-management.png)


The application should be running on ```localhost:5000```

## Application Variables 

These are devided amongst three files ```default.py```, ```production.py```, ```development.py``` located in [/app/src/configs](/app/src/configs) folder

```default.py```: loaded by default regardless of environment

```development.py```: loaded only when the environment is the development environment. Overrides same name ```default.py``` configs

```production.py```: loaded only when the environment is the production environment. Overrides same name ```default.py``` configs

Most application variables can be set via an environment variable. This should be prepended by ```EVALHALLA_```. Thus, an application variable named ```DATABASE_NAME``` will have an environment variable of ```EVALHALLA_DATABASE_NAME```. 


### Variable Definitions 

```DATABASE_NAME```: The PostgreSQL database name which the application will access. If the database does not exist, the application should be given a user with sufficient privaleges to create it.

Environment Variable: Yes

Mandatory: No

Default: evalhalla 

```DATABASE_HOST```: The PostgreSQL resolvable hostname.

Environment Variable: Yes

Mandatory: Yes


```DATABASE_USER```: The PostgreSQL user

Environment Variable: Yes 

Mandatory: Yes 

```DATABASE_PASSWORD```: The password of the PostgreSQL user

Environment Variable: Yes

Mandatory: Yes

```DATABASE_PORT```: The port of the PostgreSQL user

Environment Variable: Yes 

Mandatory: No

Default: 5432

```AMQP_HOST```: The host of the RabbitMQ instance 

Evironment Variable: Yes

Mandatory: No

Default: localhost

```AMQP_VHOST```: The v-host that will be used on the RabbitMQ instance

Environment Variable: Yes

Mandatory: No

Default: evalhalla 

```AMQP_PORT```: The port of the RabbitMQ instance

Envrionment Variable: Yes

Mandatory: No

Default: 5672

```AMQP_PASSWORD```: The password of the specified user for the RabbitMQ 

instance

Environment Variable: Yes 

Mandatory: Yes 

```AMQP_USER```: The user which will be used to access the RabbitMQ instance

Environment Variable: No

Mandatory: Yes

```RESTFUL_JSON```: Options for JSON API

Environment Variable: No

Mandatory: No 

Default: 

```python
RESTFUL_JSON = {
  "ensure_ascii": False
}
```

Please use common sense when deciding how you set your variables so as to ensure credentials are secure. If you are unsure as how to do that. Grab your nearest technical senior, if that is not available atm, wait until it is or contact the owner of this repo.


## API Routes 

Here you will find a description of the different routes for this API and what you can do 

### Evalese 
Read and create evalese. Evalese is the markdown based langauge which generates the surveys

```
GET     /evalese /evalese/<surveyName>

Description: Read the most recent evalese from a particular survey 

Parameters
----------

surveyName

type: str
mandatory: yes
description: The survey name for which you are trying to get the evalese


Responses
---------

200

description: Survey was found and evalese was successfully retrieved and returned 

response body:

{
  "surveyName": str, # the name of the survey
  "evalese": str, # the evalese
  "createdOn": datetime string iso format UTC,  # when this evalese was created
  "uuid": str, # unique identifier for this evalese  

}

404

description: The survey could not be found or there is no evalese for the specified survey

response body:
{
  "error": "NO_RESOURCE_FOUND",
  "message": str
}

400 

description: Bad request, most likely as a result of missing surveyName parameter

resposne body:
{
  "error": "API_PARAMETER_MISSING"
  "message": str
}

500

description: Internal application failure :(

response_body
{
  "error":INTERNAL_ERROR,
  "message": str

}

```

```
POST     /evalese /evalese/<surveyName>

Description: Create evalese for a particular survey. If the Survey doesn't exist it will be created for you

Parameters
----------

surveyName

type: str
mandatory: yes
description: The survey name for which you are trying to get the evalese


Request
-------

surveyName

type: str
mandatory: If provided via parameters no, otherwise yes
description: The surveyname for which you are trying to create the evalese

Responses
---------

200

description: Evalese was successfully created for the specified survey. The response will be the newly created evalese

response body:

{
  "surveyName": str, # the name of the survey
  "evalese": str, # the evalese
  "createdOn": datetime string iso format UTC,  # when this evalese was created
  "uuid": str, # unique identifier for this evalese  

}


400 

description: Bad request, most likely as a result of missing surveyName parameter or in the request body 

resposne body:
{
  "error": "API_PARAMETER_MISSING"
  "message": str
}

500

description: Internal application failure :(

response_body
{
  "error":INTERNAL_ERROR,
  "message": str

}

```


