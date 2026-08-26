import psycopg2
import run

# Rescores all articles in the article_scraper postgreSQL database. This is a separate file that executes differently from the main file
# Mainly used to rescore old articles that were scored with a previous scorer model.


RESCORE_ALL_SQL = """
SELECT id, title, url
FROM articles;
"""

UPSERT_SCORE_SQL = """
INSERT INTO article_scores (url, relevance_score, analysis_date)
VALUES (%s, %s, NOW())
ON CONFLICT (url)
DO UPDATE SET
    relevance_score = EXCLUDED.relevance_score,
    analysis_date = EXCLUDED.analysis_date;
"""

def reprocess_articles(connection, company_symbols, company_names):
    with connection.cursor() as cursor:
        cursor.execute(RESCORE_ALL_SQL)
        rows = cursor.fetchall()

        for article_id, title, url in rows:
            try:
                relevance_score = main.scorer(title, company_symbols, company_names)

                cursor.execute(
                    UPSERT_SCORE_SQL,
                    (url, relevance_score),
                )

                connection.commit()
                print(f"Processed article {article_id}: score={relevance_score}")

            except Exception as e:
                connection.rollback()
                print(f"Failed on article {article_id}: {e}")

feed_urls = {
    # |--Yahoo RSS--|
    "https://news.yahoo.com/rss/finance",
    "https://news.yahoo.com/rss/tech",
    "https://news.yahoo.com/rss/business",
    "https://news.yahoo.com/rss/health",
    "https://news.yahoo.com/rss/science",
    # |--Reuters RSS using Google News--|
    "https://news.google.com/rss/search?q=site%3Areuters.com&hl=en-US&gl=US&ceid=US%3Aen",
    # |--Wall Street Journal--|
    "https://feeds.content.dowjones.io/public/rss/RSSMarketsMain",
    "https://feeds.content.dowjones.io/public/rss/RSSWorldNews",
    "https://feeds.content.dowjones.io/public/rss/WSJcomUSBusiness",
    "https://feeds.content.dowjones.io/public/rss/RSSWSJD",
    "https://feeds.content.dowjones.io/public/rss/socialhealth",
    # |--Google News RSS Front Page--|
    "https://news.google.com/rss?hl=en-US&gl=US&ceid=US:en",
}

company_symbols, company_names = main.ticker_lookup(
    "C:/Users/wr/Downloads/nasdaq-listed.csv"
)

try:
    connection = psycopg2.connect(
        host="localhost",
        database="news_scraper",
        user="postgres",
        password="",
        port="25565"
    )

    main.ingest_feeds(connection, feed_urls)
    reprocess_articles(connection, company_symbols, company_names)

    connection.close()

except psycopg2.Error as e:
    print(f"Database error: {e}")
except Exception as e:
    print(f"General error: {e}")
