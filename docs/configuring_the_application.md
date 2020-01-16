---
title: Configuring The Application
permalink: /configuring-the-application/
---

[Home](../index.md) [Site-Map](documentation_index.md)

# Configuring The Application ⚙️

Make sure you have the prerequisites installed first. Refer to the [prerequisites](/prerequisites) page for more information.

##  Development and Production mode 🏭

This application has two seperate modes, development and production. Different configuration variables are required depending on what mode you are running the application in. This goes without saying, but you should ensure you run in production mode when you deploy this application. The docker-compose file will allow you to test both of these modes in a development environment.

The application is started in production or development based on the value of an environment variable named ```APP_ENV```. To start this application in production simply set the environment variable ```APP_ENV``` to ```production``` and then run ```docker-compose up --build``` in your favourite CLI. To run in development set ```APP_ENV``` to ```development``` and then run the docker-compose command specified above. Make sure to include the ```--build``` flag whenever you switch between the two different modes.

There are a couple of key differences between production mode and development mode.

<table>
  <tr>
    <th>Component</th>
    <th>Production</th>
    <th>Development</th>
  </tr>
  <tr>
    <td>Configuring the Application</td>
    <td>Defaults are not provided for RabbitMQ and PostgreSQL credentials </td>
    <td>Defaults are provided for RabbitMQ and PostgresSQL credentials </td>
  </tr>
  <tr>
    <td> Running the Application</td>
    <td> Run behind multiple gunicorn workers equivalent to the number of CPU cores detected on the system </td>
    <td> <code>flask run</code> is used to start and run the application. This starts a built in WSGI server intended for development purposes only. 
    </td>
  </tr>
  <tr>
    <td> Exceptions </td>
    <td> Uncaught exceptions are not intercepted and the worker is killed as a result. The killed worker will be restarted by gunicorn </td>
    <td> Debugging is turned on, uncaught exceptions are intercepted and a debugging interface is provided by flask at the url ( localhost:5000 ). You can fine more details on this in the [flask documentation](https://flask.palletsprojects.com/en/1.1.x/quickstart/)</td>
  </tr>
  <tr>
    <td>Logging</td>
    <td> No logging is enabled </td>
    <td> Requests and emitted SQL to the PostgreSQL DB are logged to the command line </td>
  </tr>
</table>


## Application Variables 🌲

Application variables are values that determine the behaviour of the application. Some may be configurable by environment variables others by values in a configuration file or both! There are three configuration files you need to be aware of, all are located in the ```app/src/config``` file. It is important you understand what these files do in case you need to modify, add or remove variables. 

### default.py

This is probably the most important configuration file in the application. The default.py configuration file defines what application variables exist, where to set them from ( environment variable xor configuration file ) and any other behaviour regarding the setting of these variables. It only contains two variables which are required to be set```APPLICATION_NAME``` and ```APPLICATION_VARIABLES```


```py
# default.py file at the time of writing this doc 

APPLICATION_NAME="EVALHALLA"
APPLICATION_VARIABLES = {
    "DATABASE_NAME": {
        "required": True,
        "default": "evalhalla",
        "type": str
    },
    "DATABASE_HOST": {
        "required": True,
        "default": {
            "development": "postgres"
        },
        "type": str
    },
    "DATABASE_USER": {
        "required": True,
        "default": {
            "development": "postgresadmin"
        },
        "type": str
    },
    "DATABASE_PASSWORD": {
        "required": True,
        "default": {
            "development": "letmein"
        },
        "type": str
    },
    "DATABASE_PORT": {
        "required": True,
        "default": 5432,
        "type": int,
        "accepted_casts_to_type": str
    },
    "AMQP_HOST": {
        "required": True,
        "default": "localhost",
        "type": str
    },
    "AMQP_VHOST": {
        "required": True,
        "default": "evalhalla",
        "type": str
    },
    "AMQP_USER": {
        "required": True,
        "default": {
            "development": "dev_inst"
        },
        "type": str
    },
    "AMQP_PASSWORD": {
        "required": True,
        "default": {
            "development": "dev_inst"
        },
        "type": str
    },
    "AMQP_PORT": {
        "required": True,
        "default": 5672,
        "type": int,
        "accepted_casts_to_type": str
    },
    "ALLOWED_ORIGINS": {
        "config_opts": {
            "environment_variable": False
        },
        "required": False,
        "default": "*",
        "type": [str,list]
    },
    "RESTFUL_JSON": {
        "config_opts": {
            "environment_variable": False
        },
        "required": False,
        "default": {
            "ensure_ascii": False
        },
        "type": dict
    },
    "USE_SENTIMENT": {
        "required": False,
        "type": str,
        "default": "False" 
    },
    "BASIC_AUTH_ENABLED": {
        "required": False,
        "type": str,
        "default": "False"
    },
    "BASIC_AUTH_USERNAME": {
        "required": False,
        "type": str
    },
    "BASIC_AUTH_PASSWORD": {
        "required": False,
        "type": str 
    },
    "BASIC_AUTH_REALM": {
        "required": False,
        "type": str,
        "default": "Evalhalla Privileged Resource"
    },
    "ENABLE_FRONT_END": {
        "required": False,
        "type": str,
        "default": "False"
    }
}
```

#### APPLICATION_NAME 

The ```APPLICATION_NAME``` variable is pretty self explanatory. It allows you to set the name of the application. The main usage of this is when you are loading application variables from environment variables. In this case the value of ```APPLICATION_NAME``` will prefix the names of defined application variables ( {APPLICATION_NAME}_{VARIABLE_NAME} ). So, for example if you have a variable named ```DATABASE_HOST``` and a value of ```AWESOME_APPLICATION``` for ```APPLICATION_NAME```. The environment variable for ```DATABASE_HOST``` from which the value will be read is ```AWESOME_APPLICATION_DATABASE_HOST```. This way your variables are garunteed to be unique accross your environments from any other application that may exist in tandem 


#### APPLICATION_VARIABLES

This is a python dictionary that define what application variables exist and constraints around setting them which will be described below. 


The general structure for an application variable in the ```APPLICATION_VARIABLES``` dict is 

```py
{
  ...
  "SOME_VARIABLE": {
    ...
    "constraint_directive": "value"
  }
}
```

### APPLICATION_VARIABLES Constraint Directives 


#### *required*

__type__: ```boolean``` 

__description__: Specifies whether or not the defined variable is required. If the default derictive is present, this directive will have no effect. If the value does not exist in the configuration file or as an environment variable, the value of the default directive will be used if defined for the environment mode.

__is required__: ```False```

__default value for directive__: ```True```


### *default*

__type__: variable, depends on the type directive 

__description__: The default value to be used should a value not be able to be retrieved for the application variable. Note this negates the effect  *required* constraint directive, ( see *required* directive for more details ). You are able to control the default value for each environment mode ( production, development ), for example you may only want to have a default for the development environment and not the production environment. In this case you would set the value of the *default* constraint key to be a dictionary consisting of one key called ```development``` with the value being the default value for the application variable in the development environment. If you wanted different default values for production and development environments you just simply need to provide two key value pairs ```development``` and ```production``` 

```py 
{
  ...
  "SOME_VARIABLE":{
    ...
    "default": {
      "development": "some default value for development only"
      "production": "some default value for production only"
    }
  }
}

```

__is required__: ```False```

__sub directives__

