"""
crud function for surveys
"""
from src.utils.errors.messages import MISSING_PARAMETER_TO_READ_DATA
from src.database.models.SurveyModel import SurveyModel





class SurveyCrud:
    def __init__(self, **kwargs):
        self.title = kwargs.get("title")
        self.info_dict = kwargs
    
    def get_survey(self,title=None):
        if self.title is None and title is None:
            raise ValueError(
                MISSING_PARAMETER_TO_READ_DATA.format(
                    parameter = "title",
                    table = SurveyModel.__tablename__
                )
            )
        
