# CURRENT_TIMESTAMP for postgresql

from sqlalchemy.sql import expression
from sqlalchemy.ext.compiler import compiles
from sqlalchemy.types import DateTime

class utcnow(expression.FunctionElement):
    type = DateTime()

@compiles(utcnow, "postgresql")
def pg_utcnow(element, compiler, **kwargs):
    return "TIMEZONE('utc', CURRENT_TIMESTAMP)"

