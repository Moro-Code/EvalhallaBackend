from flask import request 
from flask_restful import Resource, reqparse
from src.utils.errors.messages import API_PARAMETER_MUST_BE_PROVIDED, PAYLOAD_MUST_BE_SENT, API_CONSTRAINT_VIOLATED
from src.api.utils import error_response
from src.api.utils.errors.error_types import API_PARAMETER_MISSING, API_PARAMETER_INCORRECT, INTERNAL_ERROR, NO_RESOURCE_FOUND
from src.database.crud.survey_crud import SurveyCRUD
from src.utils.errors.custom_errors import ClientError, InternalError

arg_parser = reqparse.RequestParser()
arg_parser.add_argument("uuid", type=str, help="argument uuid must be a string")
arg_parser.add_argument("surveyName", type=str, help="argument surveyName must be a string")
arg_parser.add_argument("pageNumber", type=int, help="argument pageNumber must be an interger greater than 0")
arg_parser.add_argument("numberOfItems", type=int, help="argument numberOfItems must be an interger greater than 0 and less or equal to 100", default = 20)


def survey_response(survey):
    def prepare_json(survey):
        return {
            "surveyName": survey.surveyName,
            "uuid": survey.uuid,
            "createdOn": survey.createdOn.isoformat()
        }
    if isinstance(survey, list):
        surveys = []
        for srv in survey:
            surveys.append(prepare_json(srv))
        return surveys
    
    return prepare_json(survey)

class SurveyResource(Resource):
    def get(self, surveyName = None):
        # pylint: disable=no-value-for-parameter

        args = arg_parser.parse_args()
        get_arg_uuid = args.get("uuid")
        get_arg_pageNumber = args.get("pageNumber")
        get_arg_numberOfItems = args.get("numberOfItems")
        get_arg_surveyName = args.get("surveyName")

        if surveyName is None:
            if get_arg_surveyName is not None:
                surveyName = get_arg_surveyName
        
        if surveyName is not None:
            try:
                survey = SurveyCRUD().read_survey_by_surveyName(surveyName = surveyName)
                return survey_response(survey), 200
            except ClientError as e:
                return error_response(
                    NO_RESOURCE_FOUND,
                    str(e)
                ), 400
            except Exception as e:
                return error_response(
                    INTERNAL_ERROR,
                    str(e)
                ), 500
        
        if get_arg_uuid is not None:
            # todo, create crud method
            pass


        try:
            surveys = SurveyCRUD().read_surveys(
                pageNumber = get_arg_pageNumber, numberOfItems = get_arg_numberOfItems
            )
            return survey_response(surveys), 200 
        except Exception as e:
            return error_response(
                INTERNAL_ERROR,
                str(e)
            ), 500 