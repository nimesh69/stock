# 📈 Stock Market Application

A full-stack stock market application for collecting, processing, categorizing, and analyzing Nepalese stock-market data.

The project combines:

* 🐍 **Django / Django REST Framework** backend
* ⚛️ **Frontend application**
* 🐳 **Docker Compose** development environment
* 🗄️ Database-backed stock and news data
* 🕷️ ShareSansar-based data crawling
* 📰 Automated news categorization using a hybrid approach
* 📊 Buyer & seller behavior analysis
* 🔌 REST API with Swagger and ReDoc documentation

---

## 📑 Table of Contents

* [🚀 Quick Start](#-quick-start)
* [📋 Prerequisites](#-prerequisites)
* [📥 Clone the Project](#-clone-the-project)
* [💻 Open in VS Code](#-open-in-vs-code)
* [🔐 Environment Configuration](#-environment-configuration)
* [🐍 Backend Setup](#-backend-setup)
* [⚛️ Frontend Setup](#-frontend-setup)
* [🐳 Start with Docker Compose](#-start-with-docker-compose)
* [👤 Create Django Superuser](#-create-django-superuser)
* [🌐 Application URLs](#-application-urls)
* [🗄️ Database Schema](#-database-schema)
* [🕷️ Data Crawling & Collection](#-data-crawling--collection)
* [📰 Automatic News Categorization](#-automatic-news-categorization)
* [📊 Buyer & Seller Behavior Analysis](#-buyer--seller-behavior-analysis)
* [🏗️ Project Architecture](#-project-architecture)
* [🔄 Data Flow](#-data-flow)
* [🧰 Useful Commands](#-useful-commands)
* [🛠️ Development Workflow](#-development-workflow)
* [📚 Technical Documentation](#-technical-documentation)
* [🐛 Troubleshooting](#-troubleshooting)

---

# 🚀 Quick Start

If your development environment is already configured, the basic workflow is:

```bash
git clone https://github.com/nimesh69/stock.git
cd stock
```

Configure the required `.env` files using the corresponding `.env.example` files.

Then:

```bash
cd backend

python3.12 -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt

cd ../frontend
npm install

cd ..
docker compose up
```

Create an admin user:

```bash
docker compose exec web python manage.py createsuperuser
```

Then open:

| Service         | URL                                            |
| --------------- | ---------------------------------------------- |
| 🌐 Frontend     | http://localhost:3000/                         |
| 🔐 Django Admin | http://localhost:8000/admin/                   |
| 📖 Swagger UI   | http://localhost:8000/api/schema/swagger-ui/#/ |
| 📚 ReDoc        | http://localhost:8000/api/schema/redoc/        |

---

# 📋 Prerequisites

Make sure the following tools are installed before starting.

* Git
* Python 3.12
* Node.js
* npm
* Docker
* Docker Compose
* Visual Studio Code

Verify your installation:

```bash
git --version
python3.12 --version
node --version
npm --version
docker --version
docker compose version
```

---

# 📥 Clone the Project

Clone the repository:

```bash
git clone https://github.com/nimesh69/stock.git
```

Move into the project:

```bash
cd stock
```

The repository is available at:

https://github.com/nimesh69/stock

---

# 💻 Open in VS Code

From the project root:

```bash
code .
```

If the `code` command is not available, open Visual Studio Code manually and select:

```text
File → Open Folder → stock
```

---

# 🔐 Environment Configuration

The application uses environment variables for configuration.

There are `.env.example` files that should be used as templates.

## Root Environment

From the project root, locate:

```text
.env.example
```

Create:

```text
.env
```

and configure the required values.

Example workflow:

```bash
cp .env.example .env
```

> Do not commit `.env` files containing secrets, passwords, API keys, or production credentials.

---

# 🐍 Backend Setup

Navigate to the backend:

```bash
cd backend
```

## Create Python Virtual Environment

The project uses Python 3.12:

```bash
python3.12 -m venv .venv
```

Activate the virtual environment.

### Linux / macOS

```bash
source .venv/bin/activate
```

### Windows

```powershell
.venv\Scripts\activate
```

Your terminal should now indicate that the virtual environment is active.

---

## Install Backend Dependencies

Install the required Python packages:

```bash
pip install -r requirements.txt
```

---

## Backend Environment Variables

Check the backend environment template:

```text
backend/.env.example
```

Create the corresponding `.env` file:

```bash
cp .env.example .env
```

Configure the required backend settings.

Depending on the environment, these may include:

* Database configuration
* Django secret key
* Debug configuration
* Allowed hosts
* External service credentials
* Crawling-related configuration
* Other application-specific settings

---

# ⚛️ Frontend Setup

Navigate to the frontend:

```bash
cd ../frontend
```

Install JavaScript dependencies:

```bash
npm install
```

---

## Frontend Environment Variables

Check:

```text
frontend/.env.example
```

Create the required `.env` file:

```bash
cp .env.example .env
```

Configure the frontend environment variables according to the example file.

Typical frontend configuration may include the backend/API base URL and other frontend-specific settings.

---

# 🐳 Start with Docker Compose

Return to the project root:

```bash
cd ..
```

Start the application:

```bash
docker compose up
```

For detached/background mode:

```bash
docker compose up -d
```

To rebuild containers after dependency or Docker configuration changes:

```bash
docker compose up --build
```

To stop the services:

```bash
docker compose down
```

---

# 👤 Create Django Superuser

Once the backend container is running, create a Django administrator account:

```bash
docker compose exec web python manage.py createsuperuser
```

Follow the prompts to configure:

```text
Username
Email
Password
```

The account can then be used to access Django Admin.

---

# 🌐 Application URLs

Once the application is running, the main interfaces are available here.

## Frontend

**Application**

http://localhost:3000/

---

## Django Admin

**Administration panel**

http://localhost:8000/admin/

Use the superuser credentials created with:

```bash
docker compose exec web python manage.py createsuperuser
```

---

## Swagger UI

Interactive API documentation:

http://localhost:8000/api/schema/swagger-ui/#/

Swagger allows developers to:

* Browse available API endpoints
* Inspect request parameters
* Inspect response schemas
* Test API endpoints
* Understand authentication requirements

---

## ReDoc

Alternative API documentation:

http://localhost:8000/api/schema/redoc/

ReDoc provides a cleaner documentation-oriented view of the API schema.

---

# 🗄️ Database Schema

The database contains the application's core stock-market, news, and analytical data structures.

The database schema diagram should be maintained alongside the project documentation so developers can understand:

```text
Users
  │
  ├── Authentication / Administration
  │
Stock Data
  │
  ├── Companies
  ├── Prices
  ├── Market Information
  │
News
  │
  ├── Articles
  ├── Categories
  └── Classification Metadata
  │
Market Analysis
  │
  ├── Buyer Behavior
  ├── Seller Behavior
  └── Market Pressure Indicators
```





### Database Visual Architecture (ERD)
[![Database ERD](/backend/docs/Untitled.png)](/backend/docs/Untitled.png)


---

# 🕷️ Data Crawling & Collection

The application uses **ShareSansar** as the primary external source for both:

* 📈 Stock price information
* 📰 News information

The crawling and automation pipeline is documented in detail inside the backend documentation.

## ShareSansar News Spider

Documentation:

```text
backend/docs/ShareSansar News Spider Documentation.md
```

This document explains the news crawling process, including the approach used to collect news from ShareSansar.

---

## Stock App Scraping & Automation Pipeline

Documentation:

```text
backend/docs/Stock App Scraping & Automation Pipeline.md
```

This document describes the stock-data scraping and automation pipeline.

The overall collection process can be viewed as:

```text
ShareSansar
     │
     ├───────────────┐
     │               │
     ▼               ▼
Stock Prices       News
     │               │
     ▼               ▼
Data Processing   Categorization
     │               │
     └───────┬───────┘
             ▼
          Database
             │
             ▼
       Backend APIs
             │
             ▼
         Frontend
```

---

# 📰 Automatic News Categorization

The application uses a **hybrid approach** for automatic news categorization.

Instead of relying exclusively on a single classification technique, the system combines multiple signals/approaches to determine the appropriate category for an article.

The complete technical explanation is available here:

```text
backend/docs/article_categorization_approach.md
```

## Categorization Pipeline

Conceptually:

```text
Collected Article
       │
       ▼
Text Processing
       │
       ▼
Feature / Signal Extraction
       │
       ▼
Hybrid Classification
       │
       ▼
News Category
       │
       ▼
Stored in Database
```

For the complete implementation details, assumptions, rules, and methodology, refer to:

```text
backend/docs/article_categorization_approach.md
```

---

# 📊 Buyer & Seller Behavior Analysis

The application also analyzes buyer and seller behavior to derive market-pressure information.

The complete technical documentation is available here:

```text
backend/docs/Behavior Summary & Market Pressure Indicator — Technical Documentation.md
```

The analytical flow can be represented as:

```text
Market Transactions / Trading Data
              │
              ▼
      Buyer/Seller Analysis
              │
       ┌──────┴──────┐
       ▼             ▼
   Buyer Side     Seller Side
       │             │
       └──────┬──────┘
              ▼
      Behavior Summary
              │
              ▼
   Market Pressure Indicator
              │
              ▼
          API / UI
```

This component is intended to help interpret market activity beyond simply displaying price data.

---

# 🏗️ Project Architecture

At a high level, the project consists of three major layers.

```text
┌─────────────────────────────────────────────┐
│                  FRONTEND                   │
│                                             │
│  User Interface                             │
│  Market Data                                │
│  News                                       │
│  Analysis                                   │
└──────────────────────┬──────────────────────┘
                       │
                       │ HTTP / REST API
                       ▼
┌─────────────────────────────────────────────┐
│                   BACKEND                   │
│                                             │
│  Django                                    │
│  Django REST Framework                     │
│  Business Logic                             │
│  Authentication                             │
│  Data Processing                            │
│  Analytics                                  │
└──────────────────────┬──────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────┐
│                  DATABASE                   │
│                                             │
│  Stocks                                    │
│  Prices                                     │
│  News                                       │
│  Categories                                 │
│  Analysis Data                              │
└─────────────────────────────────────────────┘

                       ▲
                       │
                 Data Collection
                       │
             ┌─────────┴─────────┐
             │                   │
             ▼                   ▼
        ShareSansar          Automation
```

---

# 🔄 End-to-End Data Flow

The application's overall workflow can be understood as:

### 1. Data Collection

ShareSansar is used as the external source for stock-price and news information.

```text
ShareSansar
     │
     ├── Stock Prices
     │
     └── News
```

### 2. Data Processing

Collected information is processed before being persisted.

```text
Raw Data
   │
   ▼
Validation
   │
   ▼
Normalization
   │
   ▼
Database
```

### 3. News Classification

News articles pass through the hybrid categorization process.

```text
News Article
     │
     ▼
Categorization Pipeline
     │
     ▼
Category
     │
     ▼
Database
```

### 4. Market Analysis

Trading information is analyzed to summarize buyer/seller behavior and market pressure.

```text
Market Data
     │
     ▼
Behavior Analysis
     │
     ▼
Market Pressure
```

### 5. API

The Django backend exposes processed information through REST APIs.

```text
Database
    │
    ▼
Django
    │
    ▼
REST API
    │
    ▼
Frontend
```

---

# 🧰 Useful Commands

## Backend

Activate the virtual environment:

```bash
source backend/.venv/bin/activate
```

Install dependencies:

```bash
pip install -r backend/requirements.txt
```

---

## Docker

Start services:

```bash
docker compose up
```

Start in background:

```bash
docker compose up -d
```

Rebuild:

```bash
docker compose up --build
```

Stop:

```bash
docker compose down
```

View running containers:

```bash
docker compose ps
```

View logs:

```bash
docker compose logs
```

Follow logs:

```bash
docker compose logs -f
```

Follow only the web service:

```bash
docker compose logs -f web
```

---

## Django

Run migrations:

```bash
docker compose exec web python manage.py migrate
```

Create migrations:

```bash
docker compose exec web python manage.py makemigrations
```

Create a superuser:

```bash
docker compose exec web python manage.py createsuperuser
```

Open Django shell:

```bash
docker compose exec web python manage.py shell
```

---

# 🛠️ Development Workflow

A recommended development workflow is:

```text
1. Pull latest code
       │
       ▼
2. Configure environment
       │
       ▼
3. Install/update dependencies
       │
       ▼
4. Start Docker services
       │
       ▼
5. Run migrations
       │
       ▼
6. Create/update superuser
       │
       ▼
7. Verify API
       │
       ▼
8. Verify frontend
       │
       ▼
9. Run/test data pipelines
       │
       ▼
10. Develop and commit changes
```

---

# 📚 Technical Documentation

The project contains dedicated documentation for its major data and analytical components.

| Area                           | Documentation                                                                            |
| ------------------------------ | ---------------------------------------------------------------------------------------- |
| 📰 ShareSansar News Spider     | `backend/docs/ShareSansar News Spider Documentation.md`                                  |
| 📈 Stock Scraping & Automation | `backend/docs/Stock App Scraping & Automation Pipeline.md`                               |
| 🧠 News Categorization         | `backend/docs/article_categorization_approach.md`                                        |
| 📊 Buyer/Seller Behavior       | `backend/docs/Behavior Summary & Market Pressure Indicator — Technical Documentation.md` |

### Documentation Directory

```text
backend/
└── docs/
    ├── ShareSansar News Spider Documentation.md
    ├── Stock App Scraping & Automation Pipeline.md
    ├── article_categorization_approach.md
    └── Behavior Summary & Market Pressure Indicator — Technical Documentation.md
```

---

# 🐛 Troubleshooting

## Docker containers do not start

Check the container status:

```bash
docker compose ps
```

Inspect logs:

```bash
docker compose logs -f
```

If configuration or dependencies changed, rebuild:

```bash
docker compose up --build
```

---

## Backend dependency problems

Make sure Python 3.12 is being used:

```bash
python3.12 --version
```

Recreate the virtual environment if necessary:

```bash
rm -rf backend/.venv

python3.12 -m venv backend/.venv

source backend/.venv/bin/activate

pip install -r backend/requirements.txt
```

---

## Frontend dependency problems

From the frontend directory:

```bash
cd frontend
npm install
```

If the dependency installation is corrupted, remove the installed dependencies and reinstall:

```bash
rm -rf node_modules
npm install
```

---

## Django Admin is unavailable

Check whether the backend container is running:

```bash
docker compose ps
```

Then inspect the web logs:

```bash
docker compose logs -f web
```

Make sure migrations have been applied:

```bash
docker compose exec web python manage.py migrate
```

---

## API documentation is unavailable

Verify that the backend is running and then open:

```text
http://localhost:8000/api/schema/swagger-ui/#/
```

or:

```text
http://localhost:8000/api/schema/redoc/
```

---

# 🔒 Environment & Security

Never commit secrets to Git.

The following files should generally remain local:

```text
.env
backend/.env
frontend/.env
```

Use the example files as templates:

```text
.env.example
backend/.env.example
frontend/.env.example
```

Before deploying to production, review:

* Secret keys
* Database credentials
* Allowed hosts
* CORS configuration
* Debug mode
* API credentials
* External service credentials
* Docker configuration
* Database access permissions

---

# 📌 Important URLs

| Resource     | Address                                        |
| ------------ | ---------------------------------------------- |
| Frontend     | http://localhost:3000/                         |
| Django Admin | http://localhost:8000/admin/                   |
| Swagger UI   | http://localhost:8000/api/schema/swagger-ui/#/ |
| ReDoc        | http://localhost:8000/api/schema/redoc/        |

---

# 🧭 Project at a Glance

```text
                         STOCK APPLICATION
                                │
             ┌──────────────────┼──────────────────┐
             │                  │                  │
             ▼                  ▼                  ▼
        ShareSansar         Backend            Frontend
             │              Django               │
       ┌─────┴─────┐          │                  │
       │           │          ▼                  │
     Prices      News       REST API ◄───────────┘
       │           │          │
       │           ▼          │
       │    News Categorization
       │           │
       └─────┬─────┘
             │
             ▼
          Database
             │
             ▼
     Buyer/Seller Analysis
             │
             ▼
   Market Pressure Indicator
             │
             ▼
          Frontend
```

---

# 🎯 Getting Started Checklist

* [ ] Clone the repository
* [ ] Open the project in VS Code
* [ ] Configure root `.env`
* [ ] Configure `backend/.env`
* [ ] Configure `frontend/.env`
* [ ] Create Python 3.12 virtual environment
* [ ] Install backend requirements
* [ ] Install frontend dependencies
* [ ] Start Docker Compose
* [ ] Run database migrations if required
* [ ] Create Django superuser
* [ ] Verify Django Admin
* [ ] Verify Swagger UI
* [ ] Verify ReDoc
* [ ] Verify frontend
* [ ] Read the scraping pipeline documentation
* [ ] Read the news categorization documentation
* [ ] Read the buyer/seller behavior documentation

---

# 📖 Further Reading

For developers working on the data-engineering and analytics components, read the documentation in this order:

### 1. Data Collection

```text
ShareSansar News Spider Documentation.md
```

Understand how news is collected.

### 2. Stock Data Pipeline

```text
Stock App Scraping & Automation Pipeline.md
```

Understand how stock information is scraped and automated.

### 3. News Intelligence

```text
article_categorization_approach.md
```

Understand the hybrid news categorization system.

### 4. Market Intelligence

```text
Behavior Summary & Market Pressure Indicator — Technical Documentation.md
```

Understand buyer/seller behavior analysis and the market-pressure indicator.

---

## ⭐ Project Summary

This project provides a complete stock-market application workflow:

**Collect → Process → Categorize → Analyze → Expose through API → Visualize in Frontend**

It combines automated ShareSansar data collection, news intelligence, stock-market data processing, and buyer/seller behavior analysis into a single full-stack application.

For implementation-specific details, always refer to the documentation under:

```text
backend/docs/
```
