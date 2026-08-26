"""
Analytics package for TrendSeekr.
"""

__all__ = ["AnalyticsEngine", "EmbeddingClient", "EntityCandidate"]


def __getattr__(name):
    if name == "AnalyticsEngine":
        from .analytics_engine import AnalyticsEngine

        return AnalyticsEngine
    if name == "EmbeddingClient":
        from .analytics_engine import EmbeddingClient

        return EmbeddingClient
    if name == "EntityCandidate":
        from .analytics_engine import EntityCandidate

        return EntityCandidate
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
