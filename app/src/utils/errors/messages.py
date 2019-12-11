#### GENERAL ####

ARGUMENT_MUST_BE_PROVIDED = (
    "The argument '{argument}' must be provided. "
)


ARGUMENT_IS_INCORRECT_TYPE = (
    "The argument '{argument}' is of incorrect type {incorrect_type}. Argument should be of type {expected_type}. "
)

#### APPLICATION CONFIGURATION #### 

CONFIG_VAR_DOES_NOT_EXIST = (
      "{config_var} is a required application variable and was not provided. " +
      "please set this variable according to the APPLICATION_VARIABLES configuration " +
      "or modify the configuration of this variable with a default directive."
)

APPLICATION_VARIABLES_DEFINITION_DOES_NOT_EXIST = (
    "The config values APPLICATION_VARIABLES is required in order to configure this application. Please provide this " +
    "and place this within the src/config/default.py module"
)

APPLICATION_NAME_IS_NOT_PROVIDED = (
    "The config APPLICATION_NAME is required in order to configure this application. Please provide this " +
    "and place this within the src/config/default.py"
)

APPLICATION_NAME_IS_NOT_STRING = (
    "The config APPLICATION_NAME must be of type string, recieved {incorrect_type}"
)

APPLICATION_VARIABLES_VALUE_IS_NOT_DICT = (
    "The config {config_var} was specified but the value for this in the " +
    "APPLICATION_VARIABLES dict is not of type dict. Instead found type {incorrect_type}. " +
    "The value for any configuration variable must be a dict. "
)

APPLICATION_VARIABLES_STRUCTURE_ERROR = (
    "An error was detected in the APPLICATION_VARIABLES configuration specification. " +
    "For the configuration variable {config_var}, the following error was detected: {error_detected}"
)

DIRECTIVE_IS_WRONG_TYPE = (
    "The configuration directive {directive} is of incorrect type, expected {directive_type}. " +
    "instead recieved {directive_incorrect_type}. "
)

DIRECTIVE_IS_REQUIRED_AND_DOES_NOT_EXIST = (
    "The configuration directive {directive} is required and was not set." 
)

CONFIG_IS_WRONG_TYPE = (
    "The config variable {config_var} is of incorrect type, expected {config_var_type}. " +
    "instead recieved {config_incorrect_type}. "
)

ENVIRONMENT_MUST_BE_PROVIDED = "A valid environment must be specified to configure the application, either development or production"

CONFIG_MODULE_NOT_FOUND  = (
    "The following config module {config_module} is required for the environment {environment} "+
    "and could not be found in the src/configs folder"    
)



#### API ERRORS ####
API_PARAMETER_MUST_BE_PROVIDED = (
    "In order to access the resource {resource}, the parameter {parameter} must be provided. "
)

PAYLOAD_MUST_BE_SENT = (
    "The following resource {resource} requires a payload in body of the request"
)

#### CRUD ERRORS 

MISSING_PARAMETER_FOR_DATA_OPERATION = (
    "The following  parameter(s) are required for a {operation} " +
    "on the table {table}: {parameters} . "
)

NO_SURVEY_FOUND = (
    "No survey with the following title '{surveyName}' could be found. "
)

DATABASE_COMMIT_FAILED = (
    "A database transaction failed with the following error {e}. "
)

NO_EVALESE_FOUND = (
    "No evalese could be found for the following survey '{surveyName}'"
)