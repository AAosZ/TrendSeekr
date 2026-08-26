import sys
from pathlib import Path
from typing import Any
from PostgreDB.queries import Queries
from config import Config
from PostgreDB import Queries
from RSS import FeedIngestor

import psycopg2

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from config import Config
from LLM import Processor
from PostgreDB import Queries


class TestConfig(Config):
    DB_HOST = "localhost"
    DB_NAME = "testdb"
    DB_USER = "postgres"
    DB_PASSWORD = "testpassword"
    DB_PORT = "5432"
    MODEL_NAME = "test-analyzer"
    BATCH_SIZE = 2



def ensure_schema(connection) -> None:
    with connection.cursor() as cursor:
        cursor.execute(Queries.CREATE_ARTICLES_TABLE_SQL)
        cursor.execute(Queries.CREATE_ANALYSIS_TABLE_SQL)
    connection.commit()


def main() -> None:
    from LLM import ArticleAnalyzer, Client, Processor

    config = Config()
    client = Client(config)
    analyzer = ArticleAnalyzer(client)
    query = Queries.FETCH_UNPROCESSED_SQL

    config = TestConfig()
    processor = Processor(config, analyzer)

    connection = psycopg2.connect(
        host=config.DB_HOST,
        dbname=config.DB_NAME,
        user=config.DB_USER,
        password=config.DB_PASSWORD,
        port=config.DB_PORT,
    )
    try:
        ensure_schema(connection)
        processor.process_unprocessed_articles(connection, query)
    finally:
        connection.close()


if __name__ == "__main__":
    main()
