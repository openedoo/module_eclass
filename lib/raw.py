import decimal
import datetime
import json
from sqlalchemy import create_engine


# table declaration
from openedoo_project import config

engine = create_engine(config.SQLALCHEMY_DATABASE_URI)


def alchemyencoder(obj):
    """JSON encoder function for SQLAlchemy special classes."""
    if isinstance(obj, datetime.datetime):
        return obj.isoformat()
    elif isinstance(obj, decimal.Decimal):
        return float(obj)


def query(query):
    """output json """
    connection = engine.connect()
    res = connection.execute(query)
    if res.returns_rows:
        # use special handler for dates and decimals
        return json.dumps([dict(r) for r in res],
                          default=alchemyencoder,
                          encoding='latin-1  ')
    return res
