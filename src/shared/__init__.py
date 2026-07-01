"""Shared cross-feature utilities: audit store and RAG retrieval."""
from .audit import get_record, list_records, update_decision, write_record
from .rag_store import query_manuals

__all__ = [
    "write_record",
    "get_record",
    "list_records",
    "update_decision",
    "query_manuals",
]
