"""
crud function for surveys
"""
from src.utils.errors.messages import NO_SURVEY_FOUND, DATABASE_COMMIT_FAILED
from src.utils.errors.custom_errors import NoResultsFoundInDatabase, DatabaseCommitFailed
from src.database.models.SurveyModel import SurveyModel
from src.database.db import get_db
from .utils.decorators import requires_params
from .utils.operations import READ, UPDATE, DELETE, CREATE






class SurveyCRUD:
    def __init__(self, **kwargs):
        self.surveyName = kwargs.get("surveyName")
        self.session = get_db()

    @requires_params(READ, SurveyModel.__tablename__, "surveyName")
    def read_survey_by_surveyName(self,session, **kwargs):
        # pylint: disable=no-self-argument
        # pylint: disable=no-member
        surveyName = kwargs.get("surveyName")
        survey = session.query(SurveyModel).filter_by(
            surveyName = surveyName
        ).one_or_none()

        if survey is None:
            raise NoResultsFoundInDatabase(
                NO_SURVEY_FOUND.format(
                    surveyName = surveyName
                )
            )
        return survey
        
    @requires_params(CREATE, SurveyModel.__tablename__, "surveyName")
    def create_survey(self, session, **kwargs):
        # pylint: disable=no-self-argument
        # pylint: disable=no-member
        surveyName = kwargs.get("surveyName")
        new_survey = SurveyModel(
            surveyName=surveyName
        )
        session.add(new_survey)
        try:
            session.commit()
        except Exception as e:
            session.rollback()
            raise DatabaseCommitFailed(
                DATABASE_COMMIT_FAILED.format(
                    e = repr(e)
                )
            )
        return new_survey
    
    @requires_params(DELETE, SurveyModel.__tablename__, "surveyName")
    def delete_survey(self, session, **kwargs):
        # pylint: disable=no-self-argument
        # pylint: disable=no-member
        surveyName = kwargs.get("surveyName")
        session.query(SurveyModel).filter_by(surveyName=surveyName).delete()
        try:
            session.commit()
        except Exception as e:
            session.rollback()
            raise DatabaseCommitFailed(
                DATABASE_COMMIT_FAILED.format(
                    e = repr(e)
                )
            )
        return surveyName
    



        
        
        
