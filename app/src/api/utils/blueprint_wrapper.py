from flask import Blueprint
from flask_restful import Api
from src.utils.errors.messages import ARGUMENT_MUST_BE_PROVIDED, ARGUMENT_IS_INCORRECT_TYPE

def api_blueprint_wrapper(api_routes_creator_func):
    """
    Blueprint wrapper for api routes to avoid having to duplicate boilerplate 
    """
    def bp_wrapper_inner(app, current_version = False, version = None):
        if current_version:
            bp = Blueprint("current", import_name = __name__ )
            api = Api(bp)
        else:
            # version must be defined and of type string
            if version is None:
                raise ValueError(
                    ARGUMENT_MUST_BE_PROVIDED.format(
                        argument = "version"
                    ) + "for API versions that are not the current version."
                )
            elif not isinstance(version, str):
                raise TypeError(
                    ARGUMENT_IS_INCORRECT_TYPE.format(
                        argument = "version",
                        incorrect_type = type(version).__name__,
                        expected_type = "string"
                    )
                )
            # create a blueprint with the name of the version 
            bp = Blueprint(version, import_name = __name__)
            api = Api(bp, prefix="/" + version)
        
        api_routes_creator_func(api)
        app.register_blueprint(bp)
    
    return bp_wrapper_inner
    

