from openedoo_project import json
from openedoo_project.db.raw import query
from ..database import EclassSchema


class Eclass(object):
    def __init__(self):
        self.__tablename__ = EclassSchema.__tablename__

    def insert(self, data=None):
        """Insert a record"""

        try:
            sql = "INSERT INTO {} VALUES (DEFAULT, '{}', '{}', '{}', '{}', \
            '{}', '{}', '{}')"
            sql = sql.format(self.__tablename__, data['name'], data['course'],
                             data['university'], data['member'], data['admin'],
                             data['privilege'], data['unique_code'])
            query(sql)
            result = {'message': 'success'}
            return result

        except Exception as e:
            return {'error message': e}

    def get_all(self):
        """Get all records"""

        try:
            result = query('SELECT * FROM {}'.format(self.__tablename__))
            return result

        except Exception as e:
            return {'error message': e}

    def get(self, eclass_id=None):
        """Get record by id"""

        try:
            sql = 'SELECT * FROM {} WHERE id={}'
            sql = sql.format(self.__tablename__, eclass_id)
            result = query(sql)
            return result

        except Exception as e:
            return {'error message': e}

    def update(self, data=None):
        """Update a record by id"""

        try:
            # Sql column construction from dict
            column = ', '.join("{key}='{value}'".format(key=key, value=value)
                               for key, value in data.iteritems()
                               if key not in ('id'))
            sql = 'UPDATE {} SET {} WHERE id={}'
            sql = sql.format(self.__tablename__, column, data['id'])
            # The query execution doesn't return any value
            query(sql)
            result = {'message': 'success'}
            return result

        except Exception as e:
            return {'error message': e}

    def delete(self, eclass_id=None):
        """Delete a record by id"""

        try:
            sql = 'DELETE FROM {} WHERE id={}'
            sql = sql.format(self.__tablename__, eclass_id)
            res = query(sql)
            result = {'message': 'success'}
            return result

        except Exception as e:
            return {'error message': repr(e)}

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

            result = {'message': 'success'}
            return result

        except Exception as e:
            return {'error message': repr(e)}

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
            return {'error message': str(e)}

    def get_members(self, eclass_id=None):
        """Get eclass members"""

        try:
            get_eclass = self.get(eclass_id)
            parse = json.loads(get_eclass)
            members = parse[0]['member']
            return members

        except Exception as e:
            return {'error message': e}
