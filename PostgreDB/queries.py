"""
Repository of PostgreSQL queries used in this project.
"""


class Queries:
    CREATE_VECTOR_EXTENSION_SQL = """
        CREATE EXTENSION IF NOT EXISTS vector SCHEMA public;
    """

    CREATE_ARTICLES_TABLE_SQL = """
        CREATE TABLE IF NOT EXISTS articles (
        id SERIAL PRIMARY KEY,
        title TEXT NOT NULL,
        date TIMESTAMPTZ NOT NULL,
        url TEXT UNIQUE NOT NULL,
        processed BOOLEAN NOT NULL DEFAULT FALSE
    );
    """

    CREATE_ANALYSIS_TABLE_SQL = """
        CREATE TABLE IF NOT EXISTS article_analysis (
            article_id INTEGER PRIMARY KEY REFERENCES articles(id) ON DELETE CASCADE,
            url TEXT NOT NULL,
            model TEXT NOT NULL,
            theme TEXT NOT NULL DEFAULT 'unclassified',
            direction TEXT NOT NULL DEFAULT 'neutral',
            market_relevant BOOLEAN NOT NULL,
            north_american_impact BOOLEAN NOT NULL DEFAULT FALSE,
            confidence DOUBLE PRECISION NOT NULL,
            signal_strength TEXT NOT NULL DEFAULT 'none',
            time_of_influence TEXT NOT NULL DEFAULT 'within year',
            trend_categories TEXT[] NOT NULL DEFAULT ARRAY[]::TEXT[],
            analysis JSONB NOT NULL,
            analysis_date TIMESTAMPTZ NOT NULL DEFAULT NOW(),
            analyzed BOOLEAN NOT NULL DEFAULT FALSE
        );
    """

    CREATE_ENTITIES_TABLE_SQL = """
        CREATE TABLE IF NOT EXISTS entities (
            entity_id SERIAL PRIMARY KEY,
            entity_name TEXT NOT NULL,
            entity_type TEXT NOT NULL DEFAULT 'concept',
            embedding VECTOR(2000) NOT NULL,
            created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
        );
    """

    CREATE_ARTICLE_ENTITIES_TABLE_SQL = """
        CREATE TABLE IF NOT EXISTS article_entities (
            article_id INTEGER NOT NULL REFERENCES articles(id) ON DELETE CASCADE,
            entity_id INTEGER NOT NULL REFERENCES entities(entity_id) ON DELETE CASCADE,
            date_added TIMESTAMPTZ NOT NULL DEFAULT NOW(),
            PRIMARY KEY (article_id, entity_id)
        );
    """

    CREATE_ENTITIES_NAME_TYPE_INDEX_SQL = """
        CREATE UNIQUE INDEX IF NOT EXISTS entities_name_type_idx
        ON entities (entity_name, entity_type);
    """

    CREATE_ENTITIES_EMBEDDING_INDEX_SQL = """
        CREATE INDEX IF NOT EXISTS entities_embedding_cosine_idx
        ON entities
        USING ivfflat (embedding vector_cosine_ops)
        WITH (lists = 100);
    """

    FETCH_ANALYSIS_FOR_ANALYTICS_SQL = """
        SELECT
            aa.article_id,
            COALESCE(a.title, '') AS title,
            aa.url,
            aa.theme,
            aa.trend_categories,
            COALESCE(aa.analysis ->> 'reason', '') AS reason
        FROM article_analysis aa
        JOIN articles a ON a.id = aa.article_id
        WHERE aa.analyzed = FALSE
            AND aa.market_relevant = TRUE
            AND aa.north_american_impact = TRUE
        ORDER BY aa.analysis_date ASC
        LIMIT %s;
    """

    FIND_SIMILAR_ENTITY_SQL = """
        SELECT
            entity_id,
            entity_name,
            entity_type,
            1 - (embedding <=> %s::vector) AS cosine_similarity
        FROM entities
        WHERE 1 - (embedding <=> %s::vector) >= %s
        ORDER BY embedding <=> %s::vector
        LIMIT 1;
    """

    INSERT_ENTITY_SQL = """
        INSERT INTO entities (entity_name, entity_type, embedding)
        VALUES (%s, %s, %s::vector)
        ON CONFLICT (entity_name, entity_type)
        DO UPDATE SET entity_name = EXCLUDED.entity_name
        RETURNING entity_id;
    """

    INSERT_ARTICLE_ENTITY_SQL = """
        INSERT INTO article_entities (article_id, entity_id, date_added)
        VALUES (%s, %s, NOW())
        ON CONFLICT (article_id, entity_id) DO NOTHING;
    """

    MARK_ANALYSIS_ANALYZED_SQL = """
        UPDATE article_analysis
        SET analyzed = TRUE
        WHERE article_id = %s;
    """

    FETCH_UNPROCESSED_SQL = """
        SELECT id, title, date, url
        FROM articles
        WHERE processed = FALSE
        ORDER BY date DESC;
    """

    UPSERT_ANALYSIS_SQL = """
        INSERT INTO article_analysis (
            article_id,
            url,
            model,
            theme,
            direction,
            market_relevant,
            north_american_impact,
            confidence,
            signal_strength,
            time_of_influence,
            trend_categories,
            analysis,
            analysis_date
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, NOW())
        ON CONFLICT (article_id)
        DO UPDATE SET
            url = EXCLUDED.url,
            model = EXCLUDED.model,
            theme = EXCLUDED.theme,
            direction = EXCLUDED.direction,
            market_relevant = EXCLUDED.market_relevant,
            north_american_impact = EXCLUDED.north_american_impact,
            confidence = EXCLUDED.confidence,
            signal_strength = EXCLUDED.signal_strength,
            time_of_influence = EXCLUDED.time_of_influence,
            trend_categories = EXCLUDED.trend_categories,
            analysis = EXCLUDED.analysis,
            analysis_date = EXCLUDED.analysis_date,
            analyzed = FALSE;
    """

    MARK_PROCESSED_SQL = """
        UPDATE articles
        SET processed = TRUE
        WHERE id = %s;
    """

    INSERT_INTO_ARTICLES_SQL = """
        INSERT INTO articles (title, date, url)
        VALUES (%s, %s, %s)
        ON CONFLICT (url) DO NOTHING;
    """

        
