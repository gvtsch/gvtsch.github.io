# RAG Kit - Projekt Dokumentation

> Self-Hosted Hybrid RAG System als Docker-Paket

## Vision

Ein production-ready RAG-System, das Unternehmen in 10 Minuten auf eigener Infrastruktur deployen können. Kombiniert Vektor-Suche mit Knowledge Graph für präzisere Antworten.

---

## Architektur

```
┌─────────────────────────────────────────────────────────────────┐
│                        RAG Kit                                   │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                    Chainlit UI                           │   │
│  │                    (Port 8080)                           │   │
│  │                                                         │   │
│  │  • Chat Interface                                       │   │
│  │  • File Upload (Drag & Drop)                            │   │
│  │  • Source Citations                                     │   │
│  │  • Conversation History                                 │   │
│  │  • Admin/Diagnostics Panel                              │   │
│  └─────────────────────────────────────────────────────────┘   │
│                              │                                  │
│                              ▼                                  │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                    FastAPI Backend                       │   │
│  │                    (Internal)                            │   │
│  │                                                         │   │
│  │  • Document Processing Pipeline                         │   │
│  │  • Hybrid RAG Engine                                    │   │
│  │  • LLM Adapter Layer                                    │   │
│  │  • License Validation                                   │   │
│  │  • Caching Layer                                        │   │
│  └─────────────────────────────────────────────────────────┘   │
│                              │                                  │
│         ┌────────────────────┼────────────────────┐            │
│         ▼                    ▼                    ▼            │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐        │
│  │   Qdrant    │    │    Kuzu     │    │   SQLite    │        │
│  │  (Vectors)  │    │   (Graph)   │    │  (Metadata) │        │
│  └─────────────┘    └─────────────┘    └─────────────┘        │
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                    Redis (Optional)                      │   │
│  │                    (Caching)                             │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
                    ┌─────────────────┐
                    │   LLM Provider  │
                    │  (External)     │
                    │                 │
                    │  • OpenAI       │
                    │  • Azure        │
                    │  • Ollama       │
                    │  • Anthropic    │
                    └─────────────────┘
```

---

## Komponenten

### 1. Datenbanken

| Datenbank | Zweck | Warum diese? |
|-----------|-------|--------------|
| **Qdrant** | Vektor-Embeddings für Semantic Search | Schnell, self-hosted, gute API |
| **Kuzu** | Knowledge Graph für Entity Relations | Embedded (wie SQLite), keine separate DB nötig |
| **SQLite** | Metadata, Users, Sessions, Audit Log | Einfach, keine Konfiguration, persistent |
| **Redis** | Query Cache, Rate Limiting | Optional, für Performance |

### 2. Document Processing Pipeline

```
Document Upload
      │
      ▼
┌─────────────────┐
│  File Parser    │
│                 │
│  PDF  → pypdf   │
│  DOCX → python-docx
│  MD   → markdown│
│  TXT  → built-in│
│  CSV  → pandas  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Chunker        │
│                 │
│  • Semantic     │
│  • Overlap      │
│  • Max 512 tok  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Enrichment     │
│                 │
│  • Embeddings   │──────▶ Qdrant
│  • Entities     │──────▶ Kuzu
│  • Metadata     │──────▶ SQLite
└─────────────────┘
```

### 3. Hybrid RAG Query Engine

```
User Query
      │
      ▼
┌─────────────────┐
│  Query Router   │
│                 │
│  • Check Cache  │◀────── Redis
│  • Parse Intent │
└────────┬────────┘
         │
         ├──────────────────────────┐
         ▼                          ▼
┌─────────────────┐      ┌─────────────────┐
│  Vector Search  │      │  Graph Search   │
│                 │      │                 │
│  Top-K similar  │      │  Related        │
│  chunks         │      │  entities       │
└────────┬────────┘      └────────┬────────┘
         │                        │
         └───────────┬────────────┘
                     ▼
           ┌─────────────────┐
           │  Reranker       │
           │                 │
           │  Combine &      │
           │  Score results  │
           └────────┬────────┘
                    │
                    ▼
           ┌─────────────────┐
           │  LLM Generation │
           │                 │
           │  Answer with    │
           │  citations      │
           └────────┬────────┘
                    │
                    ▼
           ┌─────────────────┐
           │  Cache Result   │──────▶ Redis
           └─────────────────┘
```

### 4. LLM Adapter Layer

```python
# Abstraktion für verschiedene LLM Provider
class LLMAdapter(Protocol):
    def generate(self, prompt: str, **kwargs) -> str: ...
    def embed(self, texts: list[str]) -> list[list[float]]: ...

# Implementierungen
class OpenAIAdapter(LLMAdapter): ...
class AzureAdapter(LLMAdapter): ...
class OllamaAdapter(LLMAdapter): ...
class AnthropicAdapter(LLMAdapter): ...
```

### 5. Caching Strategie

| Cache Type | Was | TTL | Storage |
|------------|-----|-----|---------|
| **Query Cache** | Identische Fragen → gleiche Antwort | 1h | Redis |
| **Embedding Cache** | Text → Embedding | 24h | Redis |
| **Document Cache** | Parsed Documents | Permanent | Filesystem |
| **Session Cache** | Conversation History | Session | Redis/SQLite |

```python
# Caching Logic
def query(question: str) -> Answer:
    # 1. Check exact query cache
    cache_key = hash(question + user_id)
    if cached := redis.get(cache_key):
        return cached

    # 2. Check semantic similarity cache
    similar = find_similar_cached_queries(question, threshold=0.95)
    if similar:
        return similar.answer

    # 3. Execute query
    answer = rag_engine.query(question)

    # 4. Cache result
    redis.set(cache_key, answer, ttl=3600)
    return answer
```

---

## Feature Liste

### MVP (v1.0)

- [ ] **Document Processing**
  - [ ] PDF Parser (pypdf + pdfplumber für Tabellen)
  - [ ] DOCX Parser
  - [ ] Markdown Parser
  - [ ] TXT Parser
  - [ ] Semantic Chunking

- [ ] **Vector RAG**
  - [ ] Qdrant Integration
  - [ ] Embedding Generation
  - [ ] Similarity Search
  - [ ] Source Citations

- [ ] **Knowledge Graph**
  - [ ] Kuzu Integration
  - [ ] Entity Extraction (via LLM)
  - [ ] Relation Extraction
  - [ ] Graph Traversal für Multi-Hop Queries

- [ ] **LLM Integration**
  - [ ] OpenAI Adapter
  - [ ] Ollama Adapter (self-hosted)
  - [ ] Azure OpenAI Adapter
  - [ ] Anthropic Adapter

- [ ] **UI (Chainlit)**
  - [ ] Chat Interface
  - [ ] File Upload (Drag & Drop)
  - [ ] Source Citations Display
  - [ ] Conversation History

- [ ] **Infrastructure**
  - [ ] Docker Compose Setup
  - [ ] Health Checks
  - [ ] Startup Validation
  - [ ] Structured Logging

- [ ] **Licensing**
  - [ ] License Key Validation
  - [ ] Feature Gating (Free vs Paid)
  - [ ] Instance Tracking

### v1.1

- [ ] Query Caching (Redis)
- [ ] Embedding Caching
- [ ] Rate Limiting
- [ ] Admin Dashboard
- [ ] Usage Analytics
- [ ] CSV/XLSX Support

### v2.0

- [ ] Multi-User Support
- [ ] Role-Based Access Control
- [ ] API für externe Integration
- [ ] Branchen-Templates
- [ ] Graph Visualization
- [ ] Fine-tuning Support

---

## Tech Stack

| Komponente | Technologie | Version |
|------------|-------------|---------|
| **Language** | Python | 3.11+ |
| **UI** | Chainlit | Latest |
| **API** | FastAPI | 0.100+ |
| **Vector DB** | Qdrant | Latest |
| **Graph DB** | Kuzu | Latest |
| **Metadata DB** | SQLite | 3 |
| **Cache** | Redis | 7+ |
| **Embeddings** | OpenAI / Sentence-Transformers | - |
| **Container** | Docker + Compose | - |

### Python Dependencies

```
# Core
fastapi
uvicorn
chainlit
pydantic
pydantic-settings

# RAG
langchain
langchain-openai
langchain-community
qdrant-client
kuzu

# Document Processing
pypdf
pdfplumber
python-docx
markdown
pandas

# Caching
redis

# Utilities
httpx
python-dotenv
structlog
```

---

## Projekt Struktur

```
rag-kit/
├── docker-compose.yml
├── Dockerfile
├── .env.example
├── config.yml
├── LICENSE
├── README.md
│
├── app/
│   ├── __init__.py
│   ├── main.py                 # Chainlit Entry Point
│   ├── config.py               # Pydantic Settings
│   │
│   ├── api/
│   │   ├── __init__.py
│   │   ├── routes.py           # FastAPI Routes
│   │   └── health.py           # Health Checks
│   │
│   ├── core/
│   │   ├── __init__.py
│   │   ├── rag_engine.py       # Hybrid RAG Logic
│   │   ├── vector_store.py     # Qdrant Wrapper
│   │   ├── graph_store.py      # Kuzu Wrapper
│   │   └── reranker.py         # Result Fusion
│   │
│   ├── llm/
│   │   ├── __init__.py
│   │   ├── base.py             # LLM Protocol
│   │   ├── openai.py
│   │   ├── ollama.py
│   │   ├── azure.py
│   │   └── anthropic.py
│   │
│   ├── processing/
│   │   ├── __init__.py
│   │   ├── parser.py           # Document Parsers
│   │   ├── chunker.py          # Text Chunking
│   │   └── enricher.py         # Entity Extraction
│   │
│   ├── cache/
│   │   ├── __init__.py
│   │   └── redis_cache.py
│   │
│   ├── db/
│   │   ├── __init__.py
│   │   ├── models.py           # SQLAlchemy Models
│   │   └── session.py
│   │
│   ├── license/
│   │   ├── __init__.py
│   │   └── validator.py
│   │
│   └── ui/
│       ├── __init__.py
│       └── chainlit_app.py
│
├── data/                       # Persistent Data (Volume)
│   ├── qdrant/
│   ├── kuzu/
│   ├── sqlite/
│   └── documents/
│
├── docs/
│   ├── QUICKSTART.md
│   ├── CONFIGURATION.md
│   ├── TROUBLESHOOTING.md
│   └── API.md
│
├── scripts/
│   ├── validate.sh
│   ├── backup.sh
│   └── update.sh
│
└── tests/
    ├── __init__.py
    ├── test_parser.py
    ├── test_rag_engine.py
    └── test_llm_adapters.py
```

---

## Konfiguration

### .env.example

```bash
# License
LICENSE_KEY=RAG-XXXX-XXXX-XXXX
LICENSE_EMAIL=your@email.com

# LLM Provider (choose one)
LLM_PROVIDER=openai  # openai, ollama, azure, anthropic

# OpenAI
OPENAI_API_KEY=sk-...

# Ollama (self-hosted)
OLLAMA_BASE_URL=http://localhost:11434

# Azure OpenAI
AZURE_OPENAI_ENDPOINT=https://xxx.openai.azure.com
AZURE_OPENAI_API_KEY=...
AZURE_OPENAI_DEPLOYMENT=gpt-4

# Anthropic
ANTHROPIC_API_KEY=sk-ant-...

# Optional: Redis for Caching
REDIS_URL=redis://localhost:6379

# App Settings
LOG_LEVEL=INFO
MAX_UPLOAD_SIZE_MB=50
```

### config.yml

```yaml
# RAG Kit Configuration

app:
  name: "RAG Kit"
  host: "0.0.0.0"
  port: 8080

llm:
  provider: "${LLM_PROVIDER}"
  model: "gpt-4o-mini"
  temperature: 0.1
  max_tokens: 2000

embeddings:
  provider: "openai"  # or "local" for sentence-transformers
  model: "text-embedding-3-small"
  # For local:
  # provider: "local"
  # model: "all-MiniLM-L6-v2"

chunking:
  strategy: "semantic"  # or "fixed"
  max_chunk_size: 512
  overlap: 50

retrieval:
  vector_top_k: 10
  graph_depth: 2
  rerank: true
  rerank_top_k: 5

graph:
  enabled: true  # Requires paid license
  entity_extraction: true

cache:
  enabled: true
  ttl_seconds: 3600

documents:
  supported_formats:
    - pdf
    - docx
    - md
    - txt
  max_file_size_mb: 50
```

---

## Docker Compose

```yaml
version: '3.8'

services:
  rag:
    build: .
    ports:
      - "8080:8080"
    volumes:
      - ./data:/app/data
      - ./.env:/app/.env:ro
      - ./config.yml:/app/config.yml:ro
    environment:
      - QDRANT_HOST=qdrant
      - REDIS_URL=redis://redis:6379
    depends_on:
      qdrant:
        condition: service_healthy
      redis:
        condition: service_healthy
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8080/health"]
      interval: 30s
      timeout: 10s
      retries: 3
    restart: unless-stopped

  qdrant:
    image: qdrant/qdrant:latest
    volumes:
      - ./data/qdrant:/qdrant/storage
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:6333/health"]
      interval: 10s
      timeout: 5s
      retries: 3

  redis:
    image: redis:7-alpine
    volumes:
      - ./data/redis:/data
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 5s
      retries: 3
    # Optional: Disable if caching not needed
    profiles:
      - with-cache
```

---

## Pricing / Lizenzierung

### Modulares Pricing-Modell

Das System ist modular aufgebaut. Kunden kaufen ein **Base Package** und können **Add-Ons** hinzufügen.

#### Base Packages

| Package | Preis | Beschreibung |
|---------|-------|--------------|
| **Free** | 0€ | Zum Testen: 10 Docs, 50 Queries/Tag, Basic Vector RAG |
| **Core** | 299€ | Vollständiges Vector RAG, unbegrenzte Docs/Queries, 1 Jahr Updates |

#### Add-On Module

| Modul | Preis | Beschreibung | Abhängigkeit |
|-------|-------|--------------|--------------|
| **Graph RAG** | +199€ | Knowledge Graph, Entity Extraction, Multi-Hop Queries | Core |
| **Caching** | +99€ | Redis Integration, Query Cache, Embedding Cache | Core |
| **API Access** | +149€ | REST API für externe Integration, Webhooks | Core |
| **Multi-User** | +249€ | User Management, RBAC, Audit Log | Core |
| **OCR** | +99€ | Gescannte PDFs verarbeiten (Tesseract) | Core |
| **Web Scraper** | +149€ | URLs als Dokumentquelle, Auto-Refresh | Core |
| **Analytics** | +99€ | Usage Dashboard, Query Analytics, Export | Core |
| **Priority Support** | +199€/Jahr | 24h Response, Private Discord, Onboarding Call | Core |

#### Bundles (Rabattiert)

| Bundle | Module | Einzelpreis | Bundle-Preis | Ersparnis |
|--------|--------|-------------|--------------|-----------|
| **Starter** | Core | 299€ | **299€** | - |
| **Professional** | Core + Graph + Caching + API | 746€ | **599€** | 20% |
| **Business** | Core + Graph + Caching + API + Multi-User + Analytics | 1.094€ | **849€** | 22% |
| **Enterprise** | Alle Module + Priority Support | 1.541€ | **1.199€** | 22% |

#### Enterprise Add-Ons (Auf Anfrage)

| Add-On | Beschreibung |
|--------|--------------|
| **Unlimited Instances** | Keine Begrenzung der Instanzen |
| **Custom Branding** | Logo, Farben, Domain |
| **SSO Integration** | SAML, OIDC, Active Directory |
| **On-Premise Support** | Installation durch uns |
| **Custom Features** | Individuelle Entwicklung |
| **SLA** | Garantierte Response-Zeiten |

### Preisübersicht Visualisiert

```
┌─────────────────────────────────────────────────────────────────────┐
│                         RAG Kit Pricing                              │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  BASE                                                               │
│  ┌─────────────────┐    ┌─────────────────┐                        │
│  │     FREE        │    │     CORE        │                        │
│  │      0€         │    │     299€        │                        │
│  │                 │    │                 │                        │
│  │  • 10 Docs      │    │  • Unlimited    │                        │
│  │  • 50 Queries   │    │  • Vector RAG   │                        │
│  │  • Basic RAG    │    │  • 1 Jahr       │                        │
│  │                 │    │    Updates      │                        │
│  └─────────────────┘    └────────┬────────┘                        │
│                                  │                                  │
│  ADD-ONS (require Core)          │                                  │
│  ┌───────────────────────────────┼───────────────────────────────┐ │
│  │                               │                               │ │
│  │  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐         │ │
│  │  │ Graph    │ │ Caching  │ │ API      │ │ Multi-   │         │ │
│  │  │ RAG      │ │          │ │ Access   │ │ User     │         │ │
│  │  │ +199€    │ │ +99€     │ │ +149€    │ │ +249€    │         │ │
│  │  └──────────┘ └──────────┘ └──────────┘ └──────────┘         │ │
│  │                                                               │ │
│  │  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐         │ │
│  │  │ OCR      │ │ Web      │ │ Analytics│ │ Priority │         │ │
│  │  │          │ │ Scraper  │ │          │ │ Support  │         │ │
│  │  │ +99€     │ │ +149€    │ │ +99€     │ │ +199€/y  │         │ │
│  │  └──────────┘ └──────────┘ └──────────┘ └──────────┘         │ │
│  │                                                               │ │
│  └───────────────────────────────────────────────────────────────┘ │
│                                                                     │
│  BUNDLES (Empfohlen)                                               │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐  │
│  │ Starter     │ │Professional │ │ Business    │ │ Enterprise  │  │
│  │ 299€        │ │ 599€        │ │ 849€        │ │ 1.199€      │  │
│  │             │ │ (spar 20%)  │ │ (spar 22%)  │ │ (spar 22%)  │  │
│  └─────────────┘ └─────────────┘ └─────────────┘ └─────────────┘  │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

### License Key System

Jeder Kauf generiert einen License Key mit aktivierten Modulen:

```
License Key: RAG-XXXX-XXXX-XXXX

Aktivierte Module:
├── core: true
├── graph_rag: true
├── caching: true
├── api_access: false
├── multi_user: false
├── ocr: false
├── web_scraper: false
├── analytics: false
└── priority_support: false

Instanzen: 1/1
Gültig bis: 2026-01-27
```

### Feature Gating (Code)

```python
from dataclasses import dataclass
from typing import Optional

@dataclass
class License:
    key: str
    email: str
    modules: dict[str, bool]
    max_instances: int
    expires: datetime

    def has_module(self, module: str) -> bool:
        return self.modules.get(module, False)

# Modul-Definitionen
MODULES = {
    "core": {
        "price": 299,
        "features": {
            "max_documents": -1,
            "max_queries_per_day": -1,
            "vector_rag": True,
        }
    },
    "graph_rag": {
        "price": 199,
        "requires": ["core"],
        "features": {
            "knowledge_graph": True,
            "entity_extraction": True,
            "multi_hop_queries": True,
        }
    },
    "caching": {
        "price": 99,
        "requires": ["core"],
        "features": {
            "redis_cache": True,
            "query_cache": True,
            "embedding_cache": True,
        }
    },
    "api_access": {
        "price": 149,
        "requires": ["core"],
        "features": {
            "rest_api": True,
            "webhooks": True,
            "api_keys": True,
        }
    },
    "multi_user": {
        "price": 249,
        "requires": ["core"],
        "features": {
            "user_management": True,
            "rbac": True,
            "audit_log": True,
        }
    },
    "ocr": {
        "price": 99,
        "requires": ["core"],
        "features": {
            "tesseract_ocr": True,
            "scanned_pdfs": True,
        }
    },
    "web_scraper": {
        "price": 149,
        "requires": ["core"],
        "features": {
            "url_source": True,
            "auto_refresh": True,
            "sitemap_import": True,
        }
    },
    "analytics": {
        "price": 99,
        "requires": ["core"],
        "features": {
            "usage_dashboard": True,
            "query_analytics": True,
            "export": True,
        }
    },
}

# Feature Check
def check_feature(license: License, feature: str) -> bool:
    """Check if a feature is available based on license modules."""
    for module_name, module_def in MODULES.items():
        if license.has_module(module_name):
            if feature in module_def["features"]:
                return module_def["features"][feature]
    return False

# Decorator für Feature-Gating
def requires_module(module: str):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            license = get_current_license()
            if not license.has_module(module):
                raise FeatureNotLicensed(
                    f"This feature requires the '{module}' module. "
                    f"Upgrade at: https://ragkit.dev/pricing"
                )
            return await func(*args, **kwargs)
        return wrapper
    return decorator

# Verwendung
@requires_module("graph_rag")
async def query_with_graph(question: str):
    # Graph RAG Logic
    pass

@requires_module("ocr")
async def process_scanned_pdf(file: bytes):
    # OCR Logic
    pass
```

### UI: Modul-Status Anzeige

```
┌─────────────────────────────────────────────────────────────┐
│  ⚙️ Settings > License                                      │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  License: RAG-XXXX-XXXX-XXXX                               │
│  Status: ✅ Active (expires Jan 2026)                       │
│                                                             │
│  Installed Modules:                                         │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ ✅ Core              │ ✅ Graph RAG    │ ✅ Caching │   │
│  │ ❌ API Access        │ ❌ Multi-User   │ ❌ OCR     │   │
│  │ ❌ Web Scraper       │ ❌ Analytics    │            │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  [Upgrade Modules]  [Manage License]                        │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### Nachrüsten von Modulen

Kunde kann jederzeit Module hinzufügen:
1. Kauft Modul auf ragkit.dev/pricing
2. Erhält aktualisierten License Key (oder gleicher Key wird serverseitig aktualisiert)
3. Startet Container neu
4. Modul ist aktiv

```python
# License Validation Response
{
    "valid": True,
    "modules": {
        "core": True,
        "graph_rag": True,
        "caching": True,
        "api_access": False,  # Nicht gekauft
        "multi_user": False,
        "ocr": False,
        "web_scraper": False,
        "analytics": False,
    },
    "expires": "2026-01-27",
    "instances": {"used": 1, "max": 1}
}
```

---

## Offline-First Lizenzierung (Kein Server)

Das Lizenz-System funktioniert komplett offline - kein laufender Server deinerseits nötig.

### Ansatz: Signierte License Keys

Der License Key enthält alle Informationen und ist kryptographisch signiert. Die App validiert die Signatur lokal.

```
┌─────────────────────────────────────────────────────────────┐
│                   Offline License System                     │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  1. Kunde kauft auf LemonSqueezy/Gumroad                   │
│                      ↓                                      │
│  2. Du generierst signierten License Key                   │
│     (manuell oder via Zapier/n8n Automation)               │
│                      ↓                                      │
│  3. Kunde erhält Key per Email                             │
│                      ↓                                      │
│  4. App validiert Signatur LOKAL                           │
│     (Public Key ist in der App eingebaut)                  │
│                                                             │
│  KEIN laufender Server nötig!                              │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### License Key Format (JWT-ähnlich)

```
RAG.eyJlbWFpbCI6Imt1bmRlQGZpcm1hLmRlIiwibW9kdWxlcyI6WyJjb3JlIiwiZ3JhcGhfcmFnIl0sIm1heF9kb2NzIjotMSwibWF4X3F1ZXJpZXMiOi0xLCJleHBpcmVzIjoiMjAyNi0wMS0yNyJ9.SIGNATUR

Dekodiert:
{
  "email": "kunde@firma.de",
  "modules": ["core", "graph_rag"],
  "max_docs": -1,        // -1 = unlimited
  "max_queries": -1,     // -1 = unlimited
  "expires": "2026-01-27"
}
```

### Lokale Validierung (Code)

```python
# app/license/validator.py
import json
import base64
from datetime import datetime
from cryptography.hazmat.primitives.asymmetric import ed25519

# Public Key ist in der App eingebaut (Private Key bleibt bei dir)
PUBLIC_KEY_BYTES = b"..."  # Dein Public Key

class License:
    def __init__(self, data: dict, is_free: bool = False):
        self.email = data.get("email", "")
        self.modules = set(data.get("modules", []))
        self.max_docs = data.get("max_docs", 10)      # Free: 10
        self.max_queries = data.get("max_queries", 50) # Free: 50/Tag
        self.expires = datetime.fromisoformat(data.get("expires", "2099-12-31"))
        self.is_free = is_free

    def has_module(self, module: str) -> bool:
        if self.is_free:
            return False
        return module in self.modules

def validate_license(license_key: str) -> License:
    """Validate license key locally using embedded public key."""

    # Free mode - kein Key
    if not license_key or license_key.strip() == "":
        return License({}, is_free=True)

    try:
        # Parse: RAG.{payload}.{signature}
        parts = license_key.split(".")
        if len(parts) != 3 or parts[0] != "RAG":
            raise LicenseError("Invalid license format")

        payload_b64, signature_b64 = parts[1], parts[2]

        # Decode payload
        payload_json = base64.urlsafe_b64decode(payload_b64 + "==")
        payload = json.loads(payload_json)

        # Verify signature with embedded public key
        signature = base64.urlsafe_b64decode(signature_b64 + "==")
        public_key = ed25519.Ed25519PublicKey.from_public_bytes(PUBLIC_KEY_BYTES)
        public_key.verify(signature, payload_json)  # Raises if invalid

        # Check expiry
        license = License(payload)
        if license.expires < datetime.now():
            raise LicenseError(f"License expired on {license.expires}")

        return license

    except Exception as e:
        raise LicenseError(f"Invalid license: {e}")
```

### Key-Generierung (bei dir lokal - NICHT im Produkt)

```python
# scripts/generate_license.py - Läuft nur bei DIR
import json
import base64
from datetime import datetime, timedelta
from cryptography.hazmat.primitives.asymmetric import ed25519

# Private Key - GEHEIM, nur bei dir!
private_key = ed25519.Ed25519PrivateKey.generate()
# Speichere: private_key.private_bytes(...)

def generate_license_key(
    email: str,
    modules: list[str],
    max_docs: int = -1,
    max_queries: int = -1,
    valid_days: int = 365
) -> str:
    payload = {
        "email": email,
        "modules": modules,
        "max_docs": max_docs,
        "max_queries": max_queries,
        "expires": (datetime.now() + timedelta(days=valid_days)).isoformat()[:10]
    }

    payload_json = json.dumps(payload, separators=(',', ':')).encode()
    payload_b64 = base64.urlsafe_b64encode(payload_json).rstrip(b'=')

    signature = private_key.sign(payload_json)
    signature_b64 = base64.urlsafe_b64encode(signature).rstrip(b'=')

    return f"RAG.{payload_b64.decode()}.{signature_b64.decode()}"

# Beispiel
key = generate_license_key("kunde@firma.de", ["core", "graph_rag"])
print(key)  # RAG.eyJlbWFp...
```

### Workflow ohne Server

```
EINRICHTUNG (einmalig):
1. Ed25519 Key-Pair generieren
2. Public Key → in App einbauen
3. Private Key → sicher speichern (Passwort-Manager, etc.)

VERKAUF:
1. Kunde kauft auf Gumroad/LemonSqueezy
2. Du bekommst Email-Benachrichtigung
3. Du führst aus: python generate_license.py kunde@firma.de core,graph_rag
4. Du sendest Key per Email an Kunden
   (oder automatisiert via Zapier)

NUTZUNG:
1. Kunde trägt Key in .env ein: LICENSE_KEY=RAG.xxx.xxx
2. App validiert Signatur lokal beim Start
3. Fertig - keine Internet-Verbindung nötig
```

### Limit-Tracking (lokal in SQLite)

```python
# app/core/limits.py
from datetime import date

def check_document_limit():
    license = get_license()
    if license.max_docs == -1:  # Unlimited
        return

    current = db.query(Document).count()
    if current >= license.max_docs:
        raise LimitExceeded(
            f"Document limit reached ({current}/{license.max_docs}). "
            f"Upgrade: https://ragkit.dev/pricing"
        )

def check_query_limit():
    license = get_license()
    if license.max_queries == -1:  # Unlimited
        return

    today = date.today()
    current = db.query(QueryLog).filter(QueryLog.date == today).count()
    if current >= license.max_queries:
        raise LimitExceeded(
            f"Daily query limit reached ({current}/{license.max_queries}). "
            f"Upgrade or wait until tomorrow."
        )
```

### Sicherheit: Kann der Kunde das umgehen?

**Theoretisch ja** - SQLite löschen, Key teilen, etc.

**Warum das OK ist:**
- B2B-Kunden machen das selten (Reputation, Support)
- Free Tier ist eh zum Testen da
- Aufwand für "Crack" > Preis für License
- Wer betrügen will, hätte sowieso nie gezahlt
- Später optional: Server-Validierung hinzufügen wenn nötig

---

## Modulares System: Technische Umsetzung

### Prinzip: Alles im Image, Features per License aktiviert

```
┌─────────────────────────────────────────────────────────────┐
│                   Modulares System                           │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Docker Image enthält ALLES (alle Module).                  │
│  License Key bestimmt was AKTIV ist.                        │
│                                                             │
│  Vorteile:                                                  │
│  • Ein Image für alle Kunden                                │
│  • Kein separater Build pro Modul-Kombination              │
│  • Upgrade = neuer Key, kein neues Image                   │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### Projekt-Struktur für Modularität

```
app/
├── core/                    # IMMER aktiv (Free + Paid)
│   ├── rag_engine.py       # Basis RAG
│   ├── vector_store.py     # Qdrant
│   └── document_processor.py
│
├── modules/                 # NUR aktiv wenn lizenziert
│   ├── graph_rag/          # +199€
│   │   ├── __init__.py
│   │   ├── graph_store.py
│   │   └── entity_extractor.py
│   │
│   ├── caching/            # +99€
│   │   ├── __init__.py
│   │   └── redis_cache.py
│   │
│   ├── api/                # +149€
│   │   ├── __init__.py
│   │   └── routes.py
│   │
│   ├── ocr/                # +99€
│   │   ├── __init__.py
│   │   └── tesseract.py
│   │
│   ├── web_scraper/        # +149€
│   │   ├── __init__.py
│   │   └── scraper.py
│   │
│   ├── multi_user/         # +249€
│   │   ├── __init__.py
│   │   └── auth.py
│   │
│   └── analytics/          # +99€
│       ├── __init__.py
│       └── dashboard.py
│
└── license/
    └── validator.py
```

### Module Registry & Initialization

```python
# app/modules/__init__.py
from typing import Protocol

class Module(Protocol):
    name: str
    def initialize(self) -> None: ...
    def shutdown(self) -> None: ...

_modules: dict[str, Module] = {}

def register_module(name: str, module: Module):
    _modules[name] = module

def initialize_modules():
    """Initialisiere nur lizenzierte Module beim App-Start."""
    license = get_license()

    for name, module in _modules.items():
        if license.has_module(name):
            print(f"✅ Activating module: {name}")
            module.initialize()
        else:
            print(f"⏸️  Module not licensed: {name} (skipped)")
```

### Feature-Gating Decorator

```python
# app/modules/decorators.py
from functools import wraps
from app.license import get_license

class ModuleNotLicensed(Exception):
    pass

def requires_module(module_name: str):
    """Decorator: Funktion nur ausführen wenn Modul lizenziert."""
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            license = get_license()
            if not license.has_module(module_name):
                raise ModuleNotLicensed(
                    f"This feature requires the '{module_name}' module.\n"
                    f"Upgrade at: https://ragkit.dev/pricing"
                )
            return await func(*args, **kwargs)
        return wrapper
    return decorator

# Verwendung
@requires_module("graph_rag")
async def query_with_graph(question: str):
    # Nur wenn graph_rag lizenziert
    pass

@requires_module("ocr")
async def process_scanned_pdf(file: bytes):
    # Nur wenn ocr lizenziert
    pass
```

### RAG Engine mit modularen Retrievern

```python
# app/core/rag_engine.py
class RAGEngine:
    def __init__(self):
        self.retrievers = {}
        # Vector Search ist immer dabei (Core)
        self.retrievers["vector"] = self.vector_search

    def register_retriever(self, name: str, retriever):
        """Module können Retriever hinzufügen."""
        self.retrievers[name] = retriever

    async def query(self, question: str) -> Answer:
        results = []

        # Vector Search (immer)
        results.extend(await self.retrievers["vector"](question))

        # Graph Search (wenn Modul aktiv)
        if "graph" in self.retrievers:
            results.extend(await self.retrievers["graph"](question))

        # Rerank & Generate
        return await self.generate(question, self.rerank(results))
```

### Beispiel: Graph RAG Modul

```python
# app/modules/graph_rag/__init__.py
from app.modules import register_module

class GraphRAGModule:
    name = "graph_rag"

    def initialize(self):
        from .graph_store import KuzuGraphStore
        from .entity_extractor import EntityExtractor
        from app.core.rag_engine import rag_engine

        self.graph = KuzuGraphStore()
        self.extractor = EntityExtractor()

        # Retriever in RAG Engine registrieren
        rag_engine.register_retriever("graph", self.search)
        print("  → Knowledge Graph initialized")

    async def search(self, query: str):
        entities = await self.extractor.extract(query)
        return await self.graph.search(entities)

    def shutdown(self):
        self.graph.close()

# Beim Import automatisch registrieren
register_module("graph_rag", GraphRAGModule())
```

### FastAPI + Chainlit Integration

```python
# app/main.py
from fastapi import FastAPI
from chainlit.utils import mount_chainlit
from app.modules import initialize_modules
from app.license import load_license
import os

# FastAPI für API Endpoints
api = FastAPI(title="RAG Kit")

# Health Check (immer verfügbar)
@api.get("/health")
async def health():
    return {"status": "ok", "version": "1.0.0"}

# API Routes (nur wenn lizenziert)
from app.modules.api.routes import router as api_router
api.include_router(api_router, prefix="/api/v1")

@api.on_event("startup")
async def startup():
    # License laden
    key = os.getenv("LICENSE_KEY", "")
    license = load_license(key)

    print(f"License: {'Free' if license.is_free else license.email}")
    print(f"Modules: {list(license.modules) or ['(none)']}")
    print(f"Limits: {license.max_docs} docs, {license.max_queries} queries/day")

    # Module initialisieren
    initialize_modules()

# Chainlit UI mounten
mount_chainlit(app=api, target="app/ui/chat.py", path="/")

# Ergebnis:
# /         → Chainlit Chat UI
# /health   → Health Check
# /api/v1/* → REST API (wenn lizenziert)
```

### UI: Feature-Abhängige Anzeige

```python
# app/ui/chat.py
import chainlit as cl
from app.license import get_license
from app.modules.decorators import ModuleNotLicensed

@cl.on_chat_start
async def start():
    license = get_license()

    msg = "Willkommen! Laden Sie Dokumente hoch oder stellen Sie Fragen."

    if license.is_free:
        msg += f"\n\n⚠️ **Free Version**\n"
        msg += f"• {license.max_docs} Dokumente\n"
        msg += f"• {license.max_queries} Fragen pro Tag\n"
        msg += f"\n[Upgraden](https://ragkit.dev/pricing) für unbegrenzte Nutzung."

    await cl.Message(content=msg).send()

@cl.on_message
async def main(message: cl.Message):
    try:
        response = await rag_engine.query(message.content)
        await cl.Message(content=response.answer).send()

    except LimitExceeded as e:
        await cl.Message(
            content=f"⚠️ **Limit erreicht**\n\n{e}\n\n"
                    f"[Jetzt upgraden](https://ragkit.dev/pricing)"
        ).send()

    except ModuleNotLicensed as e:
        await cl.Message(
            content=f"🔒 **Feature nicht verfügbar**\n\n{e}"
        ).send()
```

---

## Entwicklungs-Roadmap

### Phase 1: Foundation (Woche 1-2)
- [ ] Projekt Setup (Poetry, Docker, CI)
- [ ] Config Management (Pydantic Settings)
- [ ] Basic FastAPI + Chainlit Integration
- [ ] Document Parser (PDF, TXT, MD)
- [ ] Qdrant Integration

### Phase 2: Core RAG (Woche 3-4)
- [ ] Chunking Pipeline
- [ ] Embedding Generation
- [ ] Vector Search
- [ ] Basic Chat UI
- [ ] Source Citations

### Phase 3: Graph RAG (Woche 5-6)
- [ ] Kuzu Integration
- [ ] Entity Extraction
- [ ] Graph Search
- [ ] Hybrid Retrieval + Reranking

### Phase 4: Polish (Woche 7-8)
- [ ] License Validation
- [ ] Health Checks & Diagnostics
- [ ] Caching (Redis)
- [ ] Documentation
- [ ] Testing

### Phase 5: Launch
- [ ] Landing Page
- [ ] LemonSqueezy Setup
- [ ] Beta Testers
- [ ] Launch on ProductHunt

---

## Offene Fragen / Ideen

- [ ] Streaming Responses (SSE)?
- [ ] Conversation Memory (wie viel Historie)?
- [ ] Multi-Language Support (UI)?
- [ ] Webhook für Document Processing Status?
- [ ] Backup/Export Funktion?
- [ ] OCR für gescannte PDFs?
- [ ] Web Scraping als Input?

---

## Notizen

*Platz für weitere Ideen und Notizen...*

- Caching: Auch semantisch ähnliche Queries cachen (Threshold 0.95)?
- Graph Visualization im UI?
- "Explain" Mode der die Retrieval-Schritte zeigt?
