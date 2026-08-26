"""
This file connects the application to the PostgreSQL database.
"""

import logging
from contextlib import contextmanager

import psycopg2


class DatabaseConnection:
    logger = logging.getLogger(__name__)

    def __init__(self, config) -> None:
        self.config = config

    def get_connection(self):
        return psycopg2.connect(
            host=self.config.DB_HOST,
            dbname=self.config.DB_NAME,
            user=self.config.DB_USER,
            password=self.config.DB_PASSWORD,
            port=self.config.DB_PORT,
        )

    @contextmanager
    def get_cursor(self):
        connection = self.get_connection()
        try:
            with connection.cursor() as cursor:
                yield cursor
                connection.commit()
        except psycopg2.Error as e:
            connection.rollback()
            self.logger.error(f"Database error: {e}", exc_info=True)
            raise
        except Exception as e:
            connection.rollback()
            self.logger.error(f"Unexpected error: {e}", exc_info=True)
            raise
        finally:
            connection.close()
