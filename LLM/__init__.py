"""
LLM package for TrendSeekr
"""

__all__ = ["ArticleAnalyzer", "Client", "Processor", "Prompts"]


def __getattr__(name):
    if name == "ArticleAnalyzer":
        from .analyzer import ArticleAnalyzer

        return ArticleAnalyzer
    if name == "Client":
        from .client import Client

        return Client
    if name == "Processor":
        from .processor import Processor

        return Processor
    if name == "Prompts":
        from .prompts import Prompts

        return Prompts
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
