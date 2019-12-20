from flask import request
from flask_restful import Resource, reqparse
from src.utils.errors.messages import API_PARAMETER_MUST_BE_PROVIDED, PAYLOAD_MUST_BE_SENT
from src.api.utils.errors.error_types import API_PARAMETER_MISSING, PAYLOAD_MISSING_OR_EMPTY, NO_RESOURCE_FOUND, INTERNAL_ERROR
from src.api.utils.error_response import error_response

from src.database.crud.response_crud import SurveyResponseCRUD
from src.utils.errors.custom_errors import ClientError
from src.utils.errors.custom_errors import InternalError

import json

from json.decoder import JSONDecodeError


arg_parser = reqparse.RequestParser()
arg_parser.add_argument("uuid", type=str, help = "argument uuid must be a string")
arg_parser.add_argument("surveyName", type=str, help="argument surveyName must be a string")
arg_parser.add_argument("all", type=bool, help="argument all must be a boolean")


def surveyResponse_response(response, surveyName):
    if isinstance(response, list):
        response_array = []
        for res in response:
            response_dict = dict(res.response)
            response_dict["uuid"] = res.uuid
            response_dict["createdOn"] = res.createdOn.isoformat()
            response_dict["surveyName"] = surveyName
            response_array.append(response_dict)
        
        return response_array
    
    response_dict = dict(response.response)
    response_dict["uuid"] = response.uuid
    response_dict["createdOn"] = response.createdOn.isoformat()
    response_dict["surveyName"] = surveyName
    return response_dict
    
class SurveyResponseResource(Resource):

    def get(self, surveyName = None):

        args = arg_parser.parse_args()
        get_arg_uuid = args.get("uuid")
        get_arg_surveyName = args.get("surveyName")
        get_arg_all = args.get("all")

        if surveyName is None:
            if get_arg_surveyName is None:
                return error_response(
                    API_PARAMETER_MISSING,
                    (
                        API_PARAMETER_MUST_BE_PROVIDED.format(
                            resource = "Evalese",
                            parameter = "surveyName"
                        ) +  "This must be supplied as part of the route /responses/<surveyName:str> or as a get parameter"
                    )), 400 
            
            surveyName = get_arg_surveyName
        
        if get_arg_uuid is not None:
            pass
        
        
        try:
            responses = SurveyResponseCRUD().read_responses_for_most_recent_evalese( # pylint: disable=no-value-for-parameter
                surveyName = surveyName,
                all=get_arg_all
            )
            return surveyResponse_response(responses, surveyName), 200
        except ClientError as e:
            return error_response(
                NO_RESOURCE_FOUND,
                str(e)
            ), 404
        except Exception as e:
            return error_response(
                INTERNAL_ERROR, 
                str(e)
            ), 500
    
    def post(self, surveyName = None):
        payload = request.get_json()

        if payload is None or not bool(payload):
            return error_response(
                PAYLOAD_MISSING_OR_EMPTY,
                PAYLOAD_MUST_BE_SENT.format(
                    resource = "SurveyResponse"
                )
            ), 400 
        
        if surveyName is not None:
            payload["meta_evalhalla_sur"] = surveyName
            payload["surveyName"] = surveyName
        else:
            surveyName_key_value = payload.get("surveyName")
            meta_evalhalla_sur_key_value = payload.get("meta_evalhalla_sur")

            if (surveyName_key_value is None or surveyName_key_value == "") and (meta_evalhalla_sur_key_value is None or meta_evalhalla_sur_key_value == "" ):
                return error_response(
                    API_PARAMETER_MISSING,
                    API_PARAMETER_MUST_BE_PROVIDED.format(
                        resource = "SurveyResponse",
                        parameter = "surveyName or meta_evalhalla_sur"
                    ) + "This must be specified as part of the route " +
                    "/responses/<surveyName:str> or in the payload of the request" 
                ), 400
            elif surveyName_key_value is not None and surveyName_key_value != "":
                payload["meta_evalhalla_sur"] = surveyName_key_value
            elif meta_evalhalla_sur_key_value is not None and meta_evalhalla_sur_key_value != "":
                payload["surveyName"] = meta_evalhalla_sur_key_value

        
        survey_surveyName = payload.get("surveyName")

        try:
            response = SurveyResponseCRUD().create_response_for_most_recent_evalese(surveyName= survey_surveyName, response=payload) # pylint: disable=no-value-for-parameter
            return surveyResponse_response(response, survey_surveyName), 200
        except Exception as e:
            return error_response(
                INTERNAL_ERROR,
                str(e)
            ), 500
            

            

        



