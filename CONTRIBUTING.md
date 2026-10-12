# DocuNova Boilerplate — Contributing Guidelines

Welcome to the team! This guide establishes standards, workflows, and conventions to ensure clean collaboration across all team members and their respective GitHub repositories.

---

## 1. Git Workflow & Repository Setup

### Initializing Your Personal Repository
Each group member should work from their own Git repository derived from this boilerplate:

```bash
# 1. Initialize Git in your project folder
git init -b main

# 2. Verify that .gitignore is respected (no secrets or node_modules)
git status

# 3. Create your initial commit
git add .
git commit -m "chore: initialize DocuNova starter boilerplate"

# 4. Link to your personal GitHub repository
git remote add origin https://github.com/<your-username>/<your-repo-name>.git
git push -u origin main
```

> [!IMPORTANT]
> Never copy Git metadata from other repositories or modify another member's repository directly. Each member must commit and push their own work under their own GitHub account.

---

## 2. Branching Conventions

When implementing assigned modules or fixes, create focused feature branches:

| Branch Type | Format | Example |
| :--- | :--- | :--- |
| **Feature** | `feature/<module-name>` | `feature/knowledge-graph`, `feature/pdf-ingestion` |
| **Bugfix** | `fix/<description>` | `fix/citation-regex`, `fix/quiz-timer` |
| **Refactor** | `refactor/<module-name>` | `refactor/hybrid-retriever` |
| **Documentation** | `docs/<description>` | `docs/api-specs` |
| **Testing** | `test/<module-name>` | `test/flashcards-unit` |

---

## 3. Commit Message Conventions

Follow the [Conventional Commits](https://www.conventionalcommits.org/) format:

```text
<type>(<scope>): <short description>

[optional body explaining rationale]
```

### Allowed Types:
- `feat`: A new feature implementation for an assigned module.
- `fix`: A bug fix or patch.
- `docs`: Documentation updates.
- `refactor`: Code changes that neither fix a bug nor add a feature.
- `test`: Adding or correcting tests.
- `chore`: Build scripts, dependencies, or tool configuration.

### Examples:
- `feat(ingestion): implement PDF text and table extraction using pymupdf`
- `feat(quizzes): implement deterministic scoring and review formatting`
- `fix(retrieval): prevent out-of-scope document IDs in vector search`
- `test(learning): add unit tests for topic tree cycle prevention`

---

## 4. Coding Standards

### Python (Backend)
- **Version**: Python 3.11+.
- **Style**: Follow PEP 8 guidelines.
- **Type Annotations**: All public functions and service methods must include complete type annotations.
- **Data Validation**: Use Pydantic v2 schemas (`pydantic.BaseModel`) for request/response payloads.
- **Error Handling**: Use explicit, custom exceptions or standard `HTTPException` with clear error details. Never silently pass errors or swallow exceptions.
- **Module Boundaries**: Place your business logic in the dedicated module file in `backend/core/learning/` or `backend/core/ingestion/` as specified in [MODULES.md](file:///d:/DocuNova-Boilerplate/MODULES.md).

### TypeScript / Next.js (Frontend)
- **Version**: Next.js 15 (App Router), React 19, TypeScript 5.8+.
- **Type Safety**: Maintain strict TypeScript typing. Avoid `any` where a concrete type exists in `frontend/lib/api.ts`.
- **Styling**: Use Tailwind CSS utility classes. Adhere to design tokens in `tailwind.config.js` and support both light and dark modes (`dark:` variants).
- **Component Design**: Keep views modular and responsive. Always provide loading spinners, empty states, and error alerts.

---

## 5. Security & Secrets Policy

> [!CAUTION]
> Never commit actual API keys, passwords, database credentials, or private documents to version control.

1. **Environment Variables**:
   - Store all private settings in `.env` (backend) and `.env.local` (frontend).
   - Both are excluded by `.gitignore`.
   - Update `.env.example` with safe placeholder variable names when introducing new configuration requirements.
2. **Provider Key Masking**:
   - Never log credentials in console output, Logfire spans, or API response bodies.
   - Provider status endpoints must only report boolean presence (`configured: true/false`).
3. **Data Protection**:
   - Do not upload sensitive identity documents, API keys, or private datasets into shared test suites.

---

## 6. Pre-Commit Verification Checklist

Before creating a pull request or submitting your repository, verify that:

- [ ] All automated Python tests pass:
  ```bash
  python -m pytest -q
  ```
- [ ] Frontend type check and build pass without errors:
  ```bash
  cd frontend
  npm run lint
  npm run build
  cd ..
  ```
- [ ] Environment verification script succeeds:
  ```bash
  python scripts/verify_setup.py
  ```
- [ ] Storage initialization script succeeds without error:
  ```bash
  python scripts/init_storage.py
  ```
- [ ] No `.env`, database (`.db`), or temporary test artifacts are staged in `git status`.
