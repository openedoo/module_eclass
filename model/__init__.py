from openedoo_project import json
from openedoo_project.db.raw import query
from ..database import EclassSchema
from ..error_handler import simple_error_message

SUCCESS_MESSAGE = {'message': 'success'}


def sql_column_builder(data=None):
    """SQL column builder.

    A helper for building column list in SQL syntax from python dict.
    Example:

        data = {'id': 1, 'name': 'example'}

        become:

        id='1', name='example'

    Then it can be used with existing SQL syntax by joining them.
    Example:

        sql = 'INSERT INTO table SET {}'.format(sql_column_builder(data))

    """

    column = ', '.join("{key}='{value}'"
                       .format(key=key, value=value)
                       for key, value in data.iteritems())
    return column


class Eclass(object):
    def __init__(self):
        self.__tablename__ = EclassSchema.__tablename__

    def insert(self, data=None):
        """Insert a record"""

        try:
            sql = "INSERT INTO {} SET id=DEFAULT, {}"
            sql = sql.format(self.__tablename__, sql_column_builder(data))
            query(sql)

            return SUCCESS_MESSAGE

        except Exception as e:
            return simple_error_message(str(e))

    def get_all(self):
        """Get all records"""

        try:
            result = query('SELECT * FROM {}'.format(self.__tablename__))
            return result

        except Exception as e:
            return simple_error_message(str(e))

    def get(self, eclass_id=None):
        """Get record by id"""

        try:
            sql = 'SELECT * FROM {} WHERE id={}'
            sql = sql.format(self.__tablename__, eclass_id)
            result = query(sql)
            return result

        except Exception as e:
            return simple_error_message(str(e))

    def update(self, data=None):
        """Update a record by id"""

        try:
            column_data = {key: value for key, value in data.iteritems()
                           if key not in ('id')}
            column = sql_column_builder(column_data)
            sql = 'UPDATE {} SET {} WHERE id={}'
            sql = sql.format(self.__tablename__, column, data['id'])
            # The query execution doesn't return any value
            query(sql)
            return SUCCESS_MESSAGE

        except Exception as e:
            return simple_error_message(str(e))

    def delete(self, eclass_id=None):
        """Delete a record by id"""

        try:
            sql = 'DELETE FROM {} WHERE id={}'
            sql = sql.format(self.__tablename__, eclass_id)
            res = query(sql)

            return SUCCESS_MESSAGE

        except Exception as e:
            return simple_error_message(str(e))

    def add_member(self, data=None):
        """Add member"""

        try:
            members = self.get_members(data['id'])
            member_list = members.split(',')

            if data['user_id'] not in member_list:
                member_list.append(data['user_id'])
                members = ','.join(member_list)
                update_data = {
                    'member': members,
                    'id': data['id']
                }
                update_member = self.update(update_data)

            return SUCCESS_MESSAGE

        except Exception as e:
            return simple_error_message(str(e))

    def get_member(self, eclass_id=None, member_id=None):
        """Get an eclass member"""

        try:
            members = self.get_members(eclass_id)
            member_list = members.split(',')

            result = {'member': False}
            if member_id in member_list:
                result = {
                    'member': True,
                    'user_id': member_id
                }

            return result

        except Exception as e:
            return simple_error_message(str(e))

    def delete_member(self, eclass_id, member_id):
        """Delete a member in an eclass"""

        try:
            members = self.get_members(eclass_id)
            member_list = members.split(',')

            if member_id in member_list:
                member_list.remove(member_id)
                members = ','.join(member_list)
                data = {
                    'member': members,
                    'id': eclass_id
                }
                update = self.update(data)

            return {'member': False}

        except Exception as e:
            return simple_error_message(str(e))

    def get_members(self, eclass_id=None):
        """Get eclass members"""

        try:
            get_eclass = self.get(eclass_id)
            parse = json.loads(get_eclass)
            members = parse[0]['member']
            return members

        except Exception as e:
            return simple_error_message(str(e))
