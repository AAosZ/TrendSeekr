from Analytics.analytics_engine import AnalyticsEngine
from config import Config
from PostgreDB import DatabaseConnection
import psycopg2

class TestConfig(Config):
    DB_HOST = "localhost"
    DB_NAME = "testdb"
    DB_USER = "postgres"
    DB_PASSWORD = "testpassword"
    DB_PORT = "5432"

def main() -> None:
    config = Config()
    database = DatabaseConnection(config)
    engine = AnalyticsEngine(config)

    config = TestConfig()

    # change this
    connection = psycopg2.connect(
        host=config.DB_HOST,
        dbname=config.DB_NAME,
        user=config.DB_USER,
        password=config.DB_PASSWORD,
        port=config.DB_PORT,
    )
    try:
        engine.process_pending_articles(connection)
    finally:
        connection.close()


if __name__ == "__main__":
    main()
