import os

class Config:
    # NOTE: THIS ENTIRE APP IS RAN LOCALLY

    # Local database access information
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_NAME = os.getenv("DB_NAME", "news_scraper")
    DB_USER = os.getenv("DB_USER", "postgres")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "723905")
    DB_PORT = os.getenv("DB_PORT", "25565")

    # Define local model path
    DEFAULT_MODEL_PATH = "C:/Users/shawn/Documents/Portfolio/Coding/News Scraper/DeepSeek-R1-Distill-Qwen-14B-Q4_K_M.gguf"
    MODEL_PATH = os.getenv("NEWS_LLM_MODEL_PATH", DEFAULT_MODEL_PATH)
    MODEL_NAME = os.getenv("NEWS_LLM_MODEL_NAME", os.path.basename(MODEL_PATH))

    # Local embedding model used by the analytics entity pipeline.
    DEFAULT_EMBEDDING_MODEL_PATH = "C:/Users/shawn/Documents/Portfolio/Coding/News Scraper/Qwen3-Embedding-8B-Q8_0.gguf"
    EMBEDDING_MODEL_PATH = os.getenv("NEWS_EMBEDDING_MODEL_PATH", DEFAULT_EMBEDDING_MODEL_PATH)
    EMBEDDING_MODEL_NAME = os.getenv(
        "NEWS_EMBEDDING_MODEL_NAME",
        os.path.basename(EMBEDDING_MODEL_PATH),
    )

    # Model configuration
    BATCH_SIZE = int(os.getenv("NEWS_LLM_BATCH_SIZE", "8"))
    N_CTX = int(os.getenv("NEWS_LLM_CONTEXT", "4096"))
    N_GPU_LAYERS = int(os.getenv("NEWS_LLM_GPU_LAYERS", "-1"))
    N_THREADS = int(os.getenv("NEWS_LLM_THREADS", "12"))
    MAX_TOKENS = int(os.getenv("NEWS_LLM_MAX_TOKENS", "1400"))
    TEMPERATURE = float(os.getenv("NEWS_LLM_TEMPERATURE", "0.1"))

    # Analytics configuration
    SPACY_MODEL = os.getenv("NEWS_ANALYTICS_SPACY_MODEL", "en_core_web_lg")
    EMBEDDING_DIMENSION = int(os.getenv("NEWS_EMBEDDING_DIMENSION", "1024"))
    ENTITY_SIMILARITY_THRESHOLD = float(os.getenv("NEWS_ENTITY_SIMILARITY_THRESHOLD", "0.86"))
    ANALYTICS_BATCH_SIZE = int(os.getenv("NEWS_ANALYTICS_BATCH_SIZE", "25"))

    # RSS feed repository
    feed_urls = {
        # Yahoo RSS
        "https://news.yahoo.com/rss/finance",
        "https://news.yahoo.com/rss/tech",
        "https://news.yahoo.com/rss/business",
        "https://news.yahoo.com/rss/health",
        "https://news.yahoo.com/rss/science",

        # Reuters RSS using Google News
        "https://news.google.com/rss/search?q=site%3Areuters.com&hl=en-US&gl=US&ceid=US%3Aen",

        # Wall Street Journal
        "https://feeds.content.dowjones.io/public/rss/RSSMarketsMain",
        "https://feeds.content.dowjones.io/public/rss/RSSWorldNews",
        "https://feeds.content.dowjones.io/public/rss/WSJcomUSBusiness",
        "https://feeds.content.dowjones.io/public/rss/RSSWSJD",
        "https://feeds.content.dowjones.io/public/rss/socialhealth",

        # Google News RSS Front Page
        "https://news.google.com/rss?hl=en-US&gl=US&ceid=US:en",
    }
