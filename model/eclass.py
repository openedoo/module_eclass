import json
import datetime
from openedoo_project.db.raw import query
from ..database import EclassSchema, EclassPostsSchema
from ..libs.error_handler import InvalidUsage, simple_error_message
from ..libs.sql_helper import DBQuery, sql_column_builder
from ..libs.security import sanitize

SUCCESS_MESSAGE = {'message': 'success'}


class Eclass(object):
    def __init__(self):
        self.__tablename__ = EclassSchema.__tablename__

    def add(self, data=None):
        try:
            db_query = DBQuery()

            eclass_data = {
                'name': data['name'],
                'course': data['course'],
                'university': data['university'],
                'privilege': data['privilege']
            }
            eclass = db_query.insert(table='eclass', col=eclass_data)

            member_data = {
                'user_id': data['user_id'],
                'class_id': eclass.lastrowid,
                'is_creator': 1
            }
            member = db_query.insert(table='eclass_member', col=member_data)

            data = dict(eclass_data.items() + member_data.items() +
                        SUCCESS_MESSAGE.items())

            data['links'] = {
                'self': '/eclass/{}'.format(member_data['class_id']),
            }
            return data

        except KeyError:
            raise InvalidUsage('Missing request parameter.', '',
                               status_code=400)

    def get_all(self, pagination=None):
        """Get all eclass"""

        try:
            db_query = DBQuery()
            result = db_query.select(table='eclass', pagination=pagination)
            return result

        except Exception as e:
            raise InvalidUsage('Something bad happened in the server.', str(e),
                               status_code=500)

    def get(self, eclass_id=None):
        """Get eclass by id"""

        try:
            where_clause = {'id': eclass_id}
            db_query = DBQuery()
            result = db_query.select(table='eclass',
                                     where_clause=where_clause)
            return result

        except Exception as e:
            raise InvalidUsage('Something bad happened in the server.', str(e),
                               status_code=500)

    def get_by_creator(self, creator_id=None):
        """Get eclass by creator_id"""

        try:
            sql = """SELECT eclass.* FROM eclass
                     INNER JOIN eclass_member
                     ON eclass.id = eclass_member.class_id
                     AND eclass_member.user_id = {creator_id}
                     AND eclass_member.is_creator = 1"""
            sql = sql.format(creator_id=creator_id)
            result = query(sql)
            return result

        except Exception as e:
            raise InvalidUsage('Something bad happened in the server.', str(e),
                               status_code=500)

    def update(self, data=None):
        """Update eclass by id"""

        try:
            column_data = {key: value for key, value in data.iteritems()
                           if key not in ('id')}

            db_query = DBQuery()
            result = db_query.update('eclass', column_data, {'id': data['id']})
            return SUCCESS_MESSAGE

        except KeyError:
            raise InvalidUsage('Missing request parameter.', '',
                               status_code=400)

    def delete(self, eclass_id=None):
        """Delete a record by id"""

        try:
            sql = 'DELETE FROM {} WHERE id={}'
            sql = sql.format(self.__tablename__, eclass_id)
            res = query(sql)

            return SUCCESS_MESSAGE

        except Exception as e:
            return simple_error_message(str(e))

    def add_discussion(self, eclass_id=None, data=None):
        """Add discussion"""

        try:
            get_admins = self.get_admins(eclass_id)
            if data['user_id'] not in get_admins:
                raise ValueError('The user is not permitted to post any '
                                 'discussion here')


            current_time = str(datetime.datetime.now())
            data['created'] = current_time
            data['edited'] = current_time
            data['class_id'] = eclass_id
            data['description'] = sanitize(data['description'])
            del data['user_id']
            table_name = EclassPostsSchema.__tablename__
            db_query = DBQuery()
            result = db_query.insert(table_name, data)
            return SUCCESS_MESSAGE

        except Exception as e:
            return simple_error_message(str(e))

    def get_discussion(self, eclass_id=None):
        try:
            db_query = DBQuery()
            table_name = EclassPostsSchema.__tablename__
            result = db_query.select(table=table_name)
            return result

        except Exception as e:
            return simple_error_message(str(e))
