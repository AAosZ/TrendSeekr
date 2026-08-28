import math
import os
import re
from dataclasses import dataclass
from typing import Any

import spacy
from llama_cpp import Llama

from config import Config
from LLM.prompts import Prompts
from PostgreDB.queries import Queries


@dataclass(frozen=True)
class EntityCandidate:
    entity_name: str
    entity_type: str


class EmbeddingClient:
    def __init__(
        self,
        config: Config,
        prompts: Prompts | None = None,
    ) -> None:
        self.config = config
        self.prompts = prompts or Prompts()
        self.model = None

    def load_model(self) -> Llama:
        if not os.path.exists(self.config.EMBEDDING_MODEL_PATH):
            raise FileNotFoundError(
                "Embedding model file not found: "
                f"{self.config.EMBEDDING_MODEL_PATH}. Set NEWS_EMBEDDING_MODEL_PATH "
                "to a GGUF embedding model."
            )

        self.model = Llama(
            model_path=self.config.EMBEDDING_MODEL_PATH,
            embedding=True,
            n_ctx=self.config.N_CTX,
            n_gpu_layers=self.config.N_GPU_LAYERS,
            n_threads=self.config.N_THREADS,
            verbose=False,
        )
        return self.model

    def embed_entity(self, candidate: EntityCandidate) -> list[float]:
        if self.model is None:
            self.load_model()

        prompt = self.prompts.EMBEDDING_PROMPT_TEMPLATE.format(
            entity_type=candidate.entity_type,
            entity_text=candidate.entity_name,
        ).strip()
        response = self.model.create_embedding(input=prompt)
        embedding = response["data"][0]["embedding"]

        if len(embedding) != self.config.EMBEDDING_DIMENSION:

            raise ValueError(
                "Embedding dimension mismatch. "
                f"Expected {self.config.EMBEDDING_DIMENSION}, got {len(embedding)}."
            )

        return [float(value) for value in embedding]


class AnalyticsEngine:
    ENTITY_LABELS = {
        "ORG",
        "PRODUCT",
        "GPE",
        "LOC",
        "FAC",
        "EVENT",
        "LAW",
        "NORP",
        "PERSON",
        "WORK_OF_ART",
    }
    ACTION_OBJECT_DEPS = {"dobj", "obj", "attr", "oprd", "xcomp", "ccomp"}
    PREP_OBJECT_DEPS = {"pobj", "obj"}

    def __init__(
        self,
        config: Config,
        embedding_client: EmbeddingClient | None = None,
    ) -> None:
        self.config = config
        self.queries = Queries()
        self.embedding_client = embedding_client or EmbeddingClient(config)
        self.nlp = None

        if self.config.ANALYTICS_BATCH_SIZE < 1:
            raise ValueError("ANALYTICS_BATCH_SIZE must be at least 1.")
        if not 0 <= self.config.ENTITY_SIMILARITY_THRESHOLD <= 1:
            raise ValueError("ENTITY_SIMILARITY_THRESHOLD must be between 0 and 1.")

    def load_spacy(self):
        if self.nlp is not None:
            return self.nlp

        try:
            self.nlp = spacy.load(self.config.SPACY_MODEL)
        except OSError as exc:
            raise OSError(
                f"spaCy model '{self.config.SPACY_MODEL}' is not installed. "
                "Install it before running analytics."
            ) from exc

        return self.nlp

    def ensure_schema(self, connection) -> None:
        with connection.cursor() as cursor:
            cursor.execute(self.queries.CREATE_VECTOR_EXTENSION_SQL)
            cursor.execute(self.queries.CREATE_ENTITIES_TABLE_SQL)
            cursor.execute(self.queries.CREATE_ARTICLE_ENTITIES_TABLE_SQL)
            cursor.execute(self.queries.CREATE_ENTITIES_NAME_TYPE_INDEX_SQL)
            cursor.execute(self.queries.CREATE_ENTITIES_EMBEDDING_INDEX_SQL)
        connection.commit()

    def fetch_pending_analyses(self, connection) -> list[dict[str, Any]]:
        with connection.cursor() as cursor:
            cursor.execute(
                self.queries.FETCH_ANALYSIS_FOR_ANALYTICS_SQL,
                (self.config.ANALYTICS_BATCH_SIZE,),
            )
            rows = cursor.fetchall()

        return [
            {
                "article_id": article_id,
                "title": title or "",
                "url": url or "",
                "theme": theme or "",
                "trend_categories": trend_categories or [],
                "reason": reason or "",
            }
            for article_id, title, url, theme, trend_categories, reason in rows
        ]

    @staticmethod
    def normalize_entity_name(text: str) -> str:
        normalized = str(text or "").strip().lower()
        normalized = re.sub(r"\s+", " ", normalized)
        normalized = re.sub(r"^[^\w&+.-]+|[^\w&+.-]+$", "", normalized)
        return normalized[:120]

    @staticmethod
    def is_useful_entity_name(text: str) -> bool:
        if len(text) < 2:
            return False
        if text.isnumeric():
            return False
        if len(text.split()) > 8:
            return False
        return True

    def add_candidate(
        self,
        candidates: list[EntityCandidate],
        seen: set[str],
        entity_name: str,
        entity_type: str,
    ) -> None:
        normalized = self.normalize_entity_name(entity_name)
        if not self.is_useful_entity_name(normalized):
            return
        if normalized in seen:
            return

        seen.add(normalized)
        candidates.append(
            EntityCandidate(
                entity_name=normalized,
                entity_type=entity_type,
            )
        )

    def extract_candidates(self, article: dict[str, Any]) -> list[EntityCandidate]:
        candidates: list[EntityCandidate] = []
        seen: set[str] = set()

        self.add_candidate(candidates, seen, article["theme"], "theme")
        for category in article["trend_categories"]:
            self.add_candidate(candidates, seen, category, "trend_category")

        nlp = self.load_spacy()
        for text in (article["title"], article["reason"]):
            if not text.strip():
                continue
            doc = nlp(text)
            self.extract_keyword_candidates(doc, candidates, seen)
            self.extract_action_candidates(doc, candidates, seen)

        return candidates

    def extract_keyword_candidates(self, doc, candidates: list[EntityCandidate], seen: set[str]) -> None:
        for entity in doc.ents:
            if entity.label_ in self.ENTITY_LABELS:
                self.add_candidate(candidates, seen, entity.text, "extracted_keyword")

        for chunk in doc.noun_chunks:
            if not any(token.pos_ in {"NOUN", "PROPN"} for token in chunk):
                continue

            meaningful_tokens = [
                token.text
                for token in chunk
                if not token.is_stop and not token.is_punct and not token.like_num
            ]
            if not meaningful_tokens:
                continue

            self.add_candidate(
                candidates,
                seen,
                " ".join(meaningful_tokens),
                "extracted_keyword",
            )

    def extract_action_candidates(self, doc, candidates: list[EntityCandidate], seen: set[str]) -> None:
        for token in doc:
            if token.pos_ != "VERB" or token.is_stop:
                continue

            for child in token.children:
                if child.dep_ in self.ACTION_OBJECT_DEPS:
                    self.add_action_candidate(token, child, candidates, seen)
                    continue

                if child.dep_ == "prep":
                    for grandchild in child.children:
                        if grandchild.dep_ in self.PREP_OBJECT_DEPS:
                            phrase = f"{token.lemma_} {child.text} {self.subtree_text(grandchild)}"
                            self.add_candidate(
                                candidates,
                                seen,
                                phrase,
                                "extracted_action",
                            )

    def add_action_candidate(
        self,
        verb,
        object_token,
        candidates: list[EntityCandidate],
        seen: set[str],
    ) -> None:
        phrase = f"{verb.lemma_} {self.subtree_text(object_token)}"
        self.add_candidate(candidates, seen, phrase, "extracted_action")

    @staticmethod
    def subtree_text(token) -> str:
        subtree = sorted(token.subtree, key=lambda item: item.i)
        return " ".join(item.text for item in subtree if not item.is_punct)

    @staticmethod
    def vector_literal(embedding: list[float]) -> str:
        values = []
        for value in embedding:
            if not math.isfinite(value):
                raise ValueError("Embedding contains a non-finite value.")
            values.append(format(value, ".9g"))
        return "[" + ",".join(values) + "]"

    def find_similar_entity(self, connection, embedding: list[float]) -> dict[str, Any] | None:
        vector = self.vector_literal(embedding)
        with connection.cursor() as cursor:
            cursor.execute(
                self.queries.FIND_SIMILAR_ENTITY_SQL,
                (
                    vector,
                    vector,
                    self.config.ENTITY_SIMILARITY_THRESHOLD,
                    vector,
                ),
            )
            row = cursor.fetchone()

        if not row:
            return None

        entity_id, entity_name, entity_type, cosine_similarity = row
        return {
            "entity_id": entity_id,
            "entity_name": entity_name,
            "entity_type": entity_type,
            "cosine_similarity": float(cosine_similarity),
        }

    def insert_entity(
        self,
        connection,
        candidate: EntityCandidate,
        embedding: list[float],
    ) -> int:
        with connection.cursor() as cursor:
            cursor.execute(
                self.queries.INSERT_ENTITY_SQL,
                (
                    candidate.entity_name,
                    candidate.entity_type,
                    self.vector_literal(embedding),
                ),
            )
            return int(cursor.fetchone()[0])

    def resolve_entity(self, connection, candidate: EntityCandidate) -> int:
        embedding = self.embedding_client.embed_entity(candidate)
        similar_entity = self.find_similar_entity(connection, embedding)
        if similar_entity:
            return int(similar_entity["entity_id"])

        return self.insert_entity(connection, candidate, embedding)

    def tag_article_entity(self, connection, article_id: int, entity_id: int) -> None:
        with connection.cursor() as cursor:
            cursor.execute(
                self.queries.INSERT_ARTICLE_ENTITY_SQL,
                (article_id, entity_id),
            )

    def mark_article_analyzed(self, connection, article_id: int) -> None:
        with connection.cursor() as cursor:
            cursor.execute(self.queries.MARK_ANALYSIS_ANALYZED_SQL, (article_id,))


    def process_article(self, connection, article: dict[str, Any]) -> int:
        candidates = self.extract_candidates(article)
        tagged_entities = 0

        for candidate in candidates:
            entity_id = self.resolve_entity(connection, candidate)
            self.tag_article_entity(connection, article["article_id"], entity_id)
            tagged_entities += 1

        self.mark_article_analyzed(connection, article["article_id"])
        return tagged_entities


    def process_pending_articles(self, connection) -> None:
        self.ensure_schema(connection)
        articles = self.fetch_pending_analyses(connection)
        if not articles:
            print("No unanalyzed North American market-relevant articles found.")
            return

        print(f"Found {len(articles)} articles ready for analytics.")
        for article in articles:
            try:
                tagged_entities = self.process_article(connection, article)
                connection.commit()
                print(
                    f"Tagged article {article['article_id']} with "
                    f"{tagged_entities} entity candidates."
                )
            except Exception as exc:
                connection.rollback()
                print(f"Failed analytics for article {article['article_id']}: {exc}")
