

CONFIG_VAR_DOES_NOT_EXIST = (
      "{config_var} is a required configuration variable. " +
      "both the config value and its environment variable EVALHALLA_{config_var} is None. "
)
CONFIG_IS_WRONG_TYPE = (
    "The config variable {config_var} is of incorrect type, expected {config_var_type}. " +
    "instead recieved {config_incorrect_type}. "
)

ARGUMENT_MUST_BE_PROVIDED = (
    "The argument '{argument}' must be provided. "
)


ARGUMENT_IS_INCORRECT_TYPE = (
    "The argument '{argument}' is of incorrect type {incorrect_type}. Argument should be of type {expected_type}. "
)


API_PARAMETER_MUST_BE_PROVIDED = (
    "In order to access the resource {resource}, the parameter {parameter} must be provided. "
)

PAYLOAD_MUST_BE_SENT = (
    "The following resource {resource} requires a payload in body of the request"
)

MISSING_PARAMETER_FOR_DATA_OPERATION = (
    "The following  parameter(s) are required for a {operation} " +
    "on the table {table}: {parameters} . "
)

NO_SURVEY_FOUND = (
    "No survey with the following title '{title}' could be found. "
)

DATABASE_COMMIT_FAILED = (
    "A database transaction failed with the following error {e}. "
)