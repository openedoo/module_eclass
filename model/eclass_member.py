from ..database import EclassSchema, EclassMemberSchema
from ..libs.sql_helper import DBQuery, sql_column_builder
from .eclass import SUCCESS_MESSAGE


class EclassMember(object):
    def __init__(self):
        self.eclass_table = EclassSchema.__tablename__
        self.member_table = EclassMemberSchema.__tablename__

    def add(self, data=None):
        try:
            db = DBQuery()
            result = db.insert(self.member_table, data)

            return SUCCESS_MESSAGE

        except Exception as e:
            raise
