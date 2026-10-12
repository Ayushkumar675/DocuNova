"""Pytest fixtures for DocuNova Boilerplate testing."""

from dataclasses import replace
from pathlib import Path
from types import SimpleNamespace
from uuid import uuid4

import pytest

from core.config import Config, get_config
from core.schemas import DocumentRecord, EvidenceRecord
from core.storage.document_store import DocumentStore
from core.storage.metadata_store import MetadataStore


@pytest.fixture
def temp_config(tmp_path: Path) -> Config:
    """Provide isolated configuration pointing to temporary paths."""
    base_config = get_config()
    db_path = tmp_path / "test_docunova.db"
    doc_path = tmp_path / "documents"
    proc_path = tmp_path / "processed"
    idx_path = tmp_path / "indexes"
    doc_path.mkdir(parents=True, exist_ok=True)
    proc_path.mkdir(parents=True, exist_ok=True)
    idx_path.mkdir(parents=True, exist_ok=True)

    return replace(
        base_config,
        metadata_db_path=str(db_path),
        document_store_path=str(doc_path),
        processed_store_path=str(proc_path),
        index_store_path=str(idx_path),
        qdrant_url="http://localhost:6337",
        qdrant_collection="test_collection",
        retrieval_mode="keyword",
        nvidia_api_key="",
        nvidia_reranker_api_key="",
    )


@pytest.fixture
def test_stores(temp_config: Config):
    """Provide isolated MetadataStore and DocumentStore."""
    metadata_store = MetadataStore(temp_config.metadata_db_path)
    document_store = DocumentStore(temp_config.document_store_path)
    return metadata_store, document_store


@pytest.fixture
def sample_collection_and_evidence(test_stores):
    """Provide a fixture with 1 collection, 1 document, and 1 evidence chunk."""
    metadata_store, document_store = test_stores
    collection = metadata_store.create_collection("Test Collection")

    doc_id = str(uuid4())
    stored_path = document_store.save(collection.id, doc_id, "sample.txt", b"Machine learning models learn patterns from data.")

    doc_record = DocumentRecord(
        id=doc_id,
        collection_id=collection.id,
        filename="sample.txt",
        file_type="txt",
        size=len(b"Machine learning models learn patterns from data."),
        page_count=1,
        status="processed",
        created_at=collection.created_at,
        storage_path=stored_path,
    )
    metadata_store.add_document(doc_record)

    evidence_id = str(uuid4())
    evidence_record = EvidenceRecord(
        evidence_id=evidence_id,
        collection_id=collection.id,
        document_id=doc_id,
        filename="sample.txt",
        page_number=1,
        content_type="TEXT",
        source_reference=f"document:{doc_id}#page=1",
        score=1.0,
        text="Machine learning models learn patterns from data.",
        image_reference=None,
        section="Introduction",
        metadata={"format": "txt"},
    )
    metadata_store.add_evidence(evidence_record)

    return collection, doc_record, evidence_record
