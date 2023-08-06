"""
.. module:: dh_mysql
   :platform: Unix, Windows
   :synopsis: A module which contains the boiler plate methods to be used
   when the database is MySQL.

.. moduleauthor:: Dharmateja Yarlagadda <dharmateja.yarlagadda@eneco.com>

"""

import logging
import MySQLdb
from retrying import retry
from deprecated import deprecated
from datetime import date, timedelta


class SQLClient(object):
    """
    A SQL client for making basic select and updates according to the Datahub Platform.
    """

    def __init__(self,
                 db_host='localhost',
                 db_user_name='developer',
                 db_password='test',
                 db_schema='default',
                 db_port=3306):
        """
        Initialize a new instance.
        If specified, 'db_host' is the name of the remote host to which to
        connect.
        If specified, 'db_user_name' specifies the user_name with which to connect.
        If specified, 'db_password' specifies the password with which to connect.
        If specified, 'db_schema' specifies the schema to connect.
        If specified, 'db_port' specifies the driver to use to connect.
        If these parameters are not specified defaults will be used.

        :param db_host: The database hostname/Ip Address.
        :type db_host: String
        :param db_user_name: The database username
        :type db_user_name: String
        :param db_password: The database password
        :type db_password: String
        :param db_schema: The database schema
        :type db_schema: String
        :param db_port: The port to be used for the connection.
        :type db_port: String
        """

        self.host = db_host
        self.user_name = db_user_name
        self.password = db_password
        self.schema = db_schema
        self.port = db_port

    def get_processed_files_list(self, days_back,
                                 processed_files_list, data_source):
        """
        Provide list of processed files for a particular date based on the days_back variable.

        :param days_back: Number  of days to go back, by default 0
        :param processed_files_list: empty  processed files list.
        :param data_source:  Name of the source
        :return: processed files list: It contains updated processed files list.
        """
        logging.info('DH_Utils: Fetching the list of processed files for a particular date from database')
        with MySQLdb.connect(host=self.host, user=self.user_name,
                             passwd=self.password, db=self.schema,
                             port=self.port).cursor() as cursor:
            file_date = (date.today() - timedelta(days_back)).strftime("%Y-%m-%d")
            query = "select file_name from processed_files_inventory " \
                    "where data_source='{}' and file_date='{}'".format(data_source, file_date)
            cursor.execute(query)
            for row in cursor.fetchall():
                processed_files_list.append(row[0])
        logging.info('DH_Utils: Finished fetching the list of processed files for a particular date from database')
        return processed_files_list, file_date

    def update_processed_files_list(self, file_name, file_date,
                                    processed_time, data_source):
        """
        Update the file_name in MySQL database in processed file list.

        :param file_name: Name of the processed file.
        :param file_date: Processed file date.
        :param processed_time: Processed time of the file.
        :param data_source: Name of the source.
        :return: No return value.
        """
        logging.info('DH_Utils: Updating current processed time,file name and file_date into database')
        with MySQLdb.connect(host=self.host, user=self.user_name,
                             passwd=self.password, db=self.schema,
                             port=self.port).cursor() as cursor:
            query = "insert into processed_files_inventory(data_source,file_name,file_date,processed_time) " \
                    "VALUES ('{}','{}','{}','{}')".format(data_source, file_name, file_date, processed_time)
            cursor.execute(query)
            cursor.execute('commit')
        logging.info('DH_Utils: Finished updating current processed time,file name and file_date into database')

    def get_last_processed_date(self, last_processed_date,
                                data_source,
                                file_name=None):
        """
        Get the last processed date for the given datasource/filename.

        :param last_processed_date: empty list.
        :type last_processed_date: List of datetime.
        :param data_source: Name of the source
        :type data_source: String
        :param file_name: The name of the file.( Default None)
        :type file_name: String
        :return: last_processed_time: The last processed_time for the data_source.
        """
        logging.info('DH_Utils: Fetching last processed date from database')
        with MySQLdb.connect(host=self.host, user=self.user_name,
                             passwd=self.password, db=self.schema,
                             port=self.port).cursor() as cursor:
            if file_name:
                query = "select file_date from applications_inventory where data_source='{}' and file_name ={}" \
                    .format(data_source, file_name)
            else:
                query = "select file_date from applications_inventory where data_source='{}'".format(data_source)
            cursor.execute(query)
            for row in cursor.fetchall():
                last_processed_date.append(row[0])
        logging.info('DH_Utils: Finished fetching last processed date from database')
        return last_processed_date

    def get_last_processed_time(self, last_processed_time,
                                data_source,
                                file_name=None):
        """
        Get the last processed time for the given datasource/filename.

        :param last_processed_time: empty list.
        :type last_processed_time: List of datetime.
        :param data_source: Name of the source
        :type data_source: String
        :param file_name: The name of the file.( Default None)
        :type file_name: String
        :return: last_processed_time: The last processed_time for the data_source.
        """
        logging.info('DH_Utils: Fetching last processed time from database')
        with MySQLdb.connect(host=self.host, user=self.user_name,
                             passwd=self.password, db=self.schema,
                             port=self.port).cursor() as cursor:
            if file_name:
                query = "select processed_time from applications_inventory where data_source='{}' and file_name ={}" \
                    .format(data_source, file_name)
            else:
                query = "select processed_time from applications_inventory where data_source='{}'".format(data_source)
            cursor.execute(query)
            for row in cursor.fetchall():
                last_processed_time.append(row[0])
        logging.info('DH_Utils: Finished fetching last processed time from database')
        return last_processed_time

    def update_processed_time(self, file_date, processed_time,
                              data_source, file_name=None):
        """
        Update the processed_time in database for the given data_source.

        :param file_date: Processed file date.
        :type file_date: String
        :param processed_time: Processed time of the file.
        :type processed_time: String
        :param data_source: Name of the data source.
        :type data_source: String
        :param file_name: The name of the file.( Default None)
        :type file_name: String
        :return: No return
        """
        logging.info('DH_Utils: Updating current processed time and file_date into database')
        with MySQLdb.connect(host=self.host, user=self.user_name,
                             passwd=self.password, db=self.schema,
                             port=self.port).cursor() as cursor:
            if file_name:
                query = "update applications_inventory set file_date='{}', processed_time='{}'" \
                        "where data_source='{}' and file_name='{}'".format(file_date, processed_time, data_source,
                                                                           file_name)
            else:
                query = "update applications_inventory set file_date='{}', processed_time='{}'" \
                        "where data_source='{}'".format(file_date, processed_time, data_source)
            cursor.execute(query)
            cursor.execute('commit')
        logging.info('DH_Utils: Finished updating current processed time and file_date into database')

    def get_err_count(self, data_source):
        """
        Get the error count for the current process

        :param data_source: The data_source for the current process.
        :type data_source: String
        :return: count: Int
        """
        count = 0
        logging.info('DH_Utils: Getting error count if any for the current process.')
        with MySQLdb.connect(host=self.host, user=self.user_name,
                             passwd=self.password, db=self.schema,
                             port=self.port).cursor() as cursor:
            query = "select errors from applications_inventory " \
                    "where data_source='{}'".format(data_source)
            cursor.execute(query)
            for row in cursor.fetchall():
                count = row[0]
        logging.info('DH_Utils: Finished getting error count for the current process.')
        return count

    def update_err_count(self, count, status, data_source):
        """
        Set error count for the given process

        :param count: The error count.
        :type count: Int
        :param status: The process status to be updated
        :type status: Int
        :param data_source: The data_source for the current process.
        :type data_source: String
        :type count: Int
        :return: No return
        """
        logging.info('DH_Utils: Updating error count, status for the current process into database')
        with MySQLdb.connect(host=self.host, user=self.user_name,
                             passwd=self.password, db=self.schema,
                             port=self.port).cursor() as cursor:
            query = "update applications_inventory set errors='{}', status='{}'" \
                    "where data_source='{}'".format(str(count), str(status), data_source)
            cursor.execute(query)
            cursor.execute('commit')
        logging.info('DH_Utils: Finished updating error count, status for the current process into database')

    def __repr__(self):
        return "<{module}.{name} at {id_} (hosts={hosts})>".format(
            module=self.__class__.__module__,
            name=self.__class__.__name__,
            id_=hex(id(self)),
            hosts=self.host,
        )


@deprecated(version='1.1', reason="Methods have been re-written inside a class to remove duplication.")
def get_processed_files_list(db_host, db_user_name, db_password, db_schema, db_port, days_back,
                             processed_files_list, data_source):
    """
    Provide list of processed files for a particular date based on the days_back variable.

    :param db_host: The database hostname/Ip Address.
    :type db_host: String
    :param db_user_name: The database username
    :type db_user_name: String
    :param db_password: The database password
    :type db_password: String
    :param db_schema: The database schema
    :type db_schema: String
    :param db_port: The database port
    :type db_port: Integer
    :param days_back: Number  of days to go back, by default 0
    :param processed_files_list: empty  processed files list.
    :param data_source:  Name of the source
    :return: processed files list: It contains updated processed files list.
    """
    logging.info('DH_Utils: Fetching the list of processed files for a particular date from database')
    with MySQLdb.connect(host=db_host, user=db_user_name,
                         passwd=db_password, db=db_schema,
                         port=db_port).cursor() as cursor:
        file_date = (date.today() - timedelta(days_back)).strftime("%Y-%m-%d")
        query = "select file_name from processed_files_inventory " \
                "where data_source='{}' and file_date='{}'".format(data_source, file_date)
        cursor.execute(query)
        for row in cursor.fetchall():
            processed_files_list.append(row[0])
    logging.info('DH_Utils: Finished fetching the list of processed files for a particular date from database')
    return processed_files_list, file_date


@deprecated(version='1.1', reason="Methods have been re-written inside a class to remove duplication.")
def update_processed_files_list(db_host, db_user_name, db_password, db_schema, db_port, file_name, file_date,
                                processed_time, data_source):
    """
    Update the file_name in MySQL database in processed file list.

    :param db_host: The database hostname/Ip Address.
    :type db_host: String
    :param db_user_name: The database username
    :type db_user_name: String
    :param db_password: The database password
    :type db_password: String
    :param db_schema: The database schema
    :type db_schema: String
    :param db_port: The database port
    :type db_port: Integer
    :param file_name: Name of the processed file.
    :param file_date: Processed file date.
    :param processed_time: Processed time of the file.
    :param data_source: Name of the source.
    :return: No return value.
    """
    logging.info('DH_Utils: Updating current processed time,file name and file_date into database')
    with MySQLdb.connect(host=db_host, user=db_user_name,
                         passwd=db_password, db=db_schema,
                         port=db_port).cursor() as cursor:
        query = "insert into processed_files_inventory(data_source,file_name,file_date,processed_time) " \
                "VALUES ('{}','{}','{}','{}')".format(data_source, file_name, file_date, processed_time)
        cursor.execute(query)
        cursor.execute('commit')
    logging.info('DH_Utils: Finished updating current processed time,file name and file_date into database')


@deprecated(version='1.1', reason="Methods have been re-written inside a class to remove duplication.")
def get_last_processed_date(db_host, db_user_name, db_password, db_schema, db_port, last_processed_date, data_source,
                            file_name=None):
    """
    Get the last processed date for the given datasource/filename.

    :param db_host: The database hostname/Ip Address.
    :type db_host: String
    :param db_user_name: The database username
    :type db_user_name: String
    :param db_password: The database password
    :type db_password: String
    :param db_schema: The database schema
    :type db_schema: String
    :param db_port: The database port
    :type db_port: Integer
    :param last_processed_date: empty list.
    :type last_processed_date: List of datetime.
    :param data_source: Name of the source
    :type data_source: String
    :param file_name: The name of the file.( Default None)
    :type file_name: String
    :return: last_processed_time: The last processed_time for the data_source.
    """
    logging.info('DH_Utils: Fetching last processed date from database')
    with MySQLdb.connect(host=db_host, user=db_user_name,
                         passwd=db_password, db=db_schema,
                         port=db_port).cursor() as cursor:
        if file_name:
            query = "select file_date from applications_inventory where data_source='{}' and file_name ={}" \
                .format(data_source, file_name)
        else:
            query = "select file_date from applications_inventory where data_source='{}'".format(data_source)
        cursor.execute(query)
        for row in cursor.fetchall():
            last_processed_date.append(row[0])
    logging.info('DH_Utils: Finished fetching last processed date from database')
    return last_processed_date


@deprecated(version='1.1', reason="Methods have been re-written inside a class to remove duplication.")
def get_last_processed_time(db_host, db_user_name, db_password, db_schema, db_port, last_processed_time, data_source,
                            file_name=None):
    """
    Get the last processed time for the given datasource/filename.

    :param db_host: The database hostname/Ip Address.
    :type db_host: String
    :param db_user_name: The database username
    :type db_user_name: String
    :param db_password: The database password
    :type db_password: String
    :param db_schema: The database schema
    :type db_schema: String
    :param db_port: The database port
    :type db_port: Integer
    :param last_processed_time: empty list.
    :type last_processed_time: List of datetime.
    :param data_source: Name of the source
    :type data_source: String
    :param file_name: The name of the file.( Default None)
    :type file_name: String
    :return: last_processed_time: The last processed_time for the data_source.
    """
    logging.info('DH_Utils: Fetching last processed time from database')
    with MySQLdb.connect(host=db_host, user=db_user_name,
                         passwd=db_password, db=db_schema,
                         port=db_port).cursor() as cursor:
        if file_name:
            query = "select processed_time from applications_inventory where data_source='{}' and file_name ={}" \
                .format(data_source, file_name)
        else:
            query = "select processed_time from applications_inventory where data_source='{}'".format(data_source)
        cursor.execute(query)
        for row in cursor.fetchall():
            last_processed_time.append(row[0])
    logging.info('DH_Utils: Finished fetching last processed time from database')
    return last_processed_time


@deprecated(version='1.1', reason="Methods have been re-written inside a class to remove duplication.")
def update_processed_time(db_host, db_user_name, db_password, db_schema, db_port, file_date, processed_time,
                          data_source, file_name=None):
    """
    Update the processed_time in database for the given data_source.

    :param db_host: The database hostname/Ip Address.
    :type db_host: String
    :param db_user_name: The database username
    :type db_user_name: String
    :param db_password: The database password
    :type db_password: String
    :param db_schema: The database schema
    :type db_schema: String
    :param db_port: The database port
    :type db_port: Integer
    :param file_date: Processed file date.
    :type file_date: String
    :param processed_time: Processed time of the file.
    :type processed_time: String
    :param data_source: Name of the data source.
    :type data_source: String
    :param file_name: The name of the file.( Default None)
    :type file_name: String
    :return: No return
    """
    logging.info('DH_Utils: Updating current processed time and file_date into database')
    with MySQLdb.connect(host=db_host, user=db_user_name,
                         passwd=db_password, db=db_schema,
                         port=db_port).cursor() as cursor:
        if file_name:
            query = "update applications_inventory set file_date='{}', processed_time='{}'" \
                    "where data_source='{}' and file_name='{}'".format(file_date, processed_time, data_source,
                                                                       file_name)
        else:
            query = "update applications_inventory set file_date='{}', processed_time='{}'" \
                    "where data_source='{}'".format(file_date, processed_time, data_source)
        cursor.execute(query)
        cursor.execute('commit')
    logging.info('DH_Utils: Finished updating current processed time and file_date into database')


@deprecated(version='1.1', reason="Methods have been re-written inside a class to remove duplication.")
def get_err_count(db_host, db_user_name, db_password, db_schema, db_port, data_source):
    """
    Get the error count for the current process

    :param db_host: The database hostname/Ip Address.
    :type db_host: String
    :param db_user_name: The database username
    :type db_user_name: String
    :param db_password: The database password
    :type db_password: String
    :param db_schema: The database schema
    :type db_schema: String
    :param db_port: The database port
    :type db_port: Integer
    :param data_source: The data_source for the current process.
    :type data_source: String
    :return: count: Int
    """
    count = 0
    logging.info('DH_Utils: Getting error count if any for the current process.')
    with MySQLdb.connect(host=db_host, user=db_user_name,
                         passwd=db_password, db=db_schema,
                         port=db_port).cursor() as cursor:
        query = "select errors from applications_inventory " \
                "where data_source='{}'".format(data_source)
        cursor.execute(query)
        for row in cursor.fetchall():
            count = row[0]
    logging.info('DH_Utils: Finished getting error count for the current process.')
    return count


@deprecated(version='1.1', reason="Methods have been re-written inside a class to remove duplication.")
def update_err_count(db_host, db_user_name, db_password, db_schema, db_port, count, status, data_source):
    """
    Set error count for the given process

    :param db_host: The database hostname/Ip Address.
    :type db_host: String
    :param db_user_name: The database username
    :type db_user_name: String
    :param db_password: The database password
    :type db_password: String
    :param db_schema: The database schema
    :type db_schema: String
    :param db_port: The database port
    :type db_port: Integer
    :param count: The error count.
    :type count: Int
    :param status: The process status to be updated
    :type status: Int
    :param data_source: The data_source for the current process.
    :type data_source: String
    :type count: Int
    :return: No return
    """
    logging.info('DH_Utils: Updating error count, status for the current process into database')
    with MySQLdb.connect(host=db_host, user=db_user_name,
                         passwd=db_password, db=db_schema,
                         port=db_port).cursor() as cursor:
        query = "update applications_inventory set errors='{}', status='{}'" \
                "where data_source='{}'".format(str(count), str(status), data_source)
        cursor.execute(query)
        cursor.execute('commit')
    logging.info('DH_Utils: Finished updating error count, status for the current process into database')
