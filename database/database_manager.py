import tracker_config as tkc
from PyQt6.QtSql import QSqlDatabase, QSqlQuery
import os
import shutil
from typing import List, Union
from logger_setup import logger

user_dir: str = os.path.expanduser('~')
db_path: str = os.path.join(os.getcwd(), tkc.DB_NAME)  # Database Name
target_db_path: str = os.path.join(user_dir, tkc.DB_NAME)  # Database Name


def initialize_database() -> None:
    """
    Initializes the database by creating a new database file or copying an existing one.

    If the target database file doesn't exist, it checks if the source database file exists.
    If the source database file exists, it copies it to the target location.
    If the source database file doesn't exist, it creates a new database file using the 'QSQLITE' driver.

    Returns:
        None

    Raises:
        Exception: If there is an error creating or copying the database file.
    """
    try:
        if not os.path.exists(target_db_path):
            if os.path.exists(db_path):
                shutil.copy(db_path, target_db_path)
            else:
                db: QSqlDatabase = QSqlDatabase.addDatabase('QSQLITE')
                db.setDatabaseName(target_db_path)
                if not db.open():
                    logger.error("Error: Unable to create database")
                db.close()
    except Exception as e:
        logger.error("Error: Unable to create database", str(e))


class DataManager:
    
    def __init__(self, db_name: str = target_db_path) -> None:
        """
        Initializes the DataManager object and opens the database connection.

        Args:
            db_name (str): The path to the SQLite database file.

        Raises:
            Exception: If there is an error opening the database.

        """
        try:
            self.db: QSqlDatabase = QSqlDatabase.addDatabase('QSQLITE')
            self.db.setDatabaseName(db_name)
            
            if not self.db.open():
                logger.error("Error: Unable to open database")
            logger.info("DB INITIALIZING")
            self.query: QSqlQuery = QSqlQuery()
            self.setup_tables()
        except Exception as e:
            logger.error(f"Error: Unable to open database {e}", exc_info=True)
    
    def setup_tables(self) -> None:
        """
        Sets up the necessary tables in the database.

        """
        self.setup_altman_table()
    
    def setup_altman_table(self) -> None:
        """
        Sets up the 'altman_table' in the database if it doesn't already exist.

        This method creates a table named 'altman_table' in the database with the following columns:
        - id: INTEGER (Primary Key, Autoincrement)
        - mental_mental_date: TEXT
        - mental_mental_time: TEXT
        - mood_slider: INTEGER
        - mania_slider: INTEGER
        - depression_slider: INTEGER
        - mixed_risk_slider: INTEGER

        If the table already exists, this method does nothing.

        Returns:
            None
        """
        if not self.query.exec(f"""
                        CREATE TABLE IF NOT EXISTS altman_table (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                         altman_date TEXT,
                         altman_time TEXT,
                         altmans_sleep INTEGER,
                         altmans_speech INTEGER,
                         altmans_activity INTEGER,
                         altmans_cheer INTEGER,
                         altmans_confidence INTEGER,
                         altmans_summary INTEGER
                        )"""):
            logger.error(f"Error creating table: altman_table",
                         self.query.lastError().text())
    
    def insert_into_altman_table(self,
                                 altman_date: str,
                                 altman_time: str,
                                 altmans_sleep: int,
                                 altmans_speech: int,
                                 altmans_activity: int,
                                 altmans_cheer: int,
                                 altmans_confidence: int,
                                 altmans_summary: int
                                 ) -> None:
        """
        Inserts data into the altman_table.

        Args:
            altman_date (str): The date of the mental_mental record.
            altman_time (str): The date of the mental_mental record.
            sleep (str): The time of the mental_mental record.
            speech (int): The value of the mood slider.
            activity (int): The value of the mania slider.
            cheer (int): The value of the depression slider.
            confidence (int): The value of the mixed risk slider.
            altmans_summary (int): the summary of all things and all things summary'd

        Returns:
            None

        Raises:
            ValueError: If the number of bind values does not match the number of placeholders in the SQL query.
            Exception: If there is an error during data insertion.

        """
        sql: str = f"""INSERT INTO altman_table(
        altman_date,
        altman_time,
        altmans_sleep,
        altmans_speech,
        altmans_activity,
        altmans_cheer,
        altmans_confidence,
        altmans_summary
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)"""
        bind_values: List[Union[str, int]] = [altman_date, altman_time, altmans_sleep, altmans_speech, altmans_activity, altmans_cheer, altmans_confidence, altmans_summary]
        try:
            self.query.prepare(sql)
            for value in bind_values:
                self.query.addBindValue(value)
            if sql.count('?') != len(bind_values):
                raise ValueError(f"""Mismatch: altman_table Expected {sql.count('?')}
                    bind values, got {len(bind_values)}.""")
            if not self.query.exec():
                logger.error(
                    f"Error inserting data: altman_table - {self.query.lastError().text()}")
        except ValueError as e:
            logger.error(f"ValueError altman_table: {e}")
        except Exception as e:
            logger.error(f"Error during data insertion: altman_table {e}", exc_info=True)


def close_database(self) -> None:
    """
    Closes the database connection if it is open.

    This method checks if the database connection is open and closes it if it is.
    If the connection is already closed or an error occurs while closing the
    connection, an exception is logged.

    Raises:
        None

    Returns:
        None
    """
    try:
        logger.info("if database is open")
        if self.db.isOpen():
            logger.info("the database is closed successfully")
            self.db.close()
    except Exception as e:
        logger.exception(f"Error closing database: {e}")