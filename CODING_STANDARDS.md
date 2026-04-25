# Coding Standards & AI Instruction File — Research-Backed Draft

*Compiled by Sam · Sources: PEP 8/20/257/484/526, Google Python Style Guide, OWASP SCP, Conventional Commits 1.0.0, WCAG 2.1, structlog docs, mypy/ruff/black docs, and web research (2024–2025). All claims attributed below.*

---

## Table of Contents

1. [Universal Principles](#1-universal-principles)
2. [Python Standards](#2-python-standards)
3. [JavaScript / Web Standards](#3-javascript--web-standards)
4. [Security Standards](#4-security-standards)
5. [Git & Workflow Standards](#5-git--workflow-standards)
6. [AI Instruction File Hygiene](#6-ai-instruction-file-hygiene)
7. [Architecture & Design Principles](#7-architecture--design-principles)

---

## 1. Universal Principles

*(Language-agnostic; applies to all code in all contexts.)*

### 1.1 Readability Is the Primary Virtue

> "Code is read much more often than it is written." — Guido van Rossum, PEP 8 [[1]](https://peps.python.org/pep-0008/)

- Write code for the next reader, not for the machine.
- Clarity beats cleverness. If you need a comment to explain what the code does, consider rewriting the code instead.
- Prefer explicit over implicit. Name the thing; don't make the reader infer it.

### 1.2 Naming Conventions

These rules apply regardless of language (defer to language-specific casing conventions):

| Thing | Rule |
|---|---|
| **Variables** | Reveal intent: `user_count` not `n`; `is_active` not `flag` |
| **Functions/methods** | Verb phrases: `get_user`, `validate_token`, `send_email` |
| **Booleans** | Question form: `is_valid`, `has_permission`, `can_retry` |
| **Classes** | Noun phrases, singular: `UserRepository`, `PaymentProcessor` |
| **Constants** | ALL_CAPS_SNAKE: `MAX_RETRIES`, `DEFAULT_TIMEOUT` |
| **Files/modules** | `snake_case` (Python); `kebab-case` or `camelCase` (JS) — be consistent within a project |
| **Abbreviations** | Only well-known ones (`id`, `url`, `http`). Never invent new abbreviations. |

**Never use:**
- Single-letter names except loop counters (`i`, `j`) and well-established conventions (`e` for exception in an `except` clause, `f` for file handles in `with` blocks)
- Misleading names (`temp` that is never temporary, `data` that is actually a user record)
- Negative booleans (`is_not_valid`) — use `is_invalid` or flip the logic

### 1.3 Function / Method Design

- **Single Responsibility:** One function does one thing and does it completely.
- **Size target:** A function should fit on one screen (≤40 lines as a guideline, not a law). If you can't see the whole function at once, it's likely doing too much.
- **Argument count:** 0–3 arguments is ideal; 4+ is a smell; >5 is a refactor trigger. Group related args into a data class or config object.
- **Avoid side effects** where possible. Pure functions (same inputs → same outputs, no mutation of external state) are easier to test, reason about, and compose.
- **Command–Query Separation:** A function either returns a value (query) or changes state (command). Functions that do both are the hardest to reason about. Violations are sometimes necessary; document them explicitly.
- **Avoid output parameters.** Return values; don't mutate arguments passed in (unless you're building a builder/fluent API).

### 1.4 Error Handling Philosophy

- **Fail fast and loudly.** An error that crashes immediately is better than one that silently corrupts data for hours.
- **Never swallow exceptions silently.** A bare `except: pass` or `catch (e) {}` is almost always wrong. If you must suppress, log and document *why*.
- **Handle errors at the right level.** Don't catch exceptions you can't meaningfully handle. Let them propagate to a layer that can.
- **Distinguish error categories:**
  - *Programmer errors* (bugs): let them crash; fix the code
  - *Operational errors* (network down, DB unavailable): handle gracefully, retry with backoff, alert
  - *User input errors*: validate early, return clear error messages to the caller
- **Provide context when re-raising.** `raise ValueError("Expected positive int, got -3") from original_error` is always better than a bare `raise`.

### 1.5 Logging & Observability

- **Use structured logging** (JSON or key-value output). Never build log strings with f-strings in production code — structured logs are machine-parseable and queryable. [[2]](https://www.structlog.org/en/stable/)
- **Log levels have meaning:**
  - `DEBUG`: internal state useful during development; never on in production by default
  - `INFO`: normal operational events (server started, request received, job completed)
  - `WARNING`: unexpected but handled situations (retried after transient failure, config fallback used)
  - `ERROR`: a request/operation failed; needs investigation
  - `CRITICAL`: service is impaired or data may be corrupted; page someone
- **Always log:**
  - Operation start (at DEBUG) and outcome (INFO/ERROR)
  - Correlation/request IDs on every log line in a request context
  - Timing for slow operations (queries > 100ms, external calls)
- **Never log:**
  - Passwords, tokens, secrets, PII (names, emails, SSNs, credit card numbers) — ever, at any level
  - Full request/response bodies by default in production (may contain PII)
- **Include service metadata** on every log event: `service`, `version`, `environment`.

### 1.6 Testing Philosophy

- **Test behaviour, not implementation.** Tests that break when you rename a private method are fragile and wrong.
- **Unit tests** verify one logical unit in isolation (mock all dependencies at the boundary).
- **Integration tests** verify that components work together (real DB, real HTTP client, but seeded/isolated data).
- **End-to-end tests** verify the system from the user's perspective (use sparingly; they are slow and brittle).
- **Coverage targets:** 80% line coverage is a *floor*, not a goal. 100% coverage with trivial tests is worthless. Cover all branching logic, all error paths, all edge cases.
- **Test names must be sentences:** `test_create_user_with_duplicate_email_raises_conflict_error` not `test_create_user_2`.
- **Arrange-Act-Assert (AAA) structure:** Every test has three clearly separated phases. No more than one logical assertion per test (multiple `assert` calls for the same object/outcome are fine).
- **Tests must be deterministic and isolated.** Tests that fail intermittently (flakey tests) are bugs. Tests that depend on execution order are bugs.

### 1.7 Documentation Standards

- **Code should explain *what* it does; comments explain *why*.**
- If you are writing a comment to explain *what* the code does, that's a signal the code needs to be clearer.
- **Docstrings on every public function, class, and module.** Private helpers only need them if the logic is non-obvious.
- **TODO comments must include a name and ticket:** `# TODO(alice): remove after migration completes — PROJ-1234`. Undated, unowned TODOs are permanent dead code.
- **READMEs must include:** what it does, how to set it up locally, how to run tests, how to deploy, and where to file issues. Nothing more unless needed.

### 1.8 Performance Standards

- **Don't optimize prematurely.** Write correct, clear code first. Profile before optimizing.
- **Know your algorithmic complexity.** If a loop processes N items and calls a DB query per iteration, that's O(N) queries — a well-known anti-pattern. Recognize it.
- **Set timeouts on all external calls** (HTTP, DB, queues). A call without a timeout can hang a thread indefinitely.
- **Avoid N+1 query patterns.** Use eager loading or batch queries.
- **Cache at the right layer.** Application-level caches (Redis) for computed results; HTTP caches for idempotent requests; DB-level for schema.

### 1.9 Dependency Management — Universal Rules

- **Minimal footprint:** Add a dependency only when the value clearly exceeds the cost (maintenance burden, supply chain risk, transitive vulnerabilities). Don't add a 500-line library to replace five lines of code.
- **Pin versions** in lockfiles (`poetry.lock`, `requirements.txt` generated by pip-tools/uv). Never deploy from unpinned dependencies.
- **Audit dependencies** before adding them: check last commit date, open CVEs, license compatibility.
- **Never import code you haven't reviewed** in security-sensitive contexts (auth, payments, PII handling).

---

## 2. Python Standards

*(Comprehensive, opinionated, PEP-aligned. Assumes Python 3.10+.)*

### 2.1 Formatting — Black (Non-Negotiable)

Use **Black** with default settings. Do not argue about formatting. [[3]](https://black.readthedocs.io/)

```toml
# pyproject.toml
[tool.black]
line-length = 88
target-version = ["py310"]
```

- Black is run in CI; PRs with unformatted code are blocked at the gate.
- Do not configure Black exceptions except for `# fmt: off` blocks with a documented reason.
- Line length 88 (Black default) is the standard. The PEP 8 79-char limit predates modern monitors and is not enforced.

### 2.2 Linting — Ruff (Replaces Flake8 + isort + pydocstyle)

Use **Ruff** as the single linter. It is an order of magnitude faster than Flake8 and covers all the same rules plus more. [[4]](https://docs.astral.sh/ruff/)

```toml
# pyproject.toml
[tool.ruff]
line-length = 88
target-version = "py310"

[tool.ruff.lint]
select = [
    "E",   # pycodestyle errors
    "W",   # pycodestyle warnings
    "F",   # pyflakes
    "I",   # isort
    "N",   # pep8-naming
    "B",   # flake8-bugbear (catches real bugs, not just style)
    "C4",  # flake8-comprehensions
    "UP",  # pyupgrade (modernizes syntax automatically)
    "S",   # flake8-bandit (security)
    "ANN", # flake8-annotations (enforces type hints)
    "D",   # pydocstyle
]
ignore = [
    "D100", "D104",  # missing module/package docstrings — optional at module level
    "ANN101",        # missing type annotation for `self`
]

[tool.ruff.lint.pydocstyle]
convention = "google"
```

**The `B` (bugbear) ruleset catches real bugs**, not just style violations. Enable it without question. Key rules it enforces:
- B006: Do not use mutable data structures for argument defaults (`def f(x=[])` is a classic Python trap)
- B008: Do not perform function calls in default arguments
- B023: Functions defined in a loop that use the loop variable

### 2.3 Type Annotations — Required at All Public Boundaries

Type annotations are **required** for all public functions, methods, class attributes, and module-level variables. [[5]](https://peps.python.org/pep-0484/) [[6]](https://peps.python.org/pep-0526/)

**Required (always annotate):**
```python
def get_user(user_id: int) -> User | None:
    ...

class UserRepository:
    db: Database
    max_retries: int = 3
```

**Modern syntax (Python 3.10+):**
- Use `X | Y` instead of `Union[X, Y]`
- Use `X | None` instead of `Optional[X]`
- Use `list[str]`, `dict[str, int]`, `tuple[int, ...]` (lowercase, built-in generics)
- Use `from __future__ import annotations` at the top of files targeting Python < 3.10 for forward-reference support

**Type annotation rules:**
- `# type: ignore` is allowed only with a specific error code and a comment explaining why: `# type: ignore[assignment]  # third-party stub is wrong`
- Do not annotate `self` or `cls`.
- Annotate return type `-> None` explicitly for functions that return nothing. Makes intent clear.
- Use `TypeAlias` for complex repeated types: `UserId: TypeAlias = int`
- Use `TypedDict` for dicts with a fixed schema; use `dataclass` or Pydantic model for anything complex.
- `Any` is a last resort. Document why it was unavoidable.

### 2.4 Static Type Checking — mypy in Strict Mode

```ini
# mypy.ini
[mypy]
python_version = 3.10
strict = true
warn_return_any = true
warn_unused_configs = true
```

`strict = true` enables: `disallow_untyped_defs`, `disallow_any_generics`, `no_implicit_optional`, `warn_redundant_casts`, `warn_unused_ignores`, and more.

Run mypy in CI. mypy errors block merge. If a third-party library lacks stubs, add a `[[mypy-library_name]]` ignore block with a comment.

### 2.5 Naming — PEP 8 Conventions [[1]](https://peps.python.org/pep-0008/)

| Construct | Convention | Examples |
|---|---|---|
| Functions, variables, arguments | `snake_case` | `get_user`, `retry_count` |
| Classes, Exceptions | `PascalCase` | `UserRepository`, `PaymentError` |
| Constants (module-level) | `UPPER_SNAKE_CASE` | `MAX_RETRIES`, `API_BASE_URL` |
| Modules, packages | `snake_case` (short, no hyphens) | `user_service`, `payment_utils` |
| Private attributes/methods | `_single_leading_underscore` | `_validate_token` |
| Name-mangled (use sparingly) | `__double_leading` | Only for true name-mangling needs |
| Type variables | Short `PascalCase` by convention | `T`, `UserT`, `KT`, `VT` |

**Names to actively avoid:**
- `l` (lowercase L), `O` (uppercase O), `I` (uppercase i) — ambiguous
- Shadow built-ins: `list`, `dict`, `id`, `type`, `input`, `filter`, `map`
- Non-descriptive: `data`, `info`, `obj`, `thing`, `stuff`, `temp`

### 2.6 Imports — Order and Style

Follow the isort standard (enforced by Ruff `I` rules):

1. Standard library
2. Third-party packages
3. First-party (your code)
4. Relative imports (only within a package)

```python
from __future__ import annotations

import json
import os
from collections.abc import Iterator
from pathlib import Path

import httpx
import structlog

from myapp.core import settings
from myapp.models import User
from .utils import validate_token
```

**Rules:**
- No wildcard imports (`from module import *`) except in `__init__.py` re-exports and only with explicit `__all__`.
- Import modules, not symbols, for namespace clarity in complex codebases. Exception: well-known symbols (`from pathlib import Path`).
- No circular imports. Resolve them by restructuring, not by moving imports into function bodies (which hides the problem).

### 2.7 Docstrings — Google Style [[7]](https://google.github.io/styleguide/pyguide.html#38-comments-and-docstrings)

Use **Google-style docstrings** consistently.

```python
def retry(
    fn: Callable[[], T],
    *,
    max_attempts: int = 3,
    delay_seconds: float = 1.0,
) -> T:
    """Retries a callable up to max_attempts times with a fixed delay.

    Does not retry on KeyboardInterrupt or SystemExit.

    Args:
        fn: The callable to retry. Must be idempotent.
        max_attempts: Maximum number of attempts before raising. Must be >= 1.
        delay_seconds: Seconds to wait between attempts.

    Returns:
        The return value of fn on success.

    Raises:
        RetryExhaustedError: If all attempts fail. Wraps the last exception.

    Example:
        >>> result = retry(lambda: call_external_api(), max_attempts=5)
    """
```

**Rules:**
- One-liner docstring for trivially obvious functions is acceptable: `"""Returns the user's full name."""`
- Always document `Raises:` for any non-obvious exception.
- Keep docstrings up to date. A wrong docstring is worse than no docstring.

### 2.8 Exception Design

Define a base exception for each package/application:

```python
# myapp/exceptions.py

class MyAppError(Exception):
    """Base exception for all application errors. Never raise directly."""

class ValidationError(MyAppError):
    """Input failed validation. Caller should return 4xx."""

class NotFoundError(MyAppError):
    """Resource does not exist. Caller should return 404."""

class ExternalServiceError(MyAppError):
    """Failure communicating with an external dependency."""
    def __init__(self, service: str, message: str) -> None:
        self.service = service
        super().__init__(f"{service}: {message}")
```

**Rules:**
- Always subclass `Exception`, never `BaseException` (which catches `KeyboardInterrupt` and `SystemExit`).
- Always use exception chaining: `raise AppError("context") from original_error`. This preserves the full traceback and the `__cause__`.
- Catch the most specific exception you can. `except Exception` at a boundary (API handler, job runner) is fine. `except Exception` buried in business logic is not.
- Never use exceptions for normal control flow (e.g., `try: return dict[key] except KeyError: return default` — use `dict.get(key, default)` instead).
- Do not define more exceptions than you need. One per meaningful error category, not one per function.

### 2.9 Testing — pytest Standards

```
tests/
├── unit/
│   ├── test_user_service.py
│   └── test_payment_processor.py
├── integration/
│   ├── test_user_api.py
│   └── test_database_repository.py
└── conftest.py
```

**Naming:** `test_<unit>_<scenario>_<expected_outcome>`
```python
def test_create_user_with_duplicate_email_raises_conflict_error(): ...
def test_get_user_when_not_found_returns_none(): ...
def test_payment_processor_with_expired_card_raises_payment_error(): ...
```

**Fixtures:**
```python
# conftest.py
@pytest.fixture(scope="session")
def db() -> Generator[Database, None, None]:
    """Shared database connection for the test session."""
    conn = create_test_database()
    yield conn
    conn.close()

@pytest.fixture
def sample_user(db: Database) -> User:
    """A fresh user for each test. Cleaned up after."""
    user = db.create_user(email="test@example.com")
    yield user
    db.delete_user(user.id)
```

**Fixture scope rules:**
- `function` (default): safest, use for anything that mutates state
- `module`: acceptable for read-only, expensive setup
- `session`: only for truly immutable, expensive setup (DB connection pool, loaded ML model)
- `autouse=True`: only for universally-needed setup (e.g., reset log capture)

**Parametrize for input variation:**
```python
@pytest.mark.parametrize(
    "email,expected_error",
    [
        ("not-an-email", "invalid email format"),
        ("", "email is required"),
        ("a" * 256 + "@example.com", "email too long"),
    ],
    ids=["malformed", "empty", "too-long"],
)
def test_validate_email_rejects_invalid_inputs(email: str, expected_error: str) -> None:
    with pytest.raises(ValidationError, match=expected_error):
        validate_email(email)
```

**What to always test:**
- All branches of conditional logic
- All error paths and exception scenarios
- Boundary values (0, -1, max, max+1)
- The happy path (obviously)
- Anything that has been a production bug

**What not to test:**
- Third-party library internals
- Python language behaviour itself
- Private methods in isolation (if the private method is worth testing, extract it)

### 2.10 Dependency Management — uv (Recommended 2024+)

**`uv`** is now the recommended toolchain for dependency management due to its speed and compatibility. [[8]](https://astral.sh/blog/uv)

```bash
# Setup
uv venv
source .venv/bin/activate
uv pip install -r requirements.txt

# Adding a dependency
uv add httpx
uv add --dev pytest pytest-cov
```

For lockfile-based workflows (strongly preferred):
```
pyproject.toml          # declare top-level deps with loose constraints
requirements.txt        # generated lockfile (pip-compiled) — commit this
requirements-dev.txt    # dev/test lockfile — commit this
```

**Rules:**
- Always deploy from the lockfile. Never `pip install httpx~=0.27` in a Dockerfile without pinning.
- Commit both `pyproject.toml` and the lockfile. Never commit only one.
- Separate dev dependencies from runtime dependencies. Linters, test runners, and formatters are not production dependencies.
- Run `uv pip audit` (or `pip-audit`) in CI to check for CVEs in installed packages.

### 2.11 Pythonic Idioms — Do and Don't

**Do:**
```python
# Context managers for resources
with open("file.txt") as f:
    data = f.read()

# List/dict/set comprehensions for simple transforms
active_users = [u for u in users if u.is_active]

# Walrus operator for assignment in conditions (Python 3.8+)
if match := PATTERN.search(text):
    process(match.group(0))

# Enumerate instead of range(len(...))
for i, item in enumerate(items):
    ...

# Unpack instead of index access
first, *rest = items
x, y, z = point

# dataclasses for structured data
@dataclass
class Point:
    x: float
    y: float
```

**Don't:**
```python
# Don't use mutable default arguments
def append(item, lst=[]):  # BUG: lst is shared across calls
    lst.append(item)
    return lst

# Don't check type with type(), use isinstance()
if type(x) == int:  # wrong; misses subclasses
    ...
if isinstance(x, int):  # correct

# Don't use bare except
try:
    risky()
except:  # catches SystemExit and KeyboardInterrupt too
    pass

# Don't use == to compare with None
if x == None:  # wrong
if x is None:  # correct

# Don't catch and re-raise without chaining
try:
    risky()
except ValueError as e:
    raise RuntimeError("failed") # loses traceback
    # correct: raise RuntimeError("failed") from e
```

---

## 3. JavaScript / Web Standards

*(Focused and pragmatic — Alice is not primarily a JS engineer.)*

### 3.1 Variables — `const` by Default

```javascript
// Rule: const unless you know you'll reassign. Never var.
const userId = getUserId();           // never reassigned
let retryCount = 0;                   // will be incremented
retryCount += 1;

// var is forbidden. It has function scope, not block scope,
// and hoists in confusing ways.
var name = "Alice";  // ❌ FORBIDDEN
```

ESLint rules to enforce: `no-var: error`, `prefer-const: error`.

### 3.2 ESLint + Prettier Configuration

```json
// .eslintrc.json (or eslint.config.js for flat config)
{
  "env": { "es2022": true, "browser": true, "node": true },
  "extends": ["eslint:recommended"],
  "rules": {
    "no-var": "error",
    "prefer-const": "error",
    "eqeqeq": ["error", "always"],
    "no-console": "warn",
    "no-unused-vars": ["error", { "argsIgnorePattern": "^_" }],
    "no-implicit-globals": "error"
  }
}
```

Use **Prettier** for formatting (no manual formatting debates):
```json
// .prettierrc
{
  "singleQuote": true,
  "trailingComma": "es5",
  "semi": true,
  "printWidth": 100
}
```

### 3.3 Module System — ESM Only in New Code

- New code uses **ESM** (`import`/`export`), not CommonJS (`require`/`module.exports`).
- In Node.js, set `"type": "module"` in `package.json`.
- Do not mix module systems within a project.

### 3.4 DOM Manipulation

```javascript
// Use querySelector/querySelectorAll, not getElementById soup
const button = document.querySelector('#submit-btn');
const items = document.querySelectorAll('.list-item');

// Event listeners, never inline handlers
button.addEventListener('click', handleSubmit);
// NOT: <button onclick="handleSubmit()"> in HTML

// Always check element existence before operating
const el = document.querySelector('.optional-widget');
if (el) el.textContent = 'Updated';

// Prefer dataset over getAttribute for data attributes
const userId = element.dataset.userId;  // reads data-user-id
```

### 3.5 HTML Semantics

- Use semantic elements: `<main>`, `<nav>`, `<header>`, `<footer>`, `<article>`, `<section>`, `<aside>`, `<figure>`, `<time>`.
- Heading hierarchy must be logical: one `<h1>` per page, `<h2>`–`<h6>` in order. Do not skip levels for visual effect; use CSS for size.
- Forms: every `<input>` has a `<label>` (associated via `for`/`id` or wrapping). Fieldsets and legends for related groups. Explicit `type` on every button.
- Links: `<a href="...">` for navigation; `<button>` for actions. Never `<div onclick>` or `<span onclick>`.

### 3.6 CSS Standards

```css
/* All shared values as custom properties */
:root {
  --color-primary: #1a2a4a;
  --color-action: #bf0a30;
  --spacing-base: 1rem;
  --font-size-body: 1rem;
  --transition-default: 200ms ease;
}

/* No magic numbers */
.card {
  padding: var(--spacing-base);          /* ✓ */
  padding: 16px;                         /* ✗ — magic number */
  margin-bottom: calc(var(--spacing-base) * 2);
}
```

**Rules:**
- All colors, spacing, font sizes, z-index values, and transitions must be custom properties. Magic numbers in CSS are a maintenance nightmare.
- No `!important` except as a deliberate override layer (document why).
- Do not style with `id` selectors (high specificity, hard to override). Use classes.
- BEM or a similar naming system for component-level CSS: `.card`, `.card__header`, `.card--featured`.

### 3.7 Accessibility (WCAG 2.1 AA — Non-Negotiable) [[9]](https://www.w3.org/WAI/WCAG21/quickref/)

Accessibility operates on two equal dimensions: **disability access** and **content democratization**. Neither is optional. Neither justifies weakening policy positions or shifting them toward the political center.

#### Disability accessibility

These are requirements. Treat violations the same as security failures.

| Requirement | Rule |
|---|---|
| Structure | `<html lang="en">` on every page. Single `<h1>` per page. Headings descend without skipping levels. |
| Skip link | `<a href="#main-content" class="skip-link sr-only focusable">Skip to main content</a>` as first body element (injected by `app.js`). First main section must have `id="main-content"`. |
| Images | All `<img>` have meaningful `alt` text. Decorative images get `alt=""`. Icons conveying meaning need `aria-label` or adjacent label text. |
| Color contrast | Normal text ≥ 4.5:1. Large text (≥18pt / 14pt bold) ≥ 3:1. UI components ≥ 3:1. |
| Color alone | Never use color as the only way information is conveyed — always pair with text, icon, or pattern. |
| Keyboard | All functionality operable via keyboard. Tab order must be logical. |
| Focus | Focus indicator always visible. Never suppress `outline` without an equally visible replacement. Use `:focus-visible { outline: 2px solid var(--gold); outline-offset: 3px; }`. |
| Interactive names | Every link, button, and control has a descriptive accessible name via visible text, `aria-label`, or `aria-labelledby`. Never `title` alone. |
| ARIA | Use native HTML before ARIA. Incorrect ARIA is worse than no ARIA. `aria-expanded` + `aria-controls` required on custom accordions. |
| Motion | Every animation/transition must have a `@media (prefers-reduced-motion: reduce)` override. The global override in `style.css` covers this — do not add `!important` transitions that escape it. |
| Forms | Every input has a `<label>`. `placeholder` is not a label. Error messages name the field and explain what is wrong. |
| Video/audio | Captions and text transcripts required. No autoplay. |
| Zoom | All content readable and operable at 200% browser zoom without horizontal scrolling. No fixed pixel heights that clip text. |
| Semantics | Use `<nav>`, `<main>`, `<section>`, `<article>`, `<footer>`, `<button>`. ARIA only when native semantics are insufficient. |

**Required CSS utilities (defined once in `style.css`):**

```css
.sr-only { position: absolute; width: 1px; height: 1px; padding: 0; margin: -1px;
  overflow: hidden; clip: rect(0,0,0,0); white-space: nowrap; border: 0; }
.sr-only.focusable:focus, .sr-only.focusable:focus-visible {
  position: static; width: auto; height: auto; margin: 0;
  overflow: visible; clip: auto; white-space: normal; }
:focus-visible { outline: 2px solid var(--gold); outline-offset: 3px; }
:focus:not(:focus-visible) { outline: none; }
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
    scroll-behavior: auto !important; } }
```

#### Content accessibility (democratization)

- **Every policy position card must have both `rule-plain` and `rule-stmt`:**
  - `rule-plain` (`<p class="rule-plain">`) — 1–3 sentences in plain language (~8th grade). What does this position do and why does it matter? No jargon. Any person regardless of education must understand it.
  - `rule-stmt` (`<p class="rule-stmt">`) — Full technical/legal statement. Precise language, specific thresholds, enforcement mechanisms, regulatory detail.
  - `rule-plain` appears immediately after `<p class="rule-title">`, before `<p class="rule-stmt">`.
  - `rule-plain` is **not** a summary of `rule-stmt`. It is an independent, accessible explanation. Backfill for existing cards is deferred post-migration.
- **Plain-language pillar summaries**: every pillar and policy family needs a 1–2 sentence plain-language summary alongside technical content.
- **Jargon**: define legal or technical terms on first use with tooltip, glossary link, or parenthetical.
- **Titles**: policy card titles must be understandable without domain expertise. No insider language.
- **Inclusive language**: gender-neutral throughout ("persons" not "men", singular they/them). Write as if a persuadable, politically independent person is reading for the first time.
- **Contribution pathways**: Get Involved page always lists all active channels (GitHub, Discord, non-technical workflow). CONTRIBUTING.md written for someone who has never used GitHub.

---

## 4. Security Standards

*(Cross-language, non-negotiable. These are blockers, not suggestions.)*

### 4.1 The Absolute Never-Do List

These are automatic CI failures and immediate code review rejects:

**Input & execution:**
- ❌ Never use `eval()`, `exec()`, or equivalent in any language with user-supplied input
- ❌ Never build shell commands with string concatenation/interpolation from user data
- ❌ Never use `subprocess(..., shell=True)` with any variable content; always pass argument lists
- ❌ Never construct SQL queries with string formatting — always use parameterized queries
- ❌ Never use `pickle.load()` or `pickle.loads()` on data from any external source (network, file, user input). Pickle deserialization is arbitrary code execution. [[10]](https://owasp.org/www-community/attacks/Deserialization_of_untrusted_data)
- ❌ Never use `yaml.load()` — always `yaml.safe_load()`
- ❌ Never use `marshal` or `shelve` with untrusted data

**Secrets:**
- ❌ Never hardcode API keys, passwords, tokens, or credentials anywhere in source code
- ❌ Never commit `.env` files containing secrets (`.env` should be in `.gitignore`; `.env.example` with placeholder values is allowed)
- ❌ Never log secrets, tokens, or PII at any log level
- ❌ Never put secrets in URLs (query parameters end up in logs, browser history, referrer headers)

**Cryptography:**
- ❌ Never implement your own cryptography. Use well-reviewed libraries (`cryptography`, `passlib`, `bcrypt`).
- ❌ Never use MD5 or SHA-1 for security purposes (hashing passwords, signing tokens). Use SHA-256+.
- ❌ Never use ECB mode for block ciphers.
- ❌ Never use `random` module for security purposes. Use `secrets` (Python) or `crypto.randomBytes` (Node).

**Web:**
- ❌ Never trust `Content-Type` headers alone for file upload validation; check file contents
- ❌ Never render user-supplied HTML without sanitization (XSS)
- ❌ Never use `innerHTML` with any unsanitized data in JavaScript

### 4.2 Input Validation — Validate Everything at Every Boundary

```python
# Use Pydantic for structured input validation in Python
from pydantic import BaseModel, EmailStr, Field

class CreateUserRequest(BaseModel):
    email: EmailStr
    username: str = Field(min_length=3, max_length=50, pattern=r"^[a-zA-Z0-9_-]+$")
    age: int = Field(ge=0, le=150)
```

**Rules:**
- Validate at the entry point (API handler, CLI argument parser, message queue consumer). Do not pass unvalidated data deeper into the system.
- Whitelist, don't blacklist. Define what is allowed; reject everything else.
- Validate type, format, range, and length independently.
- Return structured error messages that identify the field and the problem (don't expose internal details).

### 4.3 Secrets Management

```python
# CORRECT: Load from environment
import os
from functools import lru_cache

@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings(
        database_url=os.environ["DATABASE_URL"],
        api_secret=os.environ["API_SECRET_KEY"],
    )
```

**Toolchain:**
- Runtime secrets: environment variables injected by the deployment platform (Kubernetes secrets, AWS Parameter Store, HashiCorp Vault).
- Development secrets: `.env` file loaded by `python-dotenv`, never committed.
- Pre-commit hook: `detect-secrets` or `gitleaks` to block accidental commits of secrets. [[11]](https://github.com/Yelp/detect-secrets)

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/Yelp/detect-secrets
    rev: v1.4.0
    hooks:
      - id: detect-secrets
        args: ['--baseline', '.secrets.baseline']
```

### 4.4 Dependency Security

- Run `pip-audit` (Python) or `npm audit` (Node) in CI. Block merges on HIGH/CRITICAL CVEs.
- Use GitHub Dependabot or equivalent for automated PR-based dependency updates.
- Pin exact versions in lockfiles. Know what you're running.
- Prefer packages with: recent commits, active maintenance, published security policies, few transitive dependencies.
- Generate an SBOM (CycloneDX or SPDX format) on release. [[12]](https://cyclonedx.org/)

### 4.5 OWASP Top 10 Mitigations [[13]](https://owasp.org/www-project-top-ten/)

| OWASP Risk | Mitigation |
|---|---|
| A01: Broken Access Control | Enforce authorization on every endpoint; deny by default; never trust client-supplied role/permission claims |
| A02: Cryptographic Failures | TLS 1.2+ everywhere; encrypted at-rest PII; no home-rolled crypto |
| A03: Injection | Parameterized queries; ORM usage; no shell=True; input validation |
| A04: Insecure Design | Threat model early; fail-secure defaults; principle of least privilege |
| A05: Security Misconfiguration | Disable debug endpoints in production; rotate default credentials; explicit CORS policy |
| A06: Vulnerable Components | pip-audit/npm audit in CI; dependency pinning; SBOM |
| A07: Auth Failures | Rate-limit login; lock accounts after N failures; secure session management; short token TTLs |
| A08: Data Integrity Failures | Verify signatures on software updates and data pipelines; no pickle from untrusted sources |
| A09: Logging Failures | Log security events (auth attempts, permission failures); no PII in logs; tamper-evident log storage |
| A10: SSRF | Validate and allowlist URLs before making server-side requests; restrict egress in production |

### 4.6 PII and Privacy by Design [[14]](https://gdpr-info.eu/art-25-gdpr/)

- **Minimize collection:** only store PII you actively need; delete it when the purpose is served.
- **Redact in logs:** use a logging processor to mask known PII fields (`email`, `password`, `ssn`, `card_number`) before any log output.
- **Encrypt at rest** any PII stored in databases or file storage (column-level encryption or full-disk).
- **Document data flows:** know where PII enters, where it's stored, and who can access it. This is not optional under GDPR (Article 30).
- **Right to erasure:** build data deletion/anonymization into the data model from day one, not as an afterthought.

---

## 5. Git & Workflow Standards

### 5.1 Commit Messages — Conventional Commits [[15]](https://www.conventionalcommits.org/en/v1.0.0/)

Format:
```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

**Types:**
| Type | Meaning |
|---|---|
| `feat` | New feature (maps to MINOR in SemVer) |
| `fix` | Bug fix (maps to PATCH) |
| `docs` | Documentation only |
| `refactor` | Code change that neither fixes a bug nor adds a feature |
| `test` | Adding or correcting tests |
| `chore` | Tooling, build, CI — no production code change |
| `perf` | Performance improvement |
| `ci` | CI configuration changes |
| `revert` | Reverts a previous commit |
| `BREAKING CHANGE` | In footer or as `feat!:` — maps to MAJOR |

**Rules:**
- Description is imperative mood, present tense: `add user authentication`, not `added` or `adds`.
- Description ≤ 72 characters.
- Body explains *why*, not *what* (the diff shows what).
- Reference issue numbers in footer: `Closes #123`, `Refs #456`.

**Good examples:**
```
feat(auth): add JWT refresh token rotation

Implements sliding session windows by issuing a new refresh token
on every use and invalidating the previous one. Prevents token
reuse after theft.

Closes #892
```
```
fix(api): handle None return from get_user_by_email

Previously this raised AttributeError when a user attempted login
with an unregistered email. Now returns 401 with a generic message
to avoid user enumeration.

Closes #901
```
```
chore(deps): upgrade httpx 0.26 → 0.27

Addresses CVE-2024-XXXX in httpx's redirect handling.
```

### 5.2 Atomic Commits

- One logical change per commit. Not one file, not one task — one *logical unit*.
- Every commit must pass tests and linting independently (enables bisect).
- Never commit "fix linting" or "fix typo" as a separate commit after submitting — rebase and squash before pushing.
- Never mix refactoring with feature changes in the same commit. They must be separate commits (or PRs) to make review tractable.

### 5.3 Branch Naming

```
feature/<ticket-id>-short-description    # feature/AUTH-142-refresh-token-rotation
fix/<ticket-id>-short-description        # fix/API-901-login-null-email
chore/<short-description>                # chore/upgrade-httpx
docs/<short-description>                 # docs/add-api-authentication-guide
release/<version>                        # release/2.4.0
hotfix/<ticket-id>-short-description     # hotfix/PROD-88-stripe-webhook-crash
```

### 5.4 Pull Request Standards

**PR size:** Target ≤ 400 lines changed. PRs > 800 lines get split. Large PRs are statistically less thoroughly reviewed and have higher defect rates. [[16]](https://smartbear.com/learn/code-review/best-practices-for-peer-code-review/)

**PR description template:**
```markdown
## What
One paragraph: what changed and why.

## How
Brief: approach taken, key design decisions.

## Testing
How was this tested? What cases are covered?

## Checklist
- [ ] Tests added/updated
- [ ] Documentation updated
- [ ] No secrets or PII in code or logs
- [ ] Linting/type-checking passes
- [ ] Reviewed for security implications
```

**Rules:**
- CI must pass before requesting review. No exceptions.
- Address all review comments before merging. "Acknowledged" or "will fix in follow-up" requires a ticket reference.
- Squash-merge to keep main history clean (unless the full commit history is meaningful).
- Never force-push to `main` or shared branches.
- Protect `main`: require at least 1 approval + passing CI; no direct pushes.

---

## 6. AI Instruction File Hygiene

### 6.1 Global vs. Repo-Local Instructions

**Global (user-level, e.g., VS Code user settings or `~/.config/copilot/instructions.md`):**
- Personal preferences: pronoun preferences, response tone, formatting choices
- Universal coding rules that apply across all your projects: logging philosophy, error handling approach, never-do-this list
- Language defaults you always use (e.g., "I write Python 3.10+")
- Workflow habits: how you like explanations structured, how verbose you want comments

**Repo-local (`.github/copilot-instructions.md`, `CLAUDE.md`, `.cursorrules`):**
- Project-specific conventions: which framework, which DB, which auth pattern
- Team standards: PR template, branch naming for this project
- Domain context: what this repo is, what it does, what it doesn't do
- Stack-specific: "this project uses structlog, not logging"; "this project uses uv, not poetry"
- File structure: where tests live, how modules are organized

**The test:** Ask "would this rule apply to a new, unrelated project I start tomorrow?" If yes → global. If no → repo-local.

### 6.2 What Makes a Good AI Instruction File

**Be specific and actionable:**
```markdown
# Bad
Write good, clean Python code.

# Good
All Python functions must have:
- Type annotations on all parameters and return values
- Google-style docstrings
- A return type of None must be annotated explicitly (-> None)
```

**Provide positive AND negative examples:**
```markdown
# Exception handling: always chain exceptions

# Correct:
raise PaymentError("charge failed") from stripe_error

# Wrong (loses traceback context):
raise PaymentError("charge failed")
```

**State the why for non-obvious rules:**
```markdown
# Never use pickle for serialization of user-controlled data.
# pickle.loads() is equivalent to arbitrary code execution on the
# deserializing machine. Use JSON, msgpack, or protobuf instead.
```

**Give the AI the project's vocabulary:**
```markdown
## Domain terminology
- "subscriber" = a user who has paid for access
- "member" = a user in a team workspace
- These are different roles. Do not conflate them.
```

### 6.3 Structural Rules for Instruction Files

1. **Put hard constraints first** (security, never-do-this) before style preferences. The AI should see the most critical rules before context window limits cut in.
2. **Use numbered or bulleted lists**, not paragraphs of prose. LLMs comply more reliably with discrete rules than narrative descriptions.
3. **Section with clear headers.** The AI can reference and apply rules by section.
4. **Keep the file under ~2,000 words** for a repo-level file. Longer files get truncated or the later rules are weighted less. Put the most important rules first.
5. **Avoid contradictions.** If you say "always add a docstring" and "don't add comments to obvious code," clarify the scope of each rule.
6. **Include an example of the ideal output** for your most common task type. A concrete example is worth 10 abstract rules.

### 6.4 Common Failure Modes to Avoid

| Failure Mode | Example | Fix |
|---|---|---|
| **Vague rules** | "write readable code" | "functions ≤ 40 lines; max 4 parameters; no nested conditionals > 3 levels deep" |
| **Contradictory rules** | "add docstrings to all functions" + "don't comment obvious code" | Clarify scope: "docstrings required on all public functions; private helpers only if non-obvious" |
| **Overly prescriptive on style** | 30 rules about whitespace | Let Black/Prettier handle formatting; spend your instruction budget on semantics |
| **Missing context** | Instructions with no project description | Always start with: what is this project, what language/framework, what does it NOT do |
| **Rules that age badly** | "use Python 3.8 syntax" | Specify minimum version and update periodically |
| **Instructions ignored due to length** | 5,000-word instruction file | Front-load the critical rules; cut the rest |

### 6.5 Template Structure (Recommended)

```markdown
# [Project Name] — Copilot Instructions

## What this project is
[2–3 sentences: purpose, stack, users]

## What this project is NOT
[1–3 items: scope exclusions, technologies not used here]

## Non-negotiable rules (security)
[bullet list of never-do-this items specific to this project]

## Language and framework conventions
[Python/JS/etc. specific rules]

## Architecture rules
[module structure, dependency direction, service boundaries]

## Testing requirements
[what must be tested, how tests are named, what frameworks]

## Documentation requirements
[docstring style, comment policy]

## Example of good code in this project
[paste one real function that follows all the rules]
```

---

## 7. Architecture & Design Principles

### 7.1 SOLID — Applied, Not Theoretical [[17]](https://en.wikipedia.org/wiki/SOLID)

**S — Single Responsibility Principle**

A class/module should have exactly one reason to change.

```python
# ❌ Wrong: UserService sends emails AND manages the database
class UserService:
    def create_user(self, data: CreateUserRequest) -> User:
        user = self.db.insert(data)
        self.send_welcome_email(user)  # wrong: two responsibilities
        return user

# ✓ Correct: separate concerns
class UserService:
    def create_user(self, data: CreateUserRequest) -> User:
        return self.db.insert(data)

class UserOnboardingService:
    def on_user_created(self, user: User) -> None:
        self.email_service.send_welcome(user)
```

**O — Open/Closed Principle**

Open for extension, closed for modification. Add behavior by adding code, not modifying existing code.

```python
# ❌ Wrong: adding a new notification type requires editing this function
def notify_user(user: User, channel: str) -> None:
    if channel == "email":
        send_email(user)
    elif channel == "sms":
        send_sms(user)

# ✓ Correct: polymorphism / strategy pattern
class NotificationChannel(Protocol):
    def send(self, user: User) -> None: ...

class EmailNotification:
    def send(self, user: User) -> None: send_email(user)

class SMSNotification:
    def send(self, user: User) -> None: send_sms(user)

def notify_user(user: User, channel: NotificationChannel) -> None:
    channel.send(user)
```

**L — Liskov Substitution Principle**

Subtypes must be substitutable for their base types without altering program correctness.

The practical test: if you have a list of `Animal` and replace it with a list of `Dog`, does everything still work? If `Dog.move()` raises an exception that `Animal.move()` never does, you've violated LSP. Violating LSP almost always means the inheritance hierarchy is wrong.

**I — Interface Segregation Principle**

No client should depend on methods it doesn't use. Prefer small, focused interfaces over large ones.

```python
# ❌ Wrong: all users of Repository must implement all methods
class Repository(ABC):
    def find(self, id: int) -> T: ...
    def save(self, entity: T) -> None: ...
    def delete(self, id: int) -> None: ...
    def find_all(self) -> list[T]: ...

# ✓ Better: separate by use case
class Readable(Protocol[T]):
    def find(self, id: int) -> T | None: ...

class Writable(Protocol[T]):
    def save(self, entity: T) -> None: ...
```

**D — Dependency Inversion Principle**

High-level modules should not depend on low-level modules. Both should depend on abstractions.

```python
# ❌ Wrong: UserService is tightly coupled to PostgresRepository
class UserService:
    def __init__(self) -> None:
        self.repo = PostgresUserRepository()  # hardwired

# ✓ Correct: dependency is injected; UserService depends on an abstraction
class UserService:
    def __init__(self, repo: UserRepository) -> None:
        self.repo = repo  # inject whatever implementation you want

# At the composition root:
service = UserService(repo=PostgresUserRepository(db=db_conn))
# In tests:
service = UserService(repo=InMemoryUserRepository())
```

### 7.2 DRY — Don't Repeat Yourself

**The real DRY rule:** Every piece of *knowledge* (business rule, algorithm, data shape) should have a single, authoritative representation. It is not "never write similar-looking code" (that's a different, weaker version of the rule).

```python
# ❌ Wrong: the "user must be active and verified" rule is scattered
def can_post(user): return user.is_active and user.is_verified
def can_comment(user): return user.is_active and user.is_verified
def can_vote(user): return user.is_active and user.is_verified

# ✓ Correct: one authoritative place
def is_permitted_user(user: User) -> bool:
    """An active, verified user who can perform content actions."""
    return user.is_active and user.is_verified
```

**DRY does NOT mean:** aggressively abstracting any two pieces of code that look similar. If two things happen to look alike but represent different *concepts* with different *rates of change*, duplication is better than a wrong abstraction.

### 7.3 YAGNI — You Aren't Gonna Need It

Don't build features, abstractions, or generality that isn't required by the current requirements.

```python
# ❌ Wrong: building a plugin system when there is one implementation
class NotificationPluginRegistry:
    _plugins: dict[str, type[Notifier]] = {}

    @classmethod
    def register(cls, name: str, plugin: type[Notifier]) -> None: ...

    @classmethod
    def send(cls, name: str, user: User) -> None:
        cls._plugins[name]().send(user)

# ✓ Correct: call the email function directly until you have a second implementation
def send_welcome_email(user: User) -> None:
    email_client.send(to=user.email, template="welcome")
```

YAGNI violations accumulate. A codebase full of "for future extensibility" code that was never needed is a maintenance burden, not an asset.

### 7.4 KISS — Keep It Simple

Complexity is the enemy of correctness and the friend of bugs. The simple solution that works today is almost always better than the elegant abstraction.

Concretely:
- Prefer flat code over deeply nested code (the "arrow anti-pattern")
- Prefer a module-level function over a class with one method
- Prefer standard library over a framework where both would work
- Prefer a list over a custom data structure unless you have profiling evidence
- Prefer a synchronous function over an async one unless concurrency is genuinely needed

### 7.5 Separation of Concerns

Organize code so that each component has a clear responsibility and a clear boundary:

```
Presentation layer     (API handlers, CLI commands, HTML templates)
       ↓ calls
Application/Service layer   (use cases, orchestration, transactions)
       ↓ calls
Domain layer           (business rules, entities, value objects)
       ↓ depends on abstractions (Protocols/ABCs)
Infrastructure layer   (DB, HTTP clients, message queues, file system)
```

**Rules:**
- Business logic (pricing rules, eligibility checks, state machine transitions) never lives in API handlers or DB queries.
- DB queries never live in business logic. Use a repository pattern.
- HTTP clients never live in business logic. Pass data in, get data out.
- Import direction must only flow inward (outer layers can import inner layers; inner layers must not import outer layers).

### 7.6 Fail-Secure Defaults

Security and correctness defaults must be the safe choice:

```python
# ❌ Wrong: default is to allow access
def can_view(user, resource, allow_by_default=True):
    ...

# ✓ Correct: default is to deny; access must be explicitly granted
def can_view(user, resource, allow_by_default=False):
    ...
```

Applied to configuration: new feature flags default to off, not on. New API endpoints default to requiring authentication, not public. New roles default to minimum permissions.

---

## Sources

[1] van Rossum, G., Warsaw, B., & Coghlan, A. (2001, updated 2013). *PEP 8 – Style Guide for Python Code*. Python Software Foundation. https://peps.python.org/pep-0008/

[2] Structlog maintainers. (2024). *structlog documentation: Structured logging for Python*. https://www.structlog.org/en/stable/

[3] Langa, Ł. (2019). *Black: The uncompromising Python code formatter*. https://black.readthedocs.io/

[4] Astral Software. (2023–2024). *Ruff: An extremely fast Python linter and code formatter*. https://docs.astral.sh/ruff/

[5] van Rossum, G., Lehtosalo, J., & Langa, Ł. (2014). *PEP 484 – Type Hints*. Python Software Foundation. https://peps.python.org/pep-0484/

[6] Levkivskyi, I. (2016). *PEP 526 – Syntax for Variable Annotations*. Python Software Foundation. https://peps.python.org/pep-0526/

[7] Google. (2024). *Google Python Style Guide*. https://google.github.io/styleguide/pyguide.html

[8] Astral Software. (2024). *uv: An extremely fast Python package installer and resolver*. https://astral.sh/blog/uv

[9] W3C Web Accessibility Initiative. (2018). *WCAG 2.1 Quick Reference*. https://www.w3.org/WAI/WCAG21/quickref/

[10] OWASP Foundation. (2021). *Deserialization Cheat Sheet*. https://cheatsheetseries.owasp.org/cheatsheets/Deserialization_Cheat_Sheet.html

[11] Yelp Engineering. (2024). *detect-secrets: Preventing secrets in source code*. https://github.com/Yelp/detect-secrets

[12] CycloneDX Project. (2024). *CycloneDX: OWASP Software Bill of Materials standard*. https://cyclonedx.org/

[13] OWASP Foundation. (2021). *OWASP Top Ten 2021*. https://owasp.org/www-project-top-ten/

[14] European Parliament. (2016). *GDPR Article 25: Data protection by design and by default*. https://gdpr-info.eu/art-25-gdpr/

[15] Conventional Commits contributors. (2019). *Conventional Commits 1.0.0*. https://www.conventionalcommits.org/en/v1.0.0/

[16] SmartBear Software. (2011). *Best Practices for Peer Code Review* (Cisco study: optimal PR size ≤ 400 LOC). https://smartbear.com/learn/code-review/best-practices-for-peer-code-review/

[17] Martin, R. C. (2000). *Design Principles and Design Patterns*. Object Mentor. https://en.wikipedia.org/wiki/SOLID

---

## Recommended Toolchain Summary

| Tool | Purpose | Enforcement |
|---|---|---|
| **Black** | Python formatting | pre-commit + CI (block merge) |
| **Ruff** | Python linting + isort + security (bandit) | pre-commit + CI (block merge) |
| **mypy --strict** | Python static type checking | CI (block merge) |
| **pytest + pytest-cov** | Test runner + coverage | CI (80% floor, block merge) |
| **pip-audit** | Python CVE scanning | CI (block on HIGH+) |
| **detect-secrets** | Secrets scanning | pre-commit (block commit) |
| **uv** | Dependency management + venv | Developer tooling |
| **ESLint + Prettier** | JS linting + formatting | pre-commit + CI |
| **Dependabot** | Automated dep updates | GitHub Actions |

---

*This document is a research draft. Every citation has been verified to the primary source. Statistics, standards numbers, and external claims are sourced; the project's own positions and recommendations are original and do not require citations.*
