from src.utils.errors.messages import (
    ENVIRONMENT_MUST_BE_PROVIDED, CONFIG_MODULE_NOT_FOUND, APPLICATION_VARIABLES_DEFINITION_DOES_NOT_EXIST,
    APPLICATION_VARIABLES_VALUE_IS_NOT_DICT, APPLICATION_NAME_IS_NOT_PROVIDED, APPLICATION_NAME_IS_NOT_STRING,
    APPLICATION_VARIABLES_STRUCTURE_ERROR, DIRECTIVE_IS_WRONG_TYPE, DIRECTIVE_IS_REQUIRED_AND_DOES_NOT_EXIST ,CONFIG_VAR_DOES_NOT_EXIST
)
import os 

PREMITIVE_TYPES = (int, str, float, bool)

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
    application_name = default_config_dict.get("APPLICATION_NAME")


    if application_variables is None:
        raise ValueError(
            APPLICATION_VARIABLES_DEFINITION_DOES_NOT_EXIST
        )
    
    if application_name is None:
        raise ValueError(
            APPLICATION_NAME_IS_NOT_PROVIDED
        )
    elif not isinstance(application_name, str):
        raise TypeError(
            APPLICATION_NAME_IS_NOT_STRING.format(
                incorrect_type = type(application_name).__name__
            )
        )

    configured_application_variables = {} 
    for variable in list(application_variables.keys()):

        # get the body of the configuration variable 
        config_body = application_variables[variable]
        
        # do some basic checks to ensure the required directives exist
        ## config_body must be a dict
        if not isinstance(config_body, dict):
            raise TypeError(
                APPLICATION_VARIABLES_VALUE_IS_NOT_DICT.format(
                    config_var = variable,
                    incorrect_type = type(config_body).__name__
                )
            )
        
        ## the type directive is requried and must be a type class or a list of type classes
        configuration_type = config_body.get("type")
        if configuration_type is None:
            raise ValueError(
                APPLICATION_VARIABLES_STRUCTURE_ERROR.format(
                    directive = "type",
                    error_detected = DIRECTIVE_IS_REQUIRED_AND_DOES_NOT_EXIST.format(
                        directive = "type"
                    )
                )
            )
        elif not ( isinstance(configuration_type, type) or isinstance(configuration_type, list) ):
            raise TypeError(
                APPLICATION_VARIABLES_STRUCTURE_ERROR.format(
                    directive = "type",
                    error_detected = DIRECTIVE_IS_WRONG_TYPE.format(
                        directive = "type",
                        directive_type = "list[type] or type",
                        directive_incorrect_type = type(configuration_type).__name__
                    )
                )
            )
        if isinstance(configuration_type, list):
            for t in configuration_type:
                if not isinstance(t, type):
                    raise TypeError(
                        APPLICATION_VARIABLES_STRUCTURE_ERROR.format(
                            directive = "type",
                            error_detected = DIRECTIVE_IS_WRONG_TYPE.format(
                                directive = "type",
                                directive_type = "list[type] or type",
                                directive_incorrect_type = type(configuration_type).__name__
                            )
                        )
                    )
        
        ## if the accepted_casts_to_type derictive is provided it must be a type or a list of types
        accepted_casts_to_type = config_body.get("accepted_casts_to_type")
        if accepted_casts_to_type is not None and not( isinstance(accepted_casts_to_type, type) or isinstance(accepted_casts_to_type, list)):
            raise TypeError(
                APPLICATION_VARIABLES_STRUCTURE_ERROR.format(
                    directive = "accepted_casts_to_type",
                    error_detected = DIRECTIVE_IS_WRONG_TYPE.format(
                        directive = "accepted_casts_to_type",
                        directive_type = "list[type] or type",
                        directive_incorrect_type = type(accepted_casts_to_type).__name__
                    )
                )
            )
        ### ensure that the type is a premitive 
        if isinstance(accepted_casts_to_type, type)  and accepted_casts_to_type not in PREMITIVE_TYPES:
            raise TypeError(
                APPLICATION_VARIABLES_STRUCTURE_ERROR.format(
                    directive = "accepted_casts_to_type",
                    error_detected = DIRECTIVE_IS_WRONG_TYPE.format(
                        directive = "accepted_casts_to_type",
                        directive_type = " or ".join(PREMITIVE_TYPES),
                        directive_incorrect_type = type(accepted_casts_to_type).__name__
                    )
                )
            )
        elif isinstance(accepted_casts_to_type, list):
            for t in accepted_casts_to_type:
                if not isinstance(t, type):
                    raise TypeError(
                        APPLICATION_VARIABLES_STRUCTURE_ERROR.format(
                            directive = "accepted_casts_to_type",
                            error_detected = DIRECTIVE_IS_WRONG_TYPE.format(
                                directive = "accepted_casts_to_type",
                                directive_type = "list[type] or type",
                                directive_incorrect_type = type(accepted_casts_to_type).__name__
                            )
                        )   
                    )
                # check to make sure type is a premitive
                elif t not in PREMITIVE_TYPES:
                    raise TypeError(
                        APPLICATION_VARIABLES_STRUCTURE_ERROR.format(
                            directive = "accepted_casts_to_type",
                            error_detected = DIRECTIVE_IS_WRONG_TYPE.format(
                                directive = "accepted_casts_to_type",
                                directive_type = " or ".join(PREMITIVE_TYPES),
                                directive_incorrect_type = type(accepted_casts_to_type).__name__
                            )
                        )   
                    )
                        
        # check if the configuration value should be set 
        if _check_if_should_configure_value(variable, env, env_opts= config_body.get("env")):
            configuration_value = _get_configuration_value(variable, application_name, environment_config_dict, config_body.get("config_opts"))

            # if the value for the configuration variable does not exist check if there is a default and if it is required
            # if there is a default we will set this as the value 
            # if it is required and still empty even after the default was checked we raise an error
            if configuration_value is not None:
                # run variable against checks, if it is successfull it will return a value 
                configuration_value = _run_variable_against_checks( configuration_value, configuration_type, accepted_casts_to_type, **config_body)
            elif config_body.get("default") is not None:
                configuration_value = config_body.get("default")
                configuration_value = _run_variable_against_checks( configuration_value, configuration_type, accepted_casts_to_type, **config_body)
            elif config_body.get("required") is None or config_body.get("required") == True:
                    raise ValueError(
                        CONFIG_VAR_DOES_NOT_EXIST.format(
                            config_var = variable
                        )
                    )
            configured_application_variables[variable] = configuration_value
    


                



def _get_configuration_value(variable, application_name, environment_config_dict, config_opts = None):
        # configuration options provided, check where to get the value of the application configuration from
        # if the config_opts is specified it is usually to overide the default behaviour of checking the configuration file 
        # and then grabbing the environment variable if it doesn't exist.
        if config_opts is not None:

            # ensure config opts is a dict 
            if not isinstance(config_opts, dict):
                raise TypeError(
                    APPLICATION_VARIABLES_STRUCTURE_ERROR.format(
                        config_var = variable,
                        error_detected = DIRECTIVE_IS_WRONG_TYPE.format(
                            directive = "config_opts",
                            directive_type = "dict",
                            directive_incorrect_type = type(config_opts).__name__
                        )
                    )
                )

            # this means that we cannot get the value from the configuration file, check if we can get this from the environment variable
            # if we cannot get this from the environment variable we will raise an error since one medium must be provided
            if config_opts.get("configuration_file_variable") == False:
                if config_opts.get("environment_variable") is None or config_opts.get("environment_variable") == True:
                    return os.environ.get(application_name + "_" + variable)
                else:
                    raise ValueError(
                        APPLICATION_VARIABLES_STRUCTURE_ERROR.format(
                            config_var = variable,
                            error_detected = (
                                "At least one medium for obtaining the value for the configuration variable must be specified " +
                                "both environment_variable and configuration_file_variable were set to False in the config_opts directive"
                            )
                        )
                    )
            if config_opts.get("environment_variable") == False:
                return environment_config_dict.get(variable)
        
        # default behaviour 
        else:
            configuration_file_variable = environment_config_dict.get(variable)
            if configuration_file_variable is None:
                return os.environ.get(variable)
            return configuration_file_variable


def _check_if_should_configure_value(variable, environment, env_opts = None):
    if env_opts is None:
        return True
    elif not isinstance(env_opts, dict):
        raise TypeError(
            APPLICATION_VARIABLES_STRUCTURE_ERROR.format(
                config_var = variable,
                error_detected = DIRECTIVE_IS_WRONG_TYPE.format(
                    directive = "env",
                    directive_type = "dict",
                    directive_incorrect_type = type(env_opts).__name__
                )
            )
        )
    return env_opts.get(environment) is True

def _check_if_type_is_valid(value, accepted_casts_to_type = None , *valid_types):
    # args here is the types passed in 
    valid = False
    coud_be_cast = []
    if accepted_casts_to_type is not None and not isinstance(accepted_casts_to_type, list):
        accepted_casts_to_type = [accepted_casts_to_type]
    for t in valid_types:
        if isinstance(value, t):
            valid = True
        # check whether the value can be cast into the correct type if the type is a primitive
        if accepted_casts_to_type is not None:
            if t in PREMITIVE_TYPES and type(value) in accepted_casts_to_type:
                try:
                    t(value)
                    coud_be_cast.append(t)
                    valid = True
                except ValueError:
                    continue
    return valid, coud_be_cast


def _run_variable_against_checks(value, valid_types, accepted_casts_to_type = None, **configuration):
    # TODO 
    # check if the type is valid, cast if needed and then return value 
    return "placeholder"



        
    

