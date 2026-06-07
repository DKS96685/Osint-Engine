# 🕵️‍♂️ OSINT Engine

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-009688.svg)
![Celery](https://img.shields.io/badge/Celery-5.3+-37814A.svg)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-336791.svg)
![Redis](https://img.shields.io/badge/Redis-7-DC382D.svg)
![Docker](https://img.shields.io/badge/Docker-Ready-2496ED.svg)

A high-performance, asynchronous Open Source Intelligence (OSINT) reconnaissance engine backend.

This project provides a robust, distributed architecture for submitting, queuing, and processing long-running security scans (like Nmap or DNS enumeration) without blocking the main web server. 

## 🏗️ Architecture

The engine is built on a highly scalable task queue system:
* **The Web API (FastAPI):** Handles incoming HTTP requests, validates payloads, and immediately returns a tracking Job ID.
* **The Message Broker (Redis):** Acts as the middleman queue, holding onto pending scan tasks safely until a worker is ready.
* **The Background Workers (Celery):** Constantly monitors Redis, picks up pending tasks, and executes the heavy OSINT scanning logic asynchronously.
* **The Database (PostgreSQL):** Stores the state of all jobs (`pending`, `processing`, `completed`) and their final results, managed via SQLAlchemy.

## 📂 Project Structure

```text
osint-engine/
├── docker-compose.yml      # Infrastructure setup (Postgres + Redis)
├── requirements.txt        # Python dependencies
└── src/
    ├── api/
    │   └── main.py         # FastAPI application & endpoints
    ├── workers/
    │   └── tasks.py        # Celery background tasks & configuration
    ├── database.py         # PostgreSQL connection management
    ├── model.py            # SQLAlchemy database tables
    └── schemas.py          # Pydantic data validation rules
