from .BaseModel import Base
from sqlalchemy import Integer, ForeignKey, Column, DateTime, Boolean, text
from .utils import utcnow
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.sql import expression


class SurveyResponseModel(Base):
    __tablename__ = "survey_responses"
    id = Column("id", Integer, primary_key=True)
    response = Column("response", JSONB, nullable = False)
    createdOn = Column("created_on", DateTime, server_default=utcnow(), nullable = False)
    uuid = Column("uuid", UUID, unique = True, server_default=text("uuid_generate_v4()"))
    processed = Column("processed", Boolean, server_default="false" , nullable = False)
    evaleseId = Column("evalese_id_fk", Integer, ForeignKey(
        "evalese.id", 
        ondelete="CASCADE",
        onupdate="CASCADE"
        ),
        nullable = False
    )