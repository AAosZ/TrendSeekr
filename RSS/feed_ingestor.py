from datetime import datetime, timezone
from dateutil.parser import parse

from PostgreDB import Queries


class FeedIngestor:
    def __init__(self, insert_article_sql: str | None = None) -> None:
        self.insert_article_sql = insert_article_sql or Queries.INSERT_INTO_ARTICLES_SQL

    def parse_published_date(self, entry) -> datetime:
        """
        Return the RSS published date, or the current UTC time if missing.

        :param entry: RSS feed published date
        :return: datetime
        """
        published = getattr(entry, "published", None)
        if not published:
            return datetime.now(timezone.utc)

        try:
            return parse(published).astimezone(timezone.utc)
        except Exception:
            return datetime.now(timezone.utc)

    def ingest_feeds(self, connection, feed_urls, query: str | None = None) -> None:
        """
        Digests all new RSS feed entries and inserts them into the "articles" table in the PostgreSQL database.

        :param connection: PostgreSQL connection
        :param feed_urls: list of RSS feed urls
        :param query: optional insert query override
        :return: None
        """
        import feedparser

        insert_query = query or self.insert_article_sql

        with connection.cursor() as cursor:
            for feed_url in feed_urls:
                feed = feedparser.parse(feed_url)
                for entry in feed.entries:
                    link = getattr(entry, "link", "").strip()
                    if not link:
                        continue

                    try:
                        published_dt = self.parse_published_date(entry)

                        cursor.execute(
                            insert_query,
                            (
                                getattr(entry, "title", "").strip(),
                                published_dt.isoformat(),
                                link,
                            ),
                        )

                        connection.commit()
                    except Exception as e:
                        connection.rollback()
                        print(f"Feed insert failed for {link}: {e}")
