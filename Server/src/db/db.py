import psycopg2
import logging
import constants
from db.db_service import DataBaseServices

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class DataBase:
    _service: DataBaseServices = None

    def __init__(self) -> None:
        self._connect_to_db()

    def _connect_to_db(self):
        """
        Connect to db
        :return: Nothing
        """
        try:
            self._connect_to_db = psycopg2.connect(user=constants.DbConstants.user,
                                                   password=constants.DbConstants.password,
                                                   host=constants.DbConstants.host,
                                                   port=constants.DbConstants.port,
                                                   database=constants.DbConstants.database)
            logger.info("PostgreSQL connection open")
        except psycopg2.OperationalError as error:
            logger.error("Error while working with PostgreSQL %s", type(error))

    def get_service(self):
        """
        Get db service
        :return: db service
        """
        if self._service is None:
            self._service = DataBaseServices(self._connect_to_db)
        return self._service

    def data_base_close(self):
        """
        Close db
        :return: Nothing
        """
        self._connect_to_db.close()
        logger.info("PostgreSQL connection closed")
