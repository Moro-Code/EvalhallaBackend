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
    def read_most_recent_evalese_by_surveyName(self, session, **kwargs):
        # pylint: disable=no-self-argument
        # pylint: disable=no-member
        survey = self.surveyCRUD.read_survey(**kwargs) # pylint: disable=undefined-variable 
        evalese_query = survey.evalese
        evalese = evalese_query.first()
        if evalese is None:
            raise NoResultsFoundInDatabase(
                NO_EVALESE_FOUND.format(
                    surveyName = survey.surveyName
                )
            )
        return evalese
    
    @requires_params(CREATE, EvaleseModel.__tablename__, "evalese")
    def create_evalese(self, session, **kwargs):
        # pylint: disable=no-self-argument
        # pylint: disable=no-member
        evalese = kwargs.get("evalese")
        try:
            survey = self.surveyCRUD.read_survey(**kwargs) # pylint: disable=undefined-variable
        except NoResultsFoundInDatabase:
            survey = self.surveyCRUD.create_survey(**kwargs) # pylint: disable=undefined-variable
    
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





