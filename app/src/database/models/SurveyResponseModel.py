from .BaseModel import Base
from sqlalchemy import Integer, ForeignKey, Column, DateTime
from .utils import utcnow
from sqlalchemy.dialects.postgresql import JSONB


class SurveyResponseModel(Base):
    __tablename__ = "survey_responses"
    id = Column("id", Integer, primary_key=True)
    response = Column("response", JSONB, nullable = False)
    createdOn = Column("createdOn", DateTime, server_default=utcnow())
    evaleseId = Column("evalese_id_fk", Integer, ForeignKey(
        "evalese.id", 
        ondelete="CASCADE",
        onupdate="CASCADE"
        ),
        nullable = False
    )