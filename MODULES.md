# DocuNova Boilerplate — Feature Modules & Ownership Guide

This document defines the architectural boundaries, responsibilities, API contracts, and suggested ownership for each feature module in DocuNova. Team members can take ownership of specific modules and develop them independently in their own GitHub forks/branches.

---

## Architectural Overview

```
Frontend (Next.js 15 App Router)
  ├── Components: Navigation, Header, Source Document Selector
  ├── Views: Chat, Upload/Library, Knowledge Graph, Flashcards, Quizzes, Topic Tree, Cheat Sheet, Teach Me
  └── API Client: lib/api.ts
        ↕ REST API (HTTP / JSON / Form-Data)
FastAPI Backend (backend/api/fastapi_app.py)
  ├── Ingestion & Collections Pipeline (backend/core/ingestion/, backend/core/collections/)
  ├── Hybrid Retrieval & Grounded Answering (backend/core/retrieval/, backend/core/guardrails/)
  ├── Learning Workspace Generators (backend/core/learning/)
  └── Storage & Vector Indexing (backend/core/storage/ - SQLite & Qdrant)
```

---

## Module Catalog

### Module 1: Document Ingestion & Document Management
- **Suggested Owner**: Backend / Data Engineering Lead
- **Primary Backend Files**:
  - `backend/core/ingestion/loader.py`: Ingestion loader and file parser dispatcher.
  - `backend/core/ingestion/chunker.py`: Text chunking algorithm with source preservation.
  - `backend/core/ingestion/pdf.py`: PDF text, table, and OCR extraction.
  - `backend/core/ingestion/docx.py`: DOCX paragraph and table extraction.
  - `backend/core/ingestion/csv.py`: CSV batch row parsing with column header preservation.
  - `backend/core/ingestion/images.py`: Image OCR and visual inference.
  - `backend/core/ingestion/txt.py`: Reference text/markdown parser (already implemented as baseline).
- **Primary Frontend Files**:
  - `frontend/components/views/upload-view.tsx`: Drag-and-drop file upload zone.
  - `frontend/components/views/library-view.tsx`: Document management and deletion view.
- **Responsibilities**:
  1. Accept uploaded multi-file documents (PDF, DOCX, TXT, CSV, PNG, JPG).
  2. Parse raw files into typed `ParsedItem` records (`TEXT`, `TABLE`, `OCR`, `IMAGE`).
  3. Deterministically chunk parsed items into `EvidenceRecord` items preserving collection ID, document ID, page numbers, and row numbers.
  4. Store metadata in SQLite and raw bytes in `data/documents/` under secure UUIDs.
- **Key API Endpoints**:
  - `POST /collections/{id}/documents` (Multi-part file upload)
  - `GET /collections/{id}/documents` (List documents)
  - `POST /collections/{id}/prepare` (Background parsing and indexing job)
  - `GET /collections/{id}/ingestion` (Job status)
  - `DELETE /collections/{id}/documents/{doc_id}` (Delete document and clean vectors)

---

### Module 2: Retrieval, Multi-Document Chat, and Citations
- **Suggested Owner**: NLP / AI Reasoning Lead
- **Primary Backend Files**:
  - `backend/core/retrieval/answering.py`: `GroundedAnswerService` implementation.
  - `backend/core/retrieval/hybrid.py`: Hybrid BM25 keyword and vector retriever.
  - `backend/core/retrieval/context.py`: Context bounding and formatting.
  - `backend/core/guardrails/citations.py`: Citation validation (`[evidence:ID]`).
  - `backend/core/guardrails/verification.py`: Claim extraction and verification.
  - `backend/core/guardrails/contradictions.py`: Cross-document contradiction detection.
- **Primary Frontend Files**:
  - `frontend/components/views/chat-view.tsx`: Chat interface, markdown answer rendering, citation popovers, and contradiction alerts.
- **Responsibilities**:
  1. Query retrieval pipeline enforcing collection and selected-document scope.
  2. Bounded context construction with prompt injection protection.
  3. NVIDIA NIM reasoning structured prompt synthesis.
  4. Ensure every factual claim is cited with explicit evidence references.
  5. Validate citations and surface ungrounded or contradictory claims.
- **Key API Endpoints**:
  - `POST /collections/{id}/query` (`QueryRequest` -> `QueryResponse`)
  - `GET /query/guardrails`
  - `GET /collections/{id}/contradictions`

---

### Module 3: Knowledge Graph Generation
- **Suggested Owner**: Graph / Knowledge Engineering Lead
- **Primary Backend Files**:
  - `backend/core/learning/knowledge_graph.py`: `generate_knowledge_graph(...)`
  - `backend/core/learning/models.py`: `KnowledgeGraphContent`, `KnowledgeGraphNode`, `KnowledgeGraphEdge`
- **Primary Frontend Files**:
  - `frontend/components/views/knowledge-graph-view.tsx`: Interactive SVG concept tree/radial graph, entity directory, node inspector, and search.
- **Responsibilities**:
  1. Retrieve relevant evidence passages for a user topic or general collection overview.
  2. Prompt NVIDIA reasoning NIM to extract core entities (nodes) and directed relationships (edges).
  3. Label each relationship as `explicit` or `inferred`.
  4. Ensure all nodes and edges carry valid `source_evidence_ids`.
- **Key API Endpoints**:
  - `POST /learning/knowledge-graph` (`GenerateRequest` -> `LearningArtifact`)
  - `GET /learning/knowledge-graph/{id}`

---

### Module 4: Active Recall Flashcards Generation
- **Suggested Owner**: Educational Features Lead
- **Primary Backend Files**:
  - `backend/core/learning/flashcards.py`: `generate_flashcards(...)`
  - `backend/core/learning/models.py`: `FlashcardDeckContent`, `Flashcard`
- **Primary Frontend Files**:
  - `frontend/components/views/flashcards-view.tsx`: 3D card flip animations, active recall rating (again, hard, good, easy), batch distribution.
- **Responsibilities**:
  1. Generate distinct active-recall questions with concise answers and explanations.
  2. Prevent answers from being revealed inside question text.
  3. Distribute questions across easy, medium, and hard difficulty tiers.
  4. Ensure each card cites genuine source evidence IDs.
- **Key API Endpoints**:
  - `POST /learning/flashcards/generate`
  - `GET /learning/flashcards/{deck_id}`

---

### Module 5: Deterministic Quizzes & Understanding Checks
- **Suggested Owner**: Assessment & Evaluation Lead
- **Primary Backend Files**:
  - `backend/core/learning/quizzes.py`: `generate_quiz(...)`, `evaluate_quiz_submission(...)`
  - `backend/core/learning/models.py`: `QuizContent`, `Question`, `SubmitRequest`
- **Primary Frontend Files**:
  - `frontend/components/views/quizzes-view.tsx`: Interactive quiz taker, timer, progress bar, instant grading review, source evidence drawer.
- **Responsibilities**:
  1. Generate multiple-choice questions (4 options: 1 correct + 3 plausible distractors) or True/False questions.
  2. Conceal correct answers and explanations until user submits.
  3. Deterministically evaluate answers on backend and calculate score and percentage.
  4. Return detailed question-by-question review with source evidence citations.
- **Key API Endpoints**:
  - `POST /learning/quizzes/generate`
  - `POST /learning/quizzes/{quiz_id}/submit`

---

### Module 6: Topic Tree & Hierarchical Summary
- **Suggested Owner**: Document Structure & Summarization Lead
- **Primary Backend Files**:
  - `backend/core/learning/topic_tree.py`: `generate_topic_tree(...)`
  - `backend/core/learning/models.py`: `TopicTreeContent`, `TopicNode`
- **Primary Frontend Files**:
  - `frontend/components/views/topic-tree-view.tsx`: Expandable tree hierarchy, breadcrumbs, section summaries, citation badges.
- **Responsibilities**:
  1. Build bounded expandable topic/subtopic outline hierarchy.
  2. Preserve original source section headings when present.
  3. Prevent cyclic parent-child references.
  4. Ensure each node carries concise evidence-grounded summary facts.
- **Key API Endpoints**:
  - `POST /learning/topic-tree`

---

### Module 7: Synthesized Cheat Sheet
- **Suggested Owner**: Content Synthesis Lead
- **Primary Backend Files**:
  - `backend/core/learning/cheat_sheet.py`: `generate_cheat_sheet(...)`
  - `backend/core/learning/models.py`: `CheatSheetContent`, `CheatSheetSection`
- **Primary Frontend Files**:
  - `frontend/components/views/cheat-sheet-view.tsx`: Format selector tabs, markdown table rendering, formula cards, copy-to-clipboard, export.
- **Responsibilities**:
  1. Support 6 distinct formats: `quick_revision`, `key_concepts`, `formula_sheet`, `comparison_table`, `exam_outline`, `last_minute`.
  2. For formula sheets: extract verbatim formulas with units and conditions without fabricating numbers.
  3. For comparison tables: generate valid markdown comparison tables.
  4. Ensure all sections cite evidence IDs.
- **Key API Endpoints**:
  - `POST /learning/cheat-sheet`

---

### Module 8: Teach Me Mode (Adaptive 3-Tier Lessons)
- **Suggested Owner**: Pedagogical Systems Lead
- **Primary Backend Files**:
  - `backend/core/learning/teach_me.py`: `generate_lesson(...)`, `evaluate_lesson_answer(...)`
  - `backend/core/learning/models.py`: `TeachLessonContent`, `TeachAnswerRequest`
- **Primary Frontend Files**:
  - `frontend/components/views/teach-me-view.tsx`: Adaptive tier switcher, progressive lesson reader, worked examples, interactive check with feedback.
- **Responsibilities**:
  1. Generate lessons tailored to three depth tiers:
     - **Beginner**: Intuitive definition, plain analogy, explained jargon, simple recall check.
     - **Intermediate**: Formal mechanisms, terminology, worked source example, application check.
     - **Advanced**: Assumptions, trade-offs, limitations, mathematical derivation or edge cases, reasoning check.
  2. Evaluate interactive comprehension checks and adaptively progress user.
- **Key API Endpoints**:
  - `POST /learning/teach`
  - `POST /learning/teach/{session_id}/answer`

---

### Module 9: Frontend & Backend Integration
- **Suggested Owner**: Full-Stack Integration Lead
- **Primary Files**:
  - `frontend/lib/api.ts`: Typed REST client functions, headers, error unwrapping.
  - `frontend/app/page.tsx`: Workspace tab routing, theme persistence, collection loading, reactive status polling.
  - `backend/api/fastapi_app.py`: Lifespan event, CORS configuration, request tracing, unified HTTP 501 error handling.
- **Responsibilities**:
  1. Ensure all frontend calls handle errors cleanly and display appropriate status messages.
  2. Ensure theme toggle (light/dark) works consistently across all views.
  3. Handle multi-document scope selection reactively.

---

### Module 10: Testing, Validation & Application Integration
- **Suggested Owner**: QA & DevOps Lead
- **Primary Files**:
  - `tests/`: Automated pytest test suite.
  - `scripts/init_storage.py`: Storage setup script.
  - `scripts/verify_setup.py`: Environment diagnostics script.
  - `docker-compose.yml`: Isolated Qdrant container and volume.
- **Responsibilities**:
  1. Verify offline tests pass with zero network dependency.
  2. Validate Pydantic schemas and configuration loading.
  3. Ensure Docker containers use separate ports (6337) and volumes (`docunova_boilerplate_qdrant_data`).
  4. Maintain CI/CD workflows and regression suites.
