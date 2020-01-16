from src.database.models.SurveyResponseModel import SurveyResponseModel
from src.utils.errors.custom_errors import NoResultsFoundInDatabase, DatabaseCommitFailed
from src.utils.errors.messages import DATABASE_COMMIT_FAILED, NO_SURVEY_RESPONSE_FOUND
from .utils.decorators import requires_params
from .utils.operations import READ, UPDATE, DELETE, CREATE
from src.worker.tasks import calculate_sentiment_for_response
from flask import current_app

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
    @requires_params(READ, SurveyResponseModel.__tablename__, "uuid")
    def read_response_by_uuid(self, session, **kwargs):
        uuid = kwargs.get("uuid")

        response = session.query(SurveyResponseModel).filter_by(
            uuid = uuid
        ).one_or_none()

        if response is None:
            raise NoResultsFoundInDatabase(
                NO_SURVEY_RESPONSE_FOUND.format(
                    uuid = uuid
                )
            )
        return response
    
    @requires_params(READ, SurveyResponseModel.__tablename__)
    def read_all_responses(self, session, **kwargs):

        all_responses = kwargs.pop(
            "all", False
        )
        surveyName = kwargs.pop(
            "surveyName", None
        )
        responses = []

        all_evalese = self.evaleseCRUD.read_evalese(
            surveyName = surveyName, all = True
        )

        for evalese in all_evalese:
            if all_responses is True:
                responses.extend(
                    evalese.responses.all()
                )
            else:
                responses.extend(
                    evalese.responses.filter_by(
                        processed = True
                    ).all()
                )
        
        return responses


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
            if current_app.config.get("USE_SENTIMENT") is True:
                calculate_sentiment_for_response.delay(
                    new_response.uuid
                )
        except Exception as e:
            session.rollback()
            raise DatabaseCommitFailed(
                DATABASE_COMMIT_FAILED.format(
                    e = repr(e)
                )
            )
        
        return new_response

    

