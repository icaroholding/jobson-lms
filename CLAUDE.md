# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Jobson Academy (formerly Frappe LMS) — an open-source Learning Management System built on the **Frappe Framework**. Two-part architecture: Python/Frappe backend + Vue 3 SPA frontend.

- **Backend:** Python 3.10+, Frappe Framework (v15–v17-dev), MariaDB, Redis
- **Frontend:** Vue 3, Frappe UI, Tailwind CSS, Pinia, Vite
- **App name in Frappe:** `frappe_lms` (see `hooks.py`)

## Development Commands

All backend commands require Frappe Bench and must run from the bench directory (parent of `apps/`).

### Backend
```bash
bench start                                          # Start dev server
bench --site <site> install-app lms                  # Install app on site
bench --site <site> migrate                          # Run migrations
bench --site <site> build                            # Build assets
```

### Frontend
```bash
cd frontend
yarn install
yarn dev              # Vite dev server on :8080, proxies to Frappe on :8000
yarn build            # Production build → lms/public/frontend/
```

### Testing
```bash
# All backend tests
bench --site <site> run-tests --app lms

# Single doctype test
bench --site <site> run-tests --module lms.lms.doctype.lms_course.test_lms_course

# With coverage
bench --site <site> run-tests --app lms --coverage

# Cypress E2E (frontend)
npm run test-local                                    # Opens Cypress UI
bench --site <site> run-ui-tests lms --headless       # Headless
```

### Linting
```bash
pre-commit run --all-files    # Runs ruff, prettier, eslint
```

## Code Style

- **Python:** Ruff — tab indentation, double quotes, 110 char line length, target py310
- **JS/Vue:** Prettier — single quotes, no semicolons. ESLint for linting.
- **Commits:** Conventional commits — `feat(scope):`, `fix(scope):`, `docs:`, etc.

## Architecture

### Backend (`lms/`)

Built on **Frappe's doctype pattern** — each business entity is a DocType with auto-generated CRUD, REST API, and admin UI.

Key modules:
- `lms/lms/doctype/` — 40+ doctypes: courses, chapters, lessons, batches, enrollments, quizzes, assignments, certificates, payments, badges
- `lms/hooks.py` — App lifecycle hooks, scheduled tasks, doc events, route rules, markdown macros
- `lms/lms/api.py` — Whitelisted public API endpoints
- `lms/lms/utils.py` — Shared helpers (permissions, notifications, palette)
- `lms/lms/user.py` — User validation and login hooks
- `lms/lms/payments.py` — Payment processing (Razorpay)
- `lms/sqlite.py` — Full-text search indexing via SQLite
- `lms/plugins.py` — Extensibility system for lesson macros and profile tabs
- `lms/overrides/` — Frappe class overrides (e.g., Web Template)
- `lms/patches/` — Database migration scripts (registered in `patches.txt`)
- `lms/fixtures/` — Seed data for Custom Field, Function, Industry, LMS Category

### Frontend (`frontend/src/`)

Vue 3 SPA served at `/lms/` with Frappe as the API backend.

- `pages/` — 40+ route components (courses, batches, lessons, quizzes, profiles, billing, stats)
- `components/` — 54 reusable components organized by domain (Course/, Batch/, Lesson/, Quiz/, Editor/)
- `stores/` — Pinia stores: user, session, settings, course, batch, lesson
- `router.js` — SPA routes, all under `/lms/`
- `utils/` — API wrapper, dialogs, dayjs config, socket.io client
- Content editing uses Editor.js with multiple block types

### Routing

- All frontend routes are under `/lms/<path>` (see `website_route_rules` in hooks.py)
- Legacy routes (`/courses`, `/batches`, etc.) redirect to `/lms/` equivalents via `website_redirects`
- Certificate pages use a separate Jinja template at `/courses/<course>/<cert_id>`

### Key Patterns

- **Doc Events:** Global `on_change` hook processes badges on every doctype change
- **Scheduled Tasks:** Hourly (cert evals, course stats, attendance), daily (job updates, payment reminders, class reminders)
- **Markdown Macros:** Lessons support `Exercise`, `Quiz`, `YouTubeVideo`, `Video`, `Assignment`, `Embed`, `Audio`, `PDF` macros rendered via `lms/plugins.py`
- **Permissions:** Row-level via Frappe + custom `has_website_permission` for certificates
- **Search:** SQLite FTS index rebuilt on every scheduler tick and after migrations
- **Test helpers:** `lms/lms/test_utils.py` provides `new_user()`, `new_course()`, etc.

## Changelog automatico

**Regola obbligatoria:** al termine di ogni sessione di lavoro, prima di concludere, crea (o aggiorna se esiste già) un file markdown nella cartella `changelog/` con il nome `YYYY-MM-DD.md` (data del giorno corrente). La cartella `changelog/` è nel `.gitignore` — è solo un log locale.

Formato del file:

```markdown
# Changelog — YYYY-MM-DD

## Modifiche

- **[tipo]** breve descrizione della modifica (`percorso/file`)
- **[tipo]** breve descrizione della modifica (`percorso/file`)
...
```

Dove `[tipo]` è uno tra: `feat`, `fix`, `refactor`, `docs`, `style`, `chore`, `test`.

Esempio:

```markdown
# Changelog — 2026-04-09

## Modifiche

- **[feat]** aggiunto widget Botpress nella pagina pubblica (`lms/public/js/botpress-widget.js`)
- **[docs]** creato CLAUDE.md con documentazione architettura (`CLAUDE.md`)
- **[chore]** aggiunta cartella changelog al gitignore (`.gitignore`)
```

Se il file del giorno esiste già, aggiungi le nuove voci in fondo alla lista senza sovrascrivere quelle precedenti.
