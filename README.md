# DocuNova Boilerplate

DocuNova is an evidence-first, multimodal document intelligence and learning workspace. This repository provides a clean, production-grade starter boilerplate designed for collaborative team development.

It preserves the system architecture, technology stack, directory organization, dependencies, configuration patterns, API contracts, and integration interfaces, while providing modular scaffolding for team members to implement assigned features.

---

## 1. Technology Stack

- **Backend**:
  - [FastAPI](https://fastapi.tiangolo.com/): Asynchronous REST API framework with lifespan management and CORS middleware.
  - [Pydantic v2](https://docs.pydantic.dev/): Strict data validation, schema enforcement, and settings management.
  - [SQLite](https://sqlite.org/): ACID-compliant local metadata and learning artifact persistence.
  - [Qdrant](https://qdrant.tech/): Vector search engine for evidence chunk embeddings (isolated Docker container on port `6337`).
  - [NVIDIA NIM](https://build.nvidia.com/): Cloud inference for embeddings (`nemotron-3-embed-1b`), reasoning synthesis (`nemotron-3-ultra-550b`), and reranking.
  - [Tesseract 5](https://github.com/tesseract-ocr/tesseract): Native OCR engine for local text extraction from images and scanned PDFs.
  - [PyMuPDF](https://pymupdf.readthedocs.io/) & [python-docx](https://python-docx.readthedocs.io/): Document parsing libraries.
  - [rank-bm25](https://github.com/dorianbrown/rank_bm25): Lexical keyword search for hybrid fusion.
- **Frontend**:
  - [Next.js 15 (App Router)](https://nextjs.org/): React server and client components.
  - [React 19](https://react.dev/): Modern UI rendering.
  - [Tailwind CSS v3](https://tailwindcss.com/): Custom design system with light and dark theme tokens.
  - [TypeScript 5.8](https://www.typescriptlang.org/): Full end-to-end type safety.
  - [React Markdown](https://github.com/remarkjs/react-markdown): Formatted evidence and synthesis rendering.
- **Testing & Tooling**:
  - [pytest](https://pytest.org/): Backend test runner with isolated fixtures.
  - [Docker Compose](https://docs.docker.com/compose/): Containerized vector database infrastructure.

---

## 2. Directory Structure

```
DocuNova-Boilerplate/
├── backend/                        # Python backend package
│   ├── api/
│   │   └── fastapi_app.py          # FastAPI application entry point, routes & error handling
│   ├── app/
│   │   └── streamlit_app.py        # Optional administrative / setup interface
│   └── core/
│       ├── agents/                 # Calculation, vision, and routing agents
│       ├── collections/            # Collection management service
│       ├── comparison/             # Document comparison service
│       ├── evaluation/             # RAG evaluation metrics and benchmark evaluator
│       ├── guardrails/             # Citation, verification, contradiction & injection guardrails
│       ├── ingestion/              # Parsers (PDF, DOCX, CSV, TXT, images), chunker, workflow
│       ├── learning/               # Learning generators (KG, flashcards, quizzes, topics, cheat sheet, teach)
│       ├── llm/                    # NVIDIA NIM client integrations (embeddings, reasoning, reranking)
│       ├── retrieval/              # Hybrid retrieval, fusion, reranking, answering service
│       ├── storage/                # SQLite metadata store, document store, Qdrant store
│       ├── bootstrap.py            # Storage directory initialization
│       ├── config.py               # Environment configuration loader
│       ├── observability.py        # Logfire and event tracing instrumentation
│       └── schemas.py              # Shared Pydantic request/response schemas
├── frontend/                       # Next.js frontend application
│   ├── app/
│   │   ├── globals.css             # Tailwind styling and theme variables
│   │   ├── layout.tsx              # Root HTML layout and font configurations
│   │   └── page.tsx                # Main workspace shell with tab routing and state persistence
│   ├── components/
│   │   ├── header.tsx              # App header, active collection banner, theme toggle
│   │   ├── sidebar.tsx             # Collapsible navigation sidebar
│   │   ├── source-doc-selector.tsx # Multi-document scope filter checkboxes
│   │   └── views/                  # Feature views
│   │       ├── chat-view.tsx       # Grounded multi-document chat and citation inspector
│   │       ├── upload-view.tsx     # Drag-and-drop document upload view
│   │       ├── library-view.tsx    # Document library and management view
│   │       ├── knowledge-graph-view.tsx # Concept graph visualization
│   │       ├── flashcards-view.tsx # Active recall flashcards view
│   │       ├── quizzes-view.tsx    # Multiple-choice quizzes and review view
│   │       ├── topic-tree-view.tsx # Hierarchical topic outline view
│   │       ├── cheat-sheet-view.tsx# Synthesized cheat sheet view
│   │       └── teach-me-view.tsx   # 3-tier adaptive lesson reader view
│   ├── lib/
│   │   └── api.ts                  # Typed API client and backend connection functions
│   ├── package.json                # Frontend dependencies and npm scripts
│   ├── tailwind.config.js          # Design tokens and color themes
│   └── tsconfig.json               # TypeScript compiler configuration
├── data/                           # Local storage paths (excluded from Git)
│   ├── documents/                  # Uploaded raw files
│   ├── processed/                  # Intermediate evidence files
│   └── indexes/                    # Local search indexes
├── scripts/                        # Management and verification utilities
│   ├── init_storage.py             # Storage directory and SQLite table initialization
│   └── verify_setup.py             # Environment diagnostic and health check script
├── tests/                          # Automated backend test suite
│   ├── conftest.py                 # Pytest fixtures and isolated configuration
│   ├── test_schemas_and_config.py  # Schema and configuration tests
│   ├── test_storage_init.py        # Database and document storage tests
│   ├── test_api_contracts.py       # FastAPI contract and health check tests
│   └── test_module_scaffolding.py  # Module scaffolding and HTTP 501 tests
├── .env.example                    # Environment variable template with safe placeholders
├── .gitignore                      # Version control exclusion rules
├── docker-compose.yml              # Isolated Qdrant container on port 6337
├── pyproject.toml                  # Python package manifest
├── requirements.txt                # Python dependencies
├── start_backend.ps1               # PowerShell startup script for FastAPI
├── start_frontend.ps1              # PowerShell startup script for Next.js
├── CONTRIBUTING.md                 # Git workflow, coding conventions, and PR guidelines
├── MODULES.md                      # Detailed feature modules and ownership guide
└── README.md                       # This document
```

---

## 3. Prerequisites

Before starting, ensure the following are installed:

1. **Python**: Python 3.11 or newer (`python --version`).
2. **Node.js**: Node.js 18 or newer (`node -v`) with npm (`npm -v`).
3. **Docker**: Docker Desktop (optional for local offline testing, required for vector search).
4. **Tesseract OCR**: Optional native Tesseract 5 binary if OCR for scanned documents is needed.

---

## 4. Setup Instructions

### Step 1: Environment Configuration

Copy the environment configuration template:

```powershell
# In project root:
Copy-Item .env.example .env

# In frontend folder:
Copy-Item frontend\.env.example frontend\.env.local
```

Edit `.env` to configure your credentials:
- **NVIDIA NIM**: Set `NVIDIA_API_KEY=your-key` if you have an active key from [NVIDIA Developer](https://build.nvidia.com/). (The boilerplate operates in offline mode without this key).
- **Qdrant**: Points to `http://localhost:6337` by default.
- **Port Isolation**: Note that Qdrant in this boilerplate uses port **6337** to avoid collisions with any other Qdrant containers running on ports 6333 or 6335.

### Step 2: Install Python Dependencies

Create and activate a virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### Step 3: Install Frontend Dependencies

```powershell
cd frontend
npm install
cd ..
```

### Step 4: Initialize Storage & Verify Environment

Run the initialization script to create the local SQLite schema and storage directories:

```powershell
python scripts/init_storage.py
```

Run the diagnostic script to verify your setup:

```powershell
python scripts/verify_setup.py
```

### Step 5: Start Vector Database (Optional / Recommended)

If Docker Desktop is running, launch the dedicated, isolated Qdrant container:

```bash
docker compose up -d qdrant
```

Verify Qdrant is running:
```powershell
curl http://localhost:6337/healthz
```

---

## 5. Running the Application

### Start the Backend

In a PowerShell terminal:

```powershell
.\start_backend.ps1
```

Or manually:
```powershell
$env:PYTHONPATH = "backend"
python -m uvicorn api.fastapi_app:app --host 0.0.0.0 --port 8000 --reload
```

- API Base: `http://localhost:8000`
- Interactive API Docs (Swagger): `http://localhost:8000/docs`
- Health Check: `http://localhost:8000/health`

### Start the Frontend

In a second PowerShell terminal:

```powershell
.\start_frontend.ps1
```

Or manually:
```powershell
cd frontend
npm run dev
```

- Web Interface: `http://localhost:3000`

---

## 6. Feature Modules & Implementation Status

To enable parallel collaboration, completed features from the reference project have been converted into implementable starter modules with preserved API contracts, request/response schemas, and clear TODOs.

| Module | Assigned Owner | Primary Files | Status |
| :--- | :--- | :--- | :--- |
| **Document Ingestion** | Ingestion Lead | `core/ingestion/pdf.py`, `docx.py`, `csv.py`, `images.py` | 🛠️ Starter Scaffolding (`txt.py` reference works) |
| **Retrieval & Grounded Chat** | AI Reasoning Lead | `core/retrieval/answering.py`, `hybrid.py` | 🛠️ Scaffolding (501 Not Implemented) |
| **Knowledge Graph** | Knowledge Lead | `core/learning/knowledge_graph.py` | 🛠️ Scaffolding (501 Not Implemented) |
| **Active Recall Flashcards**| Education Lead | `core/learning/flashcards.py` | 🛠️ Scaffolding (501 Not Implemented) |
| **Deterministic Quizzes** | Assessment Lead | `core/learning/quizzes.py` | 🛠️ Scaffolding (501 Not Implemented) |
| **Topic Tree & Outline** | Summarization Lead | `core/learning/topic_tree.py` | 🛠️ Scaffolding (501 Not Implemented) |
| **Cheat Sheet Synthesis** | Content Lead | `core/learning/cheat_sheet.py` | 🛠️ Scaffolding (501 Not Implemented) |
| **Teach Me Mode** | Pedagogical Lead | `core/learning/teach_me.py` | 🛠️ Scaffolding (501 Not Implemented) |
| **Shared Foundation & UI** | Full-Stack Lead | `backend/core/storage/`, `frontend/app/` | ✅ Complete Foundation |

For detailed implementation instructions, schemas, and guidelines for each module, see [MODULES.md](file:///d:/DocuNova-Boilerplate/MODULES.md).

---

## 7. Running Tests

Run the automated backend test suite:

```powershell
$env:PYTHONPATH = "backend"
python -m pytest -q
```

Run frontend type checking:

```powershell
cd frontend
npm run lint
cd ..
```

---

## 8. Creating Your Individual GitHub Repository

Each group member should create their own GitHub repository from this boilerplate:

1. Ensure Git is initialized locally in your boilerplate directory:
   ```bash
   git init -b main
   ```
2. Confirm that `.env`, `.venv`, and `node_modules` are excluded:
   ```bash
   git status
   ```
3. Commit the clean boilerplate:
   ```bash
   git add .
   git commit -m "chore: initial commit of DocuNova boilerplate"
   ```
4. Create a new repository on your GitHub account (do not fork the reference repo directly).
5. Add your remote and push:
   ```bash
   git remote add origin https://github.com/<your-username>/DocuNova-<your-feature>.git
   git push -u origin main
   ```

For branching, commit message conventions, and pull request workflows, see [CONTRIBUTING.md](file:///d:/DocuNova-Boilerplate/CONTRIBUTING.md).
