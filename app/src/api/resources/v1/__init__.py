from src.api.utils.blueprint_wrapper import api_blueprint_wrapper
from .EvaleseResource import EvaleseResource
from .ResponsesResource import SurveyResponseResource
from .SurveyResource import SurveyResource


@api_blueprint_wrapper
def routes_creator(api):
    api.add_resource(
        EvaleseResource,
        "/evalese",
        "/evalese/<string:surveyName>",
        endpoint = "evalese"
    )
    api.add_resource(
        SurveyResponseResource, 
        "/responses",
        "/responses/<string:surveyName>",
        endpoint = "responses"
    )

    api.add_resource(
        SurveyResource,
        "/",
        "/<string:surveyName>",
        endpoint = "surveys"
    )