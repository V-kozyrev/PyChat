import psycopg2

import constants

from db.db_service import DataBaseServices


class DataBase:
    _service: DataBaseServices = None

    def __init__(self) -> None:
        self._connect_to_db()

    def _connect_to_db(self):
        try:
            # Connecting to an existing database
            self._connect_to_db = psycopg2.connect(user=constants.DbConstants.user,
                                                   password=constants.DbConstants.password,
                                                   host=constants.DbConstants.host,
                                                   port=constants.DbConstants.port,
                                                   database=constants.DbConstants.database)
        except psycopg2.OperationalError as error:
            constants.ChatConstants.logger.error("Ошибка при работе с PostgreSQL %s", type(error))

    def get_service(self):
        if self._service is None:
            self._service = DataBaseServices(self._connect_to_db)
        return self._service

    def data_base_close(self):
        self._connect_to_db.close()
        constants.ChatConstants.logger.info("Соединение с PostgreSQL закрыто")
