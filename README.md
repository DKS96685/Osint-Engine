# 🕵️‍♂️ OSINT Engine

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-009688.svg)
![Celery](https://img.shields.io/badge/Celery-5.3+-37814A.svg)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-336791.svg)
![Redis](https://img.shields.io/badge/Redis-7-DC382D.svg)
![Docker](https://img.shields.io/badge/Docker-Ready-2496ED.svg)

A high-performance, asynchronous Open Source Intelligence (OSINT) reconnaissance engine backend.

This project provides a robust, distributed architecture designed for cybersecurity researchers and penetration testers. It manages the submission, queuing, and execution of long-running security scans (such as DNS enumeration, port scanning, and social media reconnaissance) without blocking the main web server, ensuring a highly responsive user experience.

---

## ✨ Key Features

* **Asynchronous Execution:** Offloads heavy OSINT tasks to background workers, keeping the REST API lightning-fast.
* **Job Tracking:** Real-time status updates (`pending`, `processing`, `completed`, `failed`) for every submitted scan.
* **Data Persistence:** Safely stores all targets, scan configurations, and final JSON outputs in a relational database.
* **Scalable Worker Pools:** Easily spin up additional Celery workers across multiple machines to handle hundreds of concurrent scans.
* **Containerized Infrastructure:** One-command setup for the message broker and database using Docker Compose.

---

## 🏗️ Architecture

The engine is built on a highly scalable task queue system separating the web layer from the processing layer:

1. **The Web API (FastAPI):** Handles incoming HTTP requests, validates target payloads using Pydantic, and immediately returns a tracking Job ID.
2. **The Message Broker (Redis):** Acts as the high-speed middleman queue. It safely holds onto pending scan tasks until a worker is available to process them.
3. **The Background Workers (Celery):** Constantly monitors Redis, picks up pending tasks, executes the heavy OSINT scanning logic (e.g., executing Nmap, Sherlock, or custom Python scripts), and pushes the results.
4. **The Database (PostgreSQL):** The source of truth. Stores the state of all jobs and their final analytical results, securely managed via SQLAlchemy ORM.

---

## 📂 Project Structure

```text
osint-engine/
├── docker-compose.yml      # Infrastructure setup (Postgres + Redis instances)
├── requirements.txt        # Python package dependencies
└── src/
    ├── api/
    │   └── main.py         # FastAPI application, routing, and REST endpoints
    ├── workers/
    │   └── tasks.py        # Celery background tasks & OSINT tool integrations
    ├── database.py         # PostgreSQL connection pooling and session management
    ├── model.py            # SQLAlchemy database table definitions
    └── schemas.py          # Pydantic data validation rules for API requests/responses
