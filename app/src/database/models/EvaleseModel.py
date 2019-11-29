from .BaseModel import Base
from sqlalchemy import Column, Integer, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from .utils import utcnow



class EvaleseModel(Base):
    __tablename__="evalese"
    id = Column("id", Integer, primary_key=True)
    evalese = Column("evalese", Text, nullable=False)
    createdOn = Column("created_on", DateTime, server_default=utcnow())
    surveyId = Column("survey_id_fk", Integer, ForeignKey("surveys.id", onupdate= "CASCADE", ondelete= "CASCADE"), nullable=False)
    responses = relationship(
        "SurveyResponseModel",
        cascade="all, delete-orphan",
        passive_deletes=True,
        order_by= "SurveyResponseModel.createdOn"
    )

