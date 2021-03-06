from .BaseModel import Base
from sqlalchemy import Column, Integer, DateTime, ForeignKey, text, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from .utils import utcnow

class SurveyModel(Base):
    __tablename__ = "surveys"
    id = Column("id", Integer, primary_key = True)
    surveyName = Column("survey_name", Text, nullable=False, unique= True)
    uuid = Column("uuid", UUID, unique = True, server_default=text("uuid_generate_v4()"))
    createdOn = Column("created_on", DateTime, server_default=utcnow())
    # get evalese children by order of when they were created
    evalese = relationship(
        "EvaleseModel", 
        order_by="EvaleseModel.createdOn.desc()",
        cascade="all, delete-orphan",
        passive_deletes=True,
        lazy="dynamic"
    )

