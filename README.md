# FastAPI Boilerplate

A clean and scalable **FastAPI** project template following the **Clean Architecture** principles.
This boilerplate is structured for real-world applications with support for background tasks, caching, CI/CD, database
migrations, and containerized deployment.

---

## ✨ Features

- 🚀 **FastAPI** – High-performance web framework ready for production
- 🧱 **Clean Architecture** – Modular structure with clear separation of domain and use cases
- 🛢️ **Database Layer** – `SQLAlchemy` + `PostgreSQL` with Alembic migrations
- 🧪 **Test-Ready** – Built-in `pytest` support with parallel test execution
- 🧵 **Asynchronous Task Queue** – Background processing with `Celery` & `Redis`
- 🌍 **Internationalization** – Multi-language support using `Babel` & `gettext`
- 📦 **Dependency Management** – Lightweight and fast using `uv`
- 🎯 **Code Quality** – Auto-formatting and linting via `Ruff` & `pre-commit` hooks
- 🔁 **CI/CD Integration** – Automated workflows using `GitHub Actions`
- 🐳 **Containerized Deployment** – `Docker` & `Kubernetes` support out of the box
- ☁️ **Google Cloud** – Integrated cloud services via `Google Cloud`

---

## 🧩 Technologies

<div align="center">
    <code><img width="50" src="https://cdn.simpleicons.org/fastapi" alt="FastAPI" title="FastAPI" /></code>
    <code><img width="50" src="https://cdn.simpleicons.org/sqlalchemy" alt="SQLAlchemy" title="SQLAlchemy" /></code>
    <code><img width="50" src="https://cdn.simpleicons.org/pytest" alt="pytest" title="pytest" /></code>
    <code><img width="50" src="https://cdn.simpleicons.org/celery" alt="Celery" title="Celery" /></code>
    <code><img width="50" src="https://cdn.simpleicons.org/redis" alt="Redis" title="Redis" /></code>
    <code><img width="50" src="https://cdn.simpleicons.org/postgresql" alt="PostgreSQL" title="PostgreSQL" /></code>
    <code><img width="50" src="https://cdn.simpleicons.org/babel" alt="Babel" title="Babel" /></code>
    <code><img width="50" src="https://cdn.simpleicons.org/uv" alt="uv" title="uv" /></code>
    <code><img width="50" src="https://cdn.simpleicons.org/ruff" alt="Ruff" title="Ruff" /></code>
</div>

<div align="center">
    <code><img width="50" src="https://cdn.simpleicons.org/docker" alt="Docker" title="Docker" /></code>
    <code><img width="50" src="https://cdn.simpleicons.org/kubernetes" alt="Kubernetes" title="Kubernetes" /></code>
    <code><img width="50" src="https://cdn.simpleicons.org/googlecloud" alt="Google Cloud" title="Google Cloud" /></code>
</div>

---

## 🧱 Architecture Overview

This project follows a **4-layer Clean Architecture** pattern that emphasizes separation of concerns, testability, and
scalability.

      +---------------------+
      |    Presentation     |  (FastAPI, gRPC, CLI, etc.)
      +---------------------+
                 ↓
      +---------------------+
      |     Application     |  (Use Cases, Services)
      +---------------------+
                 ↓
      +---------------------+
      |       Domain        |  (Entities, Value Objects, Interfaces)
      +---------------------+
                 ↑
      +---------------------+
      |   Infrastructure    |  (DB, Email, External APIs, Logging)
      +---------------------+

---

## 📁 Project Structure

```text
app/
├── presentation/
│   ├── api/                            # API endpoints
│   └── dependency/                     # Dependencies (DB session, auth, HTTP clients, etc.)
│
├── application/
│   ├── dto/                            # Data Transfer Objects
│   ├── use_case/                       # Use cases (Interactors)
│   └── service/                        # Services (Business logic)
│
├── domain/
│   ├── entity/                         # Entities (Domain models)
│   ├── value_object/                   # Value Objects (Immutable types)
│   └── repository/                     # Repositories (Interfaces for data access)
│
├── infrastructure/
│   ├── cmd/                            # Command line scripts
│   ├── config/                         # Configuration files
│   ├── db/                             # Database configuration, models, and repository implementations
│   ├── helper/                         # Helper functions for infrastructure
│   ├── http/                           # HTTP configuration
│   ├── locale/                         # Internationalization and translation files
│   ├── smtp/                           # SMTP/email service configuration
│   ├── task/                           # Celery/Task queue configuration
│   └── template/                       # Template HTML files
│
└── main.py                             # Application entry point
```

> ⚠️ **Note**
>
> To keep things practical for small-to-medium projects, we apply some pragmatic trade-offs:
>
> - The Application layer **implements** DTOs (Pydantic models) and the Presentation layer **re-uses** those DTOs.  <br>
    → Avoids redundant class declarations and mapping logic
>
>
> - The **Domain layer includes concrete SQLAlchemy models and repositories**  <br>
    → Eliminates the need for interface abstractions  <br>
    → Still keeps business logic encapsulated within the domain
>
> These choices balance architectural clarity with development speed and maintainability.


---

## 🛠️ Setup Instructions

```bash
make
```

---

## 🚀 Run the Application

```bash
make local
make dev
```

---

## 🧪 Run the Tests

```bash
make test
```

---

## 🐳 Docker Deployment

```bash
make deploy
```

---

## 🧬 Database Migration

```bash
# Create a new migration
make db-revision msg="your_message_here"

# Apply migrations
make db-upgrade

# Downgrade last migration
make db-downgrade
```

---

## 🌍 Localization

```bash
# Initialize new language (e.g., French)
make translations-init lang=fr

# Update existing translations
make translations-update

# Compile translations
make translations-compile
```

---

## 📄 License

Distributed under the [MIT License](./LICENSE).  <br>
Feel free to use, modify, and distribute this project.
