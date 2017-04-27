

class Eclass(object):
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
            raise {'error message':e}

    def get_all(self):
        """Get all records"""

        try:
            result = query('SELECT * FROM {}'.format(self.__tablename__))
            return result

        except Exception as e:
            raise {'error message':e}

    def get(self, eclass_id=None):
        """Get record by id"""

        try:
            sql = 'SELECT * FROM {} WHERE id={}'
            sql = sql.format(self.__tablename__, eclass_id)
            result = query(sql)
            return result

        except Exception as e:
            raise {'error message':e}

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
            raise {'error message':e}
