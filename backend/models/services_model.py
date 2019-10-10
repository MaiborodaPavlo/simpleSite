import datetime

import pymysql

import config
from logger import class_logger, logger


@class_logger()
class ServicesRow:

    def __init__(self, dict_values):
        for key, value in dict_values.items():
            if key == 'creation_request_sent_date':
                key = '_creation_request_sent_date'
            try:
                self.__dict__[key] = pymysql.escape_string(value)
            except TypeError as ex:
                logger.error(f'{ex.__class__}: {ex}')

    @property
    def creation_request_sent_date(self):
        if self._creation_request_sent_date.lower() in ('null', '0000-00-00 00:00:00'):
            return 'default(creation_request_sent_date)'
        else:
            return f"'{self._creation_request_sent_date}'"

    def __repr__(self):
        return f"{self.service_id}, '{self.servtype}', '{self.subtype}', {self.user_id}, " \
            f"{self.referrer_user_id}, '{self.state}', '{self.creation_date}', '{self.creation_time}', " \
            f"{self.creation_request_sent_date}, {self.notified_about_expiration}"

    def is_valid(self):
        attributes = ('service_id', 'servtype', 'subtype', 'user_id', 'referrer_user_id',
                      'state', 'creation_date', 'creation_time', 'creation_request_sent_date',
                      'notified_about_expiration')
        try:
            for attr in attributes:
                self.__getattribute__(attr)
            return True
        except AttributeError:
            return False


@class_logger()
class ServicesModel:

    def __init__(self):
        self._connection = pymysql.connect(host=config.get_setting(config.PATH, 'Database', 'host'),
                                           port=int(config.get_setting(config.PATH, 'Database', 'port')),
                                           user=config.get_setting(config.PATH, 'Database', 'user'),
                                           passwd=config.get_setting(config.PATH, 'Database', 'password'),
                                           db=config.get_setting(config.PATH, 'Database', 'db'),
                                           local_infile=True)
        self._cursor = self._connection.cursor()
        self._table = config.get_setting(config.PATH, 'Database', 'table')

    def get_all(self):
        sql = f'SELECT * FROM {self._table}'
        self._cursor.execute(sql)
        logger.info(sql)

        result = list()

        field_names = [item[0] for item in self._cursor.description]
        for row in self._cursor:
            row_dict = {}
            for i, cell in enumerate(row):
                if isinstance(cell, (datetime.datetime, datetime.date, datetime.time, datetime.timedelta)):
                    cell = str(cell)
                row_dict[field_names[i]] = cell
            result.append(row_dict)

        return result

    def update_row(self, service_id, services_row):

        sql = f"UPDATE {self._table} SET " \
            f"servtype='{services_row.servtype}', subtype='{services_row.subtype}', " \
            f"user_id={services_row.user_id}, referrer_user_id={services_row.referrer_user_id}, " \
            f"state='{services_row.state}', creation_date='{services_row.creation_date}', " \
            f"creation_time='{services_row.creation_time}', " \
            f"creation_request_sent_date={services_row.creation_request_sent_date}, " \
            f"notified_about_expiration={services_row.notified_about_expiration} " \
            f"WHERE service_id={service_id};"
        logger.info(sql)

        try:
            row_count = self._cursor.execute(sql)
        except (pymysql.err.InternalError, pymysql.err.ProgrammingError, pymysql.err.DataError) as err:
            logger.error(str(err))
            return

        self._connection.commit()

        return row_count

    def delete_row(self, service_id):
        sql = f'DELETE FROM {self._table} WHERE service_id={service_id};'
        logger.info(sql)
        try:
            row_count = self._cursor.execute(sql)
        except pymysql.err.InternalError as err:
            logger.error(str(err))
            return

        self._connection.commit()

        return row_count

    def add_row(self, services_row):
        sql = f'INSERT {self._table} VALUE ({services_row});'
        logger.info(sql)
        try:
            row_count = self._cursor.execute(sql)
        except (pymysql.err.InternalError, pymysql.err.IntegrityError, pymysql.err.DataError) as err:
            logger.error(str(err))
            return

        self._connection.commit()

        return row_count

    def upload_data(self, path_to_file):
        sql = f"LOAD DATA LOCAL INFILE '{path_to_file}' INTO TABLE {self._table} " \
            f"FIELDS TERMINATED BY ';' " \
            f"LINES TERMINATED BY '\n' " \
            f"IGNORE 1 ROWS " \
            f"(service_id, servtype, subtype, user_id," \
            f"referrer_user_id, state, creation_date," \
            f"creation_time, creation_request_sent_date," \
            f"notified_about_expiration);"
        logger.info(sql)
        try:
            self._truncate_table()
            row_count = self._cursor.execute(sql)
        except pymysql.err.InternalError as err:
            logger.error(str(err))
            return

        self._connection.commit()

        return row_count

    def _truncate_table(self):
        sql = f'TRUNCATE TABLE {self._table}'
        logger.info(sql)
        self._cursor.execute(sql)
