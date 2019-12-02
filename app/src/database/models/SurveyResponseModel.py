from .BaseModel import Base
from sqlalchemy import Integer, ForeignKey, Column, DateTime, Boolean
from .utils import utcnow
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.sql import expression


class SurveyResponseModel(Base):
    __tablename__ = "survey_responses"
    id = Column("id", Integer, primary_key=True)
    response = Column("response", JSONB, nullable = False)
    createdOn = Column("createdOn", DateTime, server_default=utcnow(), nullable = False)
    boolean = Column("processed", Boolean, server_default=expression.true() , nullable = False)
    evaleseId = Column("evalese_id_fk", Integer, ForeignKey(
        "evalese.id", 
        ondelete="CASCADE",
        onupdate="CASCADE"
        ),
        nullable = False
    )