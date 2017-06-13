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

    def get(self, eclass_id=None, pagination=None):
        try:
            db = DBQuery()
            where = {'class_id': eclass_id}
            result = db.select(table=self.member_table,
                               where_clause=where,
                               pagination=pagination)
            return result

        except Exception as e:
            raise

    def delete(self, class_id=None, user_id=None):
        try:
            db = DBQuery()
            where = {'class_id': class_id, 'user_id': user_id}
            result = db.delete(table=self.member_table, where_clause=where)
            return SUCCESS_MESSAGE

        except Exception as e:
            print e
            raise
