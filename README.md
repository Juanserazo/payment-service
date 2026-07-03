# Payment Service

A modern asynchronous payment processing service built with **FastAPI**, **SQLAlchemy Async**, and **Hexagonal Architecture**.

This project demonstrates clean architecture principles, idempotent payment processing, retry mechanisms for transient failures, and provider abstraction.

---

## Features

- ✅ Create payments
- ✅ Retrieve payment details
- ✅ Refund approved payments
- ✅ Idempotency support
- ✅ Retry with exponential backoff
- ✅ Async database access
- ✅ Provider abstraction
- ✅ Dependency Injection
- ✅ OpenAPI / Swagger documentation
- ✅ Hexagonal Architecture

---

## Architecture

```text
app/
├── api/
│   └── payment_routes.py
│
├── application/
│   └── use_cases/
│       ├── create_payment.py
│       ├── get_payment.py
│       └── refund_payment.py
│
├── config/
│   ├── dependencies.py
│   └── settings.py
│
├── domain/
│   ├── entities/
│   │   └── payment.py
│   │
│   ├── enums/
│   │   └── payment_status.py
│   │
│   ├── exceptions/
│   │   └── payment_exceptions.py
│   │
│   └── ports/
│       ├── payment_provider_port.py
│       └── payment_repository_port.py
│
├── infrastructure/
│   ├── database/
│   │   ├── base.py
│   │   ├── models/
│   │   │   └── payment_model.py
│   │   └── session.py
│   │
│   ├── providers/
│   │   └── mock_payment_provider.py
│   │
│   └── repositories/
│       ├── payment_mapper.py
│       └── sqlalchemy_payment_repository.py
│
├── schemas/
│   └── payment.py
│
└── main.py
```

---

## Design Principles

### Hexagonal Architecture

The application is divided into three main layers:

### Domain

Contains business entities, ports, enums, and exceptions.

The domain has no dependencies on frameworks or infrastructure.

### Application

Contains use cases responsible for orchestrating business flows.

### Infrastructure

Contains implementations of repositories, database models, and external providers.

---

## Design Decisions

### Hexagonal Architecture

**Decision:** Adopt hexagonal (ports and adapters) architecture.

**Rationale:**
- Separates business logic from technical concerns
- Makes the codebase testable by allowing mock implementations
- Facilitates switching providers (Stripe, PayPal, etc.) without changing business logic
- Domain layer remains framework-agnostic

### Async/Await Throughout

**Decision:** Use async/await for all I/O operations (database, external providers).

**Rationale:**
- Improves performance under concurrent load
- Non-blocking operations allow handling more requests
- Aligns with FastAPI's async-first design
- SQLAlchemy 2.0 has excellent async support

### Idempotency Keys

**Decision:** Require idempotency keys for all payment creation requests.

**Rationale:**
- Prevents duplicate charges from network retries
- Ensures exactly-once semantics for payment operations
- Clients can safely retry failed requests without side effects
- Industry standard for payment APIs (Stripe, PayPal)

### Retry with Exponential Backoff

**Decision:** Automatically retry provider timeouts with exponential backoff (3 attempts, 1-8s delays).

**Rationale:**
- Transient network failures are common in payment processing
- Reduces false negatives from temporary issues
- Exponential backoff prevents overwhelming the provider
- Only retries timeouts, not business errors (declined cards, insufficient funds)

### Provider Abstraction

**Decision:** Define a `PaymentProviderPort` interface with mock implementation.

**Rationale:**
- Decouples business logic from specific payment providers
- Enables easy switching between providers (Stripe, PayPal, etc.)
- Simplifies testing with deterministic mock responses
- Allows A/B testing different providers in production

### SQLAlchemy Async with Alembic

**Decision:** Use SQLAlchemy 2.0 async with Alembic for migrations.

**Rationale:**
- Type-safe ORM with excellent async support
- Database-agnostic queries (easy migration from SQLite to PostgreSQL)
- Alembic provides version-controlled schema migrations
- Async engine prevents blocking the event loop

### SQLite for Development

**Decision:** Use SQLite for local development and testing.

**Rationale:**
- Zero configuration - no database server required
- Single file database - easy to reset and version control
- Sufficient for development and small-scale deployments
- Can easily migrate to PostgreSQL for production

### Poetry for Dependency Management

**Decision:** Use Poetry instead of pip/requirements.txt.

**Rationale:**
- Lock file ensures reproducible builds
- Virtual environment management built-in
- Better dependency resolution than pip
- Standard tool in modern Python ecosystem

### FastAPI

**Decision:** Use FastAPI as the web framework.

**Rationale:**
- Native async support
- Automatic OpenAPI/Swagger documentation
- Type hints for request/response validation
- High performance (comparable to Go/Node.js)
- Excellent developer experience

---

## Payment Lifecycle

```text
PENDING
   │
   ├── APPROVED
   │       │
   │       └── REFUNDED
   │
   └── DECLINED
```

---

## Idempotency

To prevent duplicate payment processing, every payment request requires an idempotency key.

### Example

```http
Idempotency-Key: payment-123
```

If the same request is submitted multiple times using the same key, the existing payment will be returned instead of creating a new one.

---

## Retry Strategy

Transient provider failures are automatically retried using Tenacity.

### Configuration

```python
@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(
        multiplier=1,
        min=1,
        max=8,
    ),
)
```

Only timeout-related failures are retried.

Business errors such as:

- Card declined
- Insufficient funds

are returned immediately.

---

## API Endpoints

### Create Payment

```http
POST /payments
```

#### Headers

```http
Idempotency-Key: payment-001
```

#### Body

```json
{
  "amount": 100,
  "currency": "USD"
}
```

---

### Get Payment

```http
GET /payments/{payment_id}
```

---

### Refund Payment

```http
POST /payments/{payment_id}/refund
```

#### Body

```json
{
  "amount": 100
}
```

---

## Error Simulation

The mock provider supports deterministic testing.

### Card Declined

```json
{
  "amount": 400,
  "currency": "USD"
}
```

### Provider Timeout

```json
{
  "amount": 500,
  "currency": "USD"
}
```

### Insufficient Funds

```json
{
  "amount": 600,
  "currency": "USD"
}
```

---

## Getting Started for Developers

### Prerequisites

- Python 3.12+
- Poetry (install from https://python-poetry.org/docs/#installation)
- Docker and Docker Compose (optional, for containerized deployment)

### Setup

1. **Clone the repository:**

```bash
git clone <repository-url>
cd payment-service
```

2. **Install dependencies:**

```bash
poetry install
```

This installs all dependencies including development tools (pytest, ruff, etc.)

3. **Activate the virtual environment:**

```bash
poetry shell
```

### Running Tests

```bash
poetry run pytest
```

For coverage report:

```bash
poetry run pytest --cov=app --cov-report=html
```

### Running the Application

#### Local Development

```bash
poetry run uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

#### Docker

Build and run with Docker Compose:

```bash
docker-compose up --build
```

The service will be available at `http://localhost:8000`

### Code Quality

Format code:

```bash
poetry run ruff format .
```

Lint code:

```bash
poetry run ruff check .
```

---

## Database Migrations

This project uses Alembic for database schema management.

### Generate a New Migration

After making changes to your SQLAlchemy models:

```bash
poetry run alembic revision --autogenerate -m "Description of changes"
```

### Apply Migrations

To apply pending migrations:

```bash
poetry run alembic upgrade head
```

### Rollback Migrations

To rollback to the previous migration:

```bash
poetry run alembic downgrade -1
```

To rollback to a specific migration:

```bash
poetry run alembic downgrade <revision_id>
```

### View Migration History

```bash
poetry run alembic history
```

### View Current Migration Status

```bash
poetry run alembic current
```

---

## Swagger Documentation

```text
http://localhost:8000/docs
```

---

## Health Check

### Request

```http
GET /health
```

### Response

```json
{
  "status": "healthy"
}
```

---

## Technology Stack

- Python 3.12
- FastAPI
- SQLAlchemy Async
- SQLite
- Poetry
- Tenacity
- Pydantic v2
- Uvicorn

---

## Future Improvements

- Structured logging
- Observability
- PostgreSQL support
- Real payment provider integration

---

## Author

**Juan Sebastian Erazo Chamorro**

Systems Engineer