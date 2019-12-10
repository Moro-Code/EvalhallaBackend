from src.utils.errors.messages import (
    ENVIRONMENT_MUST_BE_PROVIDED, CONFIG_MODULE_NOT_FOUND, APPLICATION_VARIABLES_DEFINITION_DOES_NOT_EXIST,
    APPLICATION_VARIABLES_VALUE_IS_NOT_DICT
)

def load_application_variables(env):
    # ensure that a valid environment is provided 
    if env not in ["development", "production"]:
        raise ValueError(ENVIRONMENT_MUST_BE_PROVIDED)

    try:
        from src.config import default
    except ModuleNotFoundError:
        raise ValueError(
            CONFIG_MODULE_NOT_FOUND.format(
                config_module = "default",
                environment = env 
            )
        )
    
    # load default module into dictionary
    default_config_dict = vars(default) 

    # load additional module based upon environment
    environment_config_dict = None
    if env == "development":
        try:
            from src.config import development
        except ModuleNotFoundError:
            raise ValueError(
                CONFIG_MODULE_NOT_FOUND.format(
                    config_module = "development",
                    environment = env
                )
            )
        environment_config_dict = vars(development)
    else:
        try:
            from src.config import production
        except ModuleNotFoundError:
            raise ValueError(
                CONFIG_MODULE_NOT_FOUND.format(
                    config_module = "production",
                    environment = env 
                )
            )
        environment_config_dict = vars(production)
    
    application_variables = default_config_dict.get("APPLICATION_VARIABLES")

    if application_variables is None:
        raise ValueError(
            APPLICATION_VARIABLES_DEFINITION_DOES_NOT_EXIST
        )
    
    for variable in list(application_variables.keys()):

        # get the body of the configuration variable and ensure it's a dict
        config_body = application_variables[variable]
        
        if not isinstance(config_body, dict):
            raise TypeError(
                APPLICATION_VARIABLES_VALUE_IS_NOT_DICT.format(
                    config_var = variable,
                    incorrect_type = type(config_body).__name__
                )
            )
    

