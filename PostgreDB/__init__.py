"""
Database package for TrendSeekr
"""

__all__ = ["DatabaseConnection", "Queries"]


def __getattr__(name):
    if name == "DatabaseConnection":
        from .connection import DatabaseConnection

        return DatabaseConnection
    if name == "Queries":
        from .queries import Queries

        return Queries
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
