from .BaseModel import Base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from .utils import utcnow

class SurveyModel(Base):
    __tablename__ = "surveys"
    id = Column("id", Integer, primary_key = True)
    surveyName = Column("survey_name", String(length=20), nullable=False, unique= True)
    createdOn = Column("created_on", DateTime, server_default=utcnow())
    # get evalese children by order of when they were created
    previousEvalese = relationship(
        "EvaleseModel", 
        order_by="EvaleseModel.createdOn",
        cascade="all, delete-orphan",
        passive_deletes=True
    )

