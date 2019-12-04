"""
Resource used to get and create evalese
"""

from flask import request 
from flask_restful import Resource, reqparse
from src.utils.errors.messages import API_PARAMETER_MUST_BE_PROVIDED, PAYLOAD_MUST_BE_SENT
from src.api.utils.errors.error_types import API_PARAMETER_MISSING, PAYLOAD_MISSING_OR_EMPTY, NO_RESOURCE_FOUND, INTERNAL_ERROR
from src.database.crud.evalese_crud import EvaleseCRUD
from src.utils.errors.custom_errors import ClientError
from src.utils.errors.custom_errors import InternalError


arg_parser = reqparse.RequestParser()
arg_parser.add_argument("versionNumber", type=int, help="argument versionNumber must be an interger greater than 0")
arg_parser.add_argument("surveyName", type=str, help="argument surveyName must be a string")
arg_parser.add_argument("index", type=int, help="argument index must be an interger greater than 0")
arg_parser.add_argument("offset", type=int, help="argument numberOfItems must be an integer greater that 0", default=20)



class EvaleseResource(Resource):
    def get(self, surveyName = None):
        # parse the get arguments 
        args = arg_parser.parse_args()

        # get the evalese versionNumber from the parsed arguments 
        get_arg_version_number = args.get("versionNumber")
        get_arg_index = args.get("index")
        get_arg_offset = args.get("offset")
        get_arg_surveyName = args.get("surveyName")

        if surveyName is None:
            if get_arg_surveyName is None:
                return {
                    "error": API_PARAMETER_MISSING,
                    "message": (
                        API_PARAMETER_MUST_BE_PROVIDED.format(
                            resource = "Evalese",
                            parameter = "surveyName"
                        ) +  "This must be supplied as part of the route /evalese/<surveyName:str> or as a get parameter"
                    )

                }, 400 
            
            surveyName =  get_arg_surveyName

        if get_arg_index is not None:

            index = get_arg_index
            offset = get_arg_offset

            # implement pagination request
            # dummy return for now
            return {}, 200
        
        else:

            # implement getting the most recent evalese
            # dummy return for now

            try:
                evalese = EvaleseCRUD().read_most_recent_evalese_by_surveyName(surveyName = get_arg_surveyName) # pylint: disable=no-value-for-parameter
                return {
                    "surveyName": surveyName,
                    "evalese": evalese.evalese,
                    "createdOn": evalese.createdOn.isoformat(),
                    "uuid": evalese.uuid
                }, 200
            except ClientError as e:
                return {
                    "error": NO_RESOURCE_FOUND,
                    "message": str(e)
                }, 404
            except Exception as e:
                return {
                    "error": INTERNAL_ERROR,
                    "message": str(e)
                }, 500 

            return {}, 200
    
    def post(self, surveyName = None):

        payload = request.get_json()

        if payload is None or not bool(payload):
            return {
                "error": PAYLOAD_MISSING_OR_EMPTY,
                "message": PAYLOAD_MUST_BE_SENT.format(
                    resource = "Evalese"
                )
            }, 400
        
        # if surveyName is provided in route it only makes sense to be the surveyName in the data
        if surveyName is not None:
            payload["surveyName"] = surveyName
        
        survey_surveyName = payload.get("surveyName")
        survey_evalese = payload.get("evalese")

        if survey_surveyName is None:
            return {
                "error": API_PARAMETER_MISSING,
                "message": API_PARAMETER_MUST_BE_PROVIDED.format(
                    resource = "Evalese",
                    parameter = "surveyName"
                ) + "This must be supplied as part of the route " + 
                "/evalese/<surveyName:str> or in the payload of the request"
            }, 400
        elif survey_evalese is None:
            return {
                "error": API_PARAMETER_MISSING,
                "message": API_PARAMETER_MUST_BE_PROVIDED.format(
                    resource = "Evalese",
                    parameter = "evalese"
                ) + "This must be supplied as part of the route " + 
                "/evalese/<surveyName:str> or in the payload of the request"
            }, 400

        try:
            evalese = EvaleseCRUD().create_evalese(surveyName = survey_surveyName, evalese = survey_evalese ) # pylint: disable=no-value-for-parameter
            return {
                    "surveyName": survey_surveyName,
                    "evalese": evalese.evalese,
                    "createdOn": evalese.createdOn.isoformat(),
                    "uuid": evalese.uuid
                }, 200
        except Exception as e:
            return {
                "error": INTERNAL_ERROR,
                "message": str(e)
            }, 500






        
        

