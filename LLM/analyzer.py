import json
import re
from typing import Any

from .prompts import Prompts


class ArticleAnalyzer:
    DIRECTIONS = {"bearish", "neutral", "bullish"}
    SIGNAL_STRENGTHS = {"high", "medium", "low", "none"}
    TIME_OF_INFLUENCE = {"within year", "2-5 years", "more than 5 years"}

    def __init__(self, client, prompts: Prompts | None = None) -> None:
        self.client = client
        self.prompts = prompts or Prompts()

    @staticmethod
    def extract_json_array(text: str) -> list[dict[str, Any]]:
        cleaned = text.strip()

        if cleaned.startswith("```"):
            cleaned = re.sub(r"^```(?:json)?", "", cleaned, flags=re.IGNORECASE).strip()
            cleaned = re.sub(r"```$", "", cleaned).strip()

        try:
            parsed = json.loads(cleaned)
        except json.JSONDecodeError:
            match = re.search(r"\[[\s\S]*\]", cleaned)
            if not match:
                raise
            parsed = json.loads(match.group(0))

        if not isinstance(parsed, list):
            raise ValueError("LLM returned JSON, but not a JSON array.")

        return parsed

    @staticmethod
    def normalize_bool(value: Any, default: bool = False) -> bool:
        if isinstance(value, bool):
            return value
        if isinstance(value, str):
            normalized = value.strip().lower()
            if normalized in {"true", "yes", "1"}:
                return True
            if normalized in {"false", "no", "0"}:
                return False
        if value is None:
            return default
        return bool(value)

    @staticmethod
    def normalize_confidence(value: Any) -> float:
        try:
            confidence = float(value)
        except (TypeError, ValueError):
            return 0.0

        return max(0.0, min(confidence, 1.0))

    @staticmethod
    def normalize_theme(value: Any) -> str:
        words = str(value or "unclassified").strip().split()
        if not words:
            return "unclassified"
        return " ".join(words[:5]).lower()[:100]

    @classmethod
    def normalize_direction(cls, value: Any) -> str:
        direction = str(value or "neutral").strip().lower()
        aliases = {
            "positive": "bullish",
            "negative": "bearish",
            "mixed": "neutral",
            "unclear": "neutral",
        }
        direction = aliases.get(direction, direction)
        if direction not in cls.DIRECTIONS:
            return "neutral"
        return direction

    @classmethod
    def normalize_signal_strength(cls, value: Any, market_relevant: bool) -> str:
        signal_strength = str(value or "none").strip().lower()
        if signal_strength not in cls.SIGNAL_STRENGTHS:
            signal_strength = "low" if market_relevant else "none"
        return signal_strength

    @classmethod
    def normalize_time_of_influence(cls, value: Any) -> str:
        time_of_influence = str(value or "within year").strip().lower()
        aliases = {
            "under 1 year": "within year",
            "less than 1 year": "within year",
            "1 year": "within year",
            "one year": "within year",
            "2 to 5 years": "2-5 years",
            "two to five years": "2-5 years",
            "over 5 years": "more than 5 years",
            "5+ years": "more than 5 years",
        }
        time_of_influence = aliases.get(time_of_influence, time_of_influence)
        if time_of_influence not in cls.TIME_OF_INFLUENCE:
            return "not specified"
        return time_of_influence

    @staticmethod
    def normalize_trend_categories(value: Any) -> list[str]:
        trend_categories = value
        if not isinstance(trend_categories, list):
            return []

        normalized_categories = []
        seen = set()
        for category in trend_categories:
            normalized = str(category).strip().lower()[:60]
            if normalized and normalized not in seen:
                seen.add(normalized)
                normalized_categories.append(normalized)

        return normalized_categories[:12]

    @classmethod
    def normalize_analysis(cls, raw: dict[str, Any], article: dict[str, Any]) -> dict[str, Any]:
        market_relevant = cls.normalize_bool(raw.get("market_relevant", False))
        north_american_impact = cls.normalize_bool(raw.get("north_american_impact", False))
        confidence = cls.normalize_confidence(raw.get("confidence", 0.0))
        theme = cls.normalize_theme(raw.get("theme"))
        direction = cls.normalize_direction(raw.get("direction"))
        signal_strength = cls.normalize_signal_strength(raw.get("signal_strength"), market_relevant)
        time_of_influence = cls.normalize_time_of_influence(raw.get("time_of_influence"))
        trend_categories = cls.normalize_trend_categories(raw.get("trend_categories", []))

        reason = str(raw.get("reason", "")).strip()

        return {
            "id": article["id"],
            "title": article["title"],
            "url": article["url"],
            "theme": theme,
            "direction": direction,
            "market_relevant": market_relevant,
            "north_american_impact": north_american_impact,
            "confidence": confidence,
            "signal_strength": signal_strength,
            "time_of_influence": time_of_influence,
            "trend_categories": trend_categories,
            "reason": reason[:300],
        }

    def classify_headlines(self, articles: list[dict[str, Any]]) -> list[dict[str, Any]]:
        headline_payload = [
            {
                "id": article["id"],
                "title": article["title"],
            }
            for article in articles
        ]
        content = self.client.classify_batch(self.prompts, headline_payload)

        raw_results = self.extract_json_array(content)
        articles_by_id = {article["id"]: article for article in articles}

        normalized_results = []
        for raw in raw_results:
            if not isinstance(raw, dict):
                continue
            try:
                article_id = int(raw.get("id"))
            except (TypeError, ValueError):
                continue
            if article_id not in articles_by_id:
                continue
            normalized_results.append(self.normalize_analysis(raw, articles_by_id[article_id]))

        normalized_article_ids = {result["id"] for result in normalized_results}
        missing_articles = [
            article for article in articles
            if article["id"] not in normalized_article_ids
        ]
        if missing_articles:
            raise ValueError(
                "LLM response did not include every requested article id: "
                + ", ".join(str(article["id"]) for article in missing_articles)
            )

        return normalized_results

