RESTFUL_JSON = {
    "ensure_ascii": False
}


APP_NAME="EVALHALLA"

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
        "type": int
    },
    "AMQP_HOST": {
        "required": True,
        "default": "localhost"
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
        "type": int
    },
    "ALLOWED_ORIGINS": {
        "env": {
            "development": False
        },
        "config_opts": {
            "environment_variable": False
        },
        "required": False,
        "default": "*",
        "type": [str, list]
    }
}