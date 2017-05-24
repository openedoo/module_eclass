import cgi
import os
import tempfile
import datetime
from openedoo_project import json
from openedoo_project.db.raw import query
from ..database import EclassSchema, EclassPostsSchema
from ..error_handler import simple_error_message, InvalidUsage

SUCCESS_MESSAGE = {'message': 'success'}


def sanitize(input_string=None):
    """Find percent symbol (%) to avoid python string format collision"""
    escaped = cgi.escape(input_string)
    input_as_list = list(escaped)
    for index, value in enumerate(input_as_list):
        if value == '%':
            input_as_list[index] = '%%'

    input_string = ''.join(input_as_list)
    return input_string


def generate_unique_code(prefix='ecl-'):
    """Generates a short and easy to remember unique_code.

    The python uuid module generates too long code. In order to keep it short,
    it uses tempfile.NamedTemporaryFile.
    """
    temporary = tempfile.NamedTemporaryFile(prefix=prefix)
    unique_code = os.path.basename(temporary.name)
    return unique_code


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
    column_string = ''
    for key, value in data.iteritems():
        if isinstance(value, basestring):
            column_string += ", {key}='{value}'".format(key=key,
                                                        value=sanitize(value))
        else:
            column_string += ", {key}={value}".format(key=key,
                                                      value=value)
    return column_string


def sql_select_expr_builder(expr=None):
    """SQL select expression builder.

    A helper for building select expression in SQL syntax from python list.
    """
    return ', '.join('{}'.format(expr_item for expr_item in expr))


class DBQuery(object):
    def insert(self, table=None, col=None):
        try:
            sql = "INSERT INTO {} SET id=DEFAULT{}"
            sql = sql.format(table, sql_column_builder(col))
            return query(sql)

        except Exception:
            raise InvalidUsage('Something bad happened in the server.', '',
                               status_code=500)

    def select(self, select_expr=None, table=None, where_clause=None):
        """Select query.

        You can pass the select expression with python list for many columns,
        string for one column, and none if you want to select all.

        Example:

            db_query.select(select_expr=['a_table.id','a_table.name'],
                            table='a_table')

        Equivalent to:

            'SELECT a_table.id, a_table.name FROM a_table'

        """
        try:
            if not select_expr:
                col = '*'
            elif len(select_expr) == 1:
                col = select_expr[0]
            elif isinstance(select_expr, basestring):
                col = select_expr
            else:
                col = sql_select_expr_builder(select_expr)

            sql = 'SELECT {} FROM {}'.format(col, table)
            if where_clause:
                sql_where = "{key}='{value}'"
                for key, value in where_clause.iteritems():
                    sql_where = sql_where.format(key=key, value=sanitize(value))
                sql = 'SELECT {} FROM {} WHERE {}'.format(col,
                                                          table,
                                                          sql_where)

            result = query(sql)
            return result

        except Exception as e:
            raise


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

    def get_all(self):
        """Get all records"""

        try:
            db_query = DBQuery()
            result = db_query.select(table=self.__tablename__)
            return result

        except Exception as e:
            return simple_error_message(str(e))

    def get(self, eclass_id=None):
        """Get record by id"""

        try:
            where_clause = {'id': eclass_id}
            db_query = DBQuery()
            result = db_query.select(table=self.__tablename__,
                                     where_clause=where_clause)
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

    def get_admins(self, eclass_id=None):
        """Get eclass admins"""

        try:
            get_eclass = self.get(eclass_id)
            parse = json.loads(get_eclass)
            admins = parse[0]['admin']
            return admins

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
