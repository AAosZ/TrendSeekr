from PostgreDB.queries import Queries
from config import Config
from PostgreDB import Queries
from RSS import FeedIngestor


def ensure_schema(connection) -> None:
    with connection.cursor() as cursor:
        cursor.execute(Queries.CREATE_ARTICLES_TABLE_SQL)
        cursor.execute(Queries.CREATE_ANALYSIS_TABLE_SQL)
    connection.commit()


def main() -> None:
    from LLM import ArticleAnalyzer, Client, Processor
    from PostgreDB import DatabaseConnection

    config = Config()
    database = DatabaseConnection(config)
    client = Client(config)
    analyzer = ArticleAnalyzer(client)
    processor = Processor(config, analyzer)
    ingestor = FeedIngestor()
    query = Queries.FETCH_UNPROCESSED_SQL

    connection = database.get_connection()
    try:
        ensure_schema(connection)
        ingestor.ingest_feeds(connection, config.feed_urls)
        processor.process_unprocessed_articles(connection, query)
    finally:
        connection.close()


if __name__ == "__main__":
    main()
