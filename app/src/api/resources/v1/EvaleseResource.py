"""
Resource used to get and create evalese
"""

from flask import request 
from flask_restful import Resource, reqparse
from src.utils.errors.messages import API_PARAMETER_MUST_BE_PROVIDED, PAYLOAD_MUST_BE_SENT, API_CONSTRAINT_VIOLATED
from src.api.utils import error_response
from src.api.utils.errors.error_types import API_PARAMETER_MISSING, API_PARAMETER_INCORRECT, PAYLOAD_MISSING_OR_EMPTY, NO_RESOURCE_FOUND, INTERNAL_ERROR
from src.database.crud.evalese_crud import EvaleseCRUD
from src.utils.errors.custom_errors import ClientError, InternalError



arg_parser = reqparse.RequestParser()
arg_parser.add_argument("uuid", type=str, help="argument uuid must be a string")
arg_parser.add_argument("surveyName", type=str, help="argument surveyName must be a string")
arg_parser.add_argument("pageNumber", type=int, help="argument pageNumber must be an interger greater than 0")
arg_parser.add_argument("numberOfItems", type=int, help="argument numberOfItems must be an integer greater that 0 and less or equal to 100", default=20)



def evalese_response(evalese, surveyName):
    def prepare_json(evalese):
        return {
            "surveyName": surveyName,
            "evalese": evalese.evalese,
            "createdOn": evalese.createdOn.isoformat(),
            "uuid": evalese.uuid
        }
    if isinstance(evalese, list):
        evalese_array = []
        for version in evalese:
            evalese_array.append(prepare_json(version))
        return evalese_array
    
    return prepare_json(evalese)



class EvaleseResource(Resource):
    def get(self, surveyName = None):
        # pylint: disable=no-value-for-parameter

        # parse the get arguments 
        args = arg_parser.parse_args() 
        get_arg_uuid = args.get("uuid")
        get_arg_pageNumber = args.get("pageNumber")
        get_arg_numberOfItems = args.get("numberOfItems")
        get_arg_surveyName = args.get("surveyName")

        if surveyName is None:
            if get_arg_surveyName is None:
                
                return error_response(
                    API_PARAMETER_MISSING,
                    API_PARAMETER_MUST_BE_PROVIDED.format(
                            resource = "Evalese",
                            parameter = "surveyName"
                        ) +  "This must be supplied as part of the route /evalese/<surveyName:str> or as a get parameter"
                ), 400 
            
            surveyName =  get_arg_surveyName

        if get_arg_uuid is not None:

            try:
                evalese = EvaleseCRUD().read_evalese_by_uuid(surveyName = surveyName, uuid = get_arg_uuid)
                return evalese_response(evalese, surveyName), 200
            except ClientError as e:
                return error_response(
                    NO_RESOURCE_FOUND,
                    str(e)
                ), 404
            except Exception as e:
                return  error_response(
                  INTERNAL_ERROR,
                  str(e)
                ), 500
        
        if get_arg_pageNumber is not None:
            if get_arg_pageNumber < 1:
                return error_response(
                    API_PARAMETER_INCORRECT,
                    API_CONSTRAINT_VIOLATED.format(
                        parameter = "pageNumber",
                        resource = "evalese",
                        constraint = "pageNumber must be an Interger with a value above 1"
                    )
                ), 400
            elif get_arg_numberOfItems <= 0:
                return error_response(
                    API_PARAMETER_INCORRECT,
                    API_CONSTRAINT_VIOLATED.format(
                        parameter = "numberOfItems",
                        resource = "evalese",
                        constraint = "numberOfItems must be an Integer with a value above 1"
                    )
                ), 400
            
            try:
                evalese = EvaleseCRUD().read_evalese(
                    surveyName= surveyName, 
                    pageNumber=get_arg_pageNumber,
                    numberOfItems=get_arg_numberOfItems
                )
                return evalese_response(evalese, surveyName), 200
            except Exception as e:
                return error_response(
                    INTERNAL_ERROR,
                    str(e)
                ), 500

        try:
            evalese = EvaleseCRUD().read_most_recent_evalese(surveyName = surveyName) 
            return evalese_response(evalese, surveyName), 200
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
                    resource = "Evalese"
                )
            ), 400
        
        # if surveyName is provided in route it only makes sense to be the surveyName in the data
        if surveyName is not None:
            payload["surveyName"] = surveyName
        
        survey_surveyName = payload.get("surveyName")
        survey_evalese = payload.get("evalese")

        if survey_surveyName is None:
            return error_response(
                API_PARAMETER_MISSING,
                API_PARAMETER_MUST_BE_PROVIDED.format(
                    resource = "Evalese",
                    parameter = "surveyName"
                ) + "This must be supplied as part of the route " + 
                "/evalese/<surveyName:str> or in the payload of the request"
            ), 400
        elif survey_evalese is None:
            return error_response(
                API_PARAMETER_MISSING,
                API_PARAMETER_MUST_BE_PROVIDED.format(
                    resource = "Evalese",
                    parameter = "evalese"
                ) + "This must be supplied as part of the route " + 
                "/evalese/<surveyName:str> or in the payload of the request"
            ), 400

        try:
            evalese = EvaleseCRUD().create_evalese(surveyName = survey_surveyName, evalese = survey_evalese ) # pylint: disable=no-value-for-parameter
            return evalese_response(evalese, survey_surveyName), 200
        except Exception as e:
            return error_response(
                INTERNAL_ERROR,
                str(e)
            ), 500






        
        

