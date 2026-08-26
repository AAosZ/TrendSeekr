from config import Config
from PostgreDB.queries import Queries
from typing import Any


class Processor:

    def __init__(self, config: Config, analyzer) -> None:
        self.queries = Queries()
        self.config = config
        self.analyzer = analyzer
        if self.config.BATCH_SIZE < 1:
            raise ValueError("BATCH_SIZE must be at least 1.")

    def fetch_unprocessed_articles(self, connection, query) -> list[dict[str, Any]]:

        with connection.cursor() as cursor:
            cursor.execute(query)
            rows = cursor.fetchall()

        return [
            {
                "id": article_id,
                "title": title or "",
                "date": article_date,
                "url": url or "",
            }
            for article_id, title, article_date, url in rows
        ]

    @staticmethod
    def chunked(items: list[dict[str, Any]], size: int):
        for index in range(0, len(items), size):
            yield items[index:index + size]

    def store_ai_analysis(self, connection, analysis_results: list[dict[str, Any]]) -> None:
        from psycopg2.extras import Json

        with connection.cursor() as cursor:
            for result in analysis_results:
                cursor.execute(
                    self.queries.UPSERT_ANALYSIS_SQL,
                    (
                        result["id"],
                        result["url"],
                        self.config.MODEL_NAME,
                        result["theme"],
                        result["direction"],
                        result["market_relevant"],
                        result["north_american_impact"],
                        result["confidence"],
                        result["signal_strength"],
                        result["time_of_influence"],
                        result["trend_categories"],
                        Json(result),
                    ),
                )
                cursor.execute(self.queries.MARK_PROCESSED_SQL, (result["id"],))

        connection.commit()

    def process_unprocessed_articles(self, connection, query) -> None:
        articles = self.fetch_unprocessed_articles(connection, query)
        if not articles:
            print("No unprocessed articles found.")
            return

        print(f"Found {len(articles)} unprocessed articles.")

        for batch in self.chunked(articles, self.config.BATCH_SIZE):
            try:
                analysis_results = self.analyzer.classify_headlines(batch)
                self.store_ai_analysis(connection, analysis_results)

                relevant_count = sum(1 for result in analysis_results if result["market_relevant"])
                print(
                    f"Processed {len(analysis_results)} articles "
                    f"({relevant_count} market-relevant)."
                )
            except Exception as e:
                connection.rollback()
                batch_ids = ", ".join(str(article["id"]) for article in batch)
                print(f"Failed to process batch [{batch_ids}]: {e}")
