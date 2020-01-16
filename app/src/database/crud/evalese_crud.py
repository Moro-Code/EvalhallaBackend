from src.utils.errors.messages import DATABASE_COMMIT_FAILED, NO_EVALESE_FOUND
from src.utils.errors.custom_errors import NoResultsFoundInDatabase, DatabaseCommitFailed
from src.database.models.SurveyModel import SurveyModel
from src.database.models.EvaleseModel import EvaleseModel
from .utils.decorators import requires_params
from .utils.operations import READ, UPDATE, DELETE, CREATE
import src.database.crud.survey_crud as sv


class EvaleseCRUD:
    def __init__(self, surveyCRUD= None, **kwargs):
        if surveyCRUD is None:
            self.surveyCRUD = sv.SurveyCRUD(**kwargs)
        else:
            self.surveyCRUD = surveyCRUD

        self.evalese = kwargs.get("evalese")
    
    @requires_params(READ, EvaleseModel.__tablename__)
    def read_most_recent_evalese(self, session, **kwargs):
        survey = self.surveyCRUD.read_survey_by_surveyName(**kwargs) 
        evalese_query = survey.evalese
        evalese = evalese_query.first()
        if evalese is None:
            raise NoResultsFoundInDatabase(
                NO_EVALESE_FOUND.format(
                    surveyName = survey.surveyName
                )
            )
        return evalese
    @requires_params(READ, EvaleseModel.__tablename__)
    def read_evalese(self, session, **kwargs):
        pageNumber = kwargs.pop("pageNumber", None) or 1
        numberOfItems = kwargs.pop("numberOfItems", None) or 20
        all_evalese = kwargs.pop("all", False)
        
        survey = self.surveyCRUD.read_survey_by_surveyName(**kwargs)
        
        if all_evalese is True:
            return survey.evalese.all()
        
        return survey.evalese.limit(numberOfItems).offset( (pageNumber - 1) * numberOfItems).all()
    
        
    @requires_params(READ, EvaleseModel.__tablename__, "uuid")
    def read_evalese_by_uuid(self, session, **kwargs):
        uuid = kwargs.get("uuid")
        survey = self.surveyCRUD.read_survey_by_surveyName(**kwargs)
        evalese_query = survey.evalese
        evalese = evalese_query.filter_by(
            uuid = uuid
        ).one_or_none()

        if evalese is None:
            raise NoResultsFoundInDatabase(
                NO_EVALESE_FOUND.format(
                    surveyName = survey.surveyName
                ) + f" and with the following uuid {uuid}"
            )
        return evalese

    
    @requires_params(CREATE, EvaleseModel.__tablename__, "evalese")
    def create_evalese(self, session, **kwargs):
        evalese = kwargs.get("evalese")
        try:
            survey = self.surveyCRUD.read_survey_by_surveyName(**kwargs) 
        except NoResultsFoundInDatabase:
            survey = self.surveyCRUD.create_survey(**kwargs) 
    
        new_evalese = EvaleseModel(evalese=evalese)
        survey.evalese.append(new_evalese)

        try:
            session.commit()
        except Exception as e:
            session.rollback()
            raise DatabaseCommitFailed(
                DATABASE_COMMIT_FAILED.format(
                    e = repr(e)
                )
            )
        
        return new_evalese





