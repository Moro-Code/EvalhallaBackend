from src.database.models.SurveyResponseModel import SurveyResponseModel
from src.utils.errors.custom_errors import NoResultsFoundInDatabase, DatabaseCommitFailed
from src.utils.errors.messages import DATABASE_COMMIT_FAILED
from .utils.decorators import requires_params
from .utils.operations import READ, UPDATE, DELETE, CREATE

import src.database.crud.evalese_crud as ev

class SurveyResponseCRUD:

    def __init__(self, evaleseCRUD = None, **kwargs):
        if evaleseCRUD is None:
            self.evaleseCRUD =  ev.EvaleseCRUD(**kwargs)
        else:
            self.evaleseCRUD = evaleseCRUD

        self.response = kwargs.get("response")
    
    @requires_params(READ, SurveyResponseModel.__tablename__)
    def read_responses_for_most_recent_evalese(self, session, **kwargs):
        allResponses = kwargs.pop("all", None) or False
        evalese = self.evaleseCRUD.read_most_recent_evalese(**kwargs)
        
        if allResponses:
            return evalese.responses.all()

        return evalese.responses.filter_by(
            processed = True 
        ).all()

    @requires_params(CREATE, SurveyResponseModel.__tablename__, "response")
    def create_response_for_most_recent_evalese(self, session, **kwargs):
        response = kwargs.get("response")
        evalese = self.evaleseCRUD.read_most_recent_evalese(**kwargs)

        new_response = SurveyResponseModel(
            response = response
        )

        evalese.responses.append(new_response)

        try:
            session.commit()
        except Exception as e:
            session.rollback()
            raise DatabaseCommitFailed(
                DATABASE_COMMIT_FAILED.format(
                    e = repr(e)
                )
            )
        
        return new_response

    

