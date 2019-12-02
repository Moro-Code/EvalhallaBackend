"""
Resource used to get and create evalese
"""


from flask_restful import Resource, reqparse
from src.utils.errors.messages import API_PARAMETER_MUST_BE_PROVIDED
from src.api.utils.errors.error_types import API_PARAMETER_MISSING


arg_parser = reqparse.RequestParser()
arg_parser.add_argument("versionNumber", type=int, help="argument versionNumber must be an interger greater than 0")
arg_parser.add_argument("title", type=str, help="argument title must be a string")
arg_parser.add_argument("index", type=int, help="argument index must be an interger greater than 0")
arg_parser.add_argument("numberOfItems", type=int, help="argument numberOfItems must be an integer greater that 0", default=20)



class EvaleseResource(Resource):
    def get(self, title = None):
        # parse the get arguments 
        args = arg_parser.parse_args()

        # get the evalese versionNumber from the parsed arguments 
        get_arg_version_number = args.get("versionNumber")
        get_arg_index = args.get("index")
        get_arg_numberOfItems = args.get("numberOfItems")
        get_arg_title = args.get("title")

        if title is None:
            if get_arg_title is None:
                return {
                    "error": API_PARAMETER_MISSING,
                    "message": (
                        API_PARAMETER_MUST_BE_PROVIDED.format(
                            resource = "Evalese",
                            parameter = "title"
                        ) +  "This must be supplied as part of the route /evalese/<title:str> or as a get parameter"
                    )

                }, 400 
            
            title =  get_arg_title

        if get_arg_index is not None:

            index = get_arg_index
            offset = get_arg_numberOfItems

            # implement pagination request
            # dummy return for now
            return {}, 200
        
        else:

            # implement getting the most recent evalese
            # dummy return for now 
            return {}, 200
        



        
        

