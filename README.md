# Enterprise RAG / Search API — Technical Exercise

## Brief

You have inherited a small **multi-tenant enterprise search & RAG service**. Internal
company documents from several tenants (`acme`, `globex`) are served through a JSON API.
Employees, managers and admins from different tenants share one deployment.

The happy path "works", but the team has open reports of:

- a **data-exposure incident** (a user saw another company's document),
- **wrong / inconsistent search results**,
- **request failures when the model provider is slow or erroring**.

The existing test suite is partly red.

Your job: make the service **correct, safe and reliable** without changing the public
HTTP contract below.

**Time-box: 75 minutes.**

## What you are expected to do

1. Create a virtual environment, install dependencies, run the test suite, and
   reproduce the failures.
2. Read `app/` and follow a request from the API layer through services,
   repositories and providers.
3. Identify the security, correctness and reliability problems.
4. Fix cross-tenant isolation and document-level authorization.
5. Fix retrieval ordering and hybrid (lexical + semantic) ranking.
6. Make provider calls resilient: timeout, bounded retry, and a degraded
   response instead of a 5xx.
7. Add tests for every issue you fix, including a concurrency test.
8. Keep the request/response shapes and status-code semantics of the four
   endpoints unchanged.
9. Run `pytest`, `ruff` and `mypy` — all three must be green.
10. Commit your work as one clean commit.
11. Be ready to explain how you would take this service to production.

## Setup (Windows / CMD)

```
python -m venv .venv
.venv\Scripts\activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Optional — run the API for manual exploration:

```
python -m uvicorn app.main:app --reload
```

## Commands

```
python -m pytest                 :: full suite
python -m pytest -m "not slow"    :: skip provider-hang tests
python -m ruff check .
python -m mypy app
```

## Authentication

There is no real auth. Every request sends an `X-User-Id` header; the caller's
tenant and role are resolved from it.

| user_id | tenant_id | role     |
| ------- | --------- | -------- |
| u-alice | acme      | employee |
| u-bob   | acme      | manager  |
| u-carol | acme      | admin    |
| u-dave  | globex    | employee |
| u-erin  | globex    | manager  |
| u-frank | globex    | admin    |

## API contract

### `GET /documents/{document_id}`

- `200` — `{ document_id, tenant_id, owner_id, visibility, content, metadata }`
- `401` — missing / unknown `X-User-Id`
- `403` — caller may not read this document
- `404` — no such document for this caller

Visibility: `public` / `tenant` — any user **in the document's tenant**;
`private` — only the owner. A document is never visible outside its own tenant.

### `POST /search`

Body: `{ "query": <non-empty string>, "top_k": <int 1..50, default 5> }`

- `200` — `{ "hits": [ { "document_id", "score", "snippet" } ], "cached": bool }`
- `401` — missing / unknown `X-User-Id`
- `422` — invalid body

Hits are unique by `document_id`, ordered by **descending** relevance, and limited
to documents the caller may read in the caller's tenant. Hybrid ranking must
combine lexical and semantic signals on a comparable scale.

### `POST /answer`

Body: `{ "query": <non-empty string>, "top_k": <int 1..50, default 5> }`

- `200` — `{ "answer": string, "sources": [ SearchHit ], "degraded": bool }`
- `401` — missing / unknown `X-User-Id`
- `422` — invalid body

If the model provider errors or is too slow, return `200` with `degraded=true`
and whatever sources were retrieved — never a 5xx.

### `GET /admin/audit-logs`

- `200` — `{ "logs": [ { log_id, tenant_id, user_id, action, target_id, timestamp } ] }`,
  scoped to the caller's tenant
- `401` — missing / unknown `X-User-Id`
- `403` — caller is not an admin

## Acceptance criteria

- [ ] No request can read data outside the caller's tenant, including under
      concurrent load.
- [ ] Document-level authorization is enforced for every visibility level.
- [ ] Search results are de-duplicated and ordered best-first; lexical and
      semantic scores are combined on a comparable scale.
- [ ] `/answer` degrades gracefully on provider failure or timeout.
- [ ] Invalid input (empty query, out-of-range `top_k`, mismatched tenant) is
      rejected with `422`.
- [ ] Distinct failure causes map to distinct status codes.
- [ ] `pytest`, `ruff check` and `mypy` all pass.
- [ ] New tests cover isolation, authorization, ranking, validation and provider
      failure, plus a concurrency test.
- [ ] The four endpoints keep their documented request/response shapes.
- [ ] One commit, clear message.
