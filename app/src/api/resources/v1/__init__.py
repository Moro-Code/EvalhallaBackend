from src.api.utils.blueprint_wrapper import api_blueprint_wrapper
from .EvaleseResource import EvaleseResource


@api_blueprint_wrapper
def routes_creator(api):
    api.add_resource(
        EvaleseResource,
        "/evalese",
        "/evalese/<string:surveyName>",
        endpoint = "evalese"
    )