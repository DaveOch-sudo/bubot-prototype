# BuBot — AI-Driven Campus Conversational AI Prototype

## 1. Project Overview

**BuBot** is an AI-driven conversational system designed to provide students and other university users with accurate, contextual and continuously updatable information about a university.

The project is being developed initially using **Busitema University as the demonstration case**, with the long-term objective of creating a scalable architecture that can support other universities and institutions.

The prototype combines:

- React for the user interface
- Django and Django REST Framework for the central application backend
- Rasa for conversational management and dialogue state
- Retrieval-Augmented Generation (RAG) for institutional knowledge retrieval
- NVIDIA-hosted LLM inference for natural-language generation
- PostgreSQL with pgvector for persistent data and vector search

The prototype must demonstrate that a user can communicate naturally with the system, ask follow-up questions, and receive answers grounded in institutional documents without every possible question being manually programmed.

---

# 2. Main Objective

The main objective of the prototype is to demonstrate a conversational AI system that can:

1. Understand natural-language questions.
2. Handle different ways of asking for the same information.
3. Maintain conversational context.
4. Retrieve relevant information from university documents.
5. Generate answers using retrieved institutional evidence.
6. Provide the source of information used to answer a question.
7. Allow administrators to add new institutional documents without developers manually programming new answers.
8. Safely indicate when the available institutional knowledge does not contain enough information.

The prototype is therefore **not simply a chatbot**.

It is a demonstration of a complete knowledge-driven conversational pipeline.

---

# 3. Core Prototype Demonstration

The prototype must be capable of demonstrating three important capabilities.

## 3.1 Natural Language Variation

The system should recognize that different questions can represent the same underlying information need.

For example:

> What are the requirements for Computer Science?

and:

> I'm a diploma holder and I want to study Computer Science. What do I need?

and:

> Can someone with a diploma apply for Computer Science?

The system should not depend on having a separate hard-coded intent for every possible wording.

The exact implementation can evolve, but semantic understanding should increasingly be handled through the AI/RAG layer rather than creating hundreds of manually defined university-specific intents.

---

# 4. Conversational Context

The system must support follow-up questions.

For example:

### User

> When does registration begin?

### BuBot

> Registration begins on ...

### User

> What about first years?

### BuBot

> For first-year students, ...

### User

> And when should they report?

The final question should be understood in the context of the previous conversation.

Another example:

### User

> What are the requirements for Computer Science?

### BuBot

> ...

### User

> What about diploma holders?

The system should understand that the second question is referring to Computer Science admission requirements.

Rasa should participate in managing conversation state and session information, while the AI/RAG layer may assist with contextual query understanding and retrieval.

---

# 5. Dynamic Institutional Knowledge

One of the most important demonstrations is that the system can learn new institutional knowledge without developers manually adding a new response.

The intended workflow is:

```text
Administrator
      ↓
Upload University PDF
      ↓
Text Extraction
      ↓
Document Structure Detection
      ↓
Structure-Aware Chunking
      ↓
Metadata Generation
      ↓
Embeddings
      ↓
Vector Storage
      ↓
Document Becomes Searchable
      ↓
User Asks Question
      ↓
Relevant Evidence Retrieved
      ↓
NVIDIA LLM
      ↓
Grounded Answer + Source
```

For example, an administrator can upload a new admissions guide.

The system processes the document.

A user can then ask a question whose answer exists only in that document.

The system retrieves the relevant passage and uses it to produce the answer.

No developer should have to create a new hard-coded answer specifically for that question.

---

# 6. System Architecture

The agreed prototype architecture is:

```text
                    ┌─────────────────┐
                    │      User       │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │ React Frontend  │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │ Django Backend  │
                    │   REST API      │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │      Rasa       │
                    │ Dialogue/State  │
                    └────────┬────────┘
                             │
                             ▼
                 ┌───────────────────────┐
                 │   AI Orchestration    │
                 └───────────┬───────────┘
                             │
                 ┌───────────┴───────────┐
                 ▼                       ▼
        ┌─────────────────┐     ┌─────────────────┐
        │      RAG        │     │ NVIDIA LLM      │
        │ Retrieval       │────▶│ Generation      │
        └────────┬────────┘     └─────────────────┘
                 │
                 ▼
        ┌─────────────────┐
        │ PostgreSQL +    │
        │    pgvector     │
        └─────────────────┘

Response:
NVIDIA → AI Orchestration → Rasa → Django → React
```

---

# 7. Component Responsibilities

## 7.1 React

React provides the user-facing interface.

Responsibilities include:

- Chat interface
- Message display
- User input
- Loading states
- Error states
- Session handling
- Source display
- Basic document/admin interfaces where required
- Communication with Django REST APIs

React should not directly communicate with the NVIDIA API, Rasa service, or vector database.

The frontend communicates primarily with Django.

---

# 8. Django Backend

Django is the central application backend.

Django is responsible for:

- REST APIs
- Authentication where required
- Users
- Conversations
- Messages
- Sessions
- Administration
- Document management
- Knowledge management
- Database access
- Rasa integration
- AI orchestration integration
- Background processing where required
- Application configuration
- Health/status endpoints

Django acts as the central application boundary.

The prototype should use **Django REST Framework** for API development.

---

# 9. Rasa

Rasa remains a core part of the architecture.

Rasa is responsible primarily for:

- Dialogue management
- Conversation state
- Session handling
- Basic NLU where useful
- Conversation events
- Controlled interaction with the AI layer
- Traditional deterministic conversational behaviour where appropriate

Rasa should not become a giant collection of hard-coded university questions.

Avoid creating an architecture such as:

```text
ask_fees
ask_admission
ask_admission_requirements
ask_computer_science_requirements
ask_diploma_requirements
ask_registration
ask_first_year_registration
ask_reporting_date
...
```

for every possible university question.

The system should instead increasingly use semantic understanding and RAG.

Rasa can still contain deterministic intents and actions where they provide clear value.

---

# 10. AI Orchestration Layer

The AI orchestration layer connects the conversational system to:

- RAG
- Embedding services
- Vector retrieval
- NVIDIA LLM inference
- Prompt construction
- Context handling
- Grounding rules
- Source attribution

The orchestration layer should coordinate the process rather than place all AI logic inside Django or Rasa.

Conceptually:

```text
Rasa
  ↓
AI Orchestrator
  ├── Understand/prepare query
  ├── Retrieve knowledge
  ├── Build context
  ├── Apply grounding rules
  └── Call LLM
       ↓
    Response
```

---

# 11. LLM Provider Architecture

The LLM provider must be replaceable.

Use an abstraction such as:

```text
LLMProvider
      │
      └── NVIDIAProvider
```

The rest of the application should not depend directly on NVIDIA-specific implementation details.

For example:

```python
class LLMProvider:
    def generate(self, prompt, context):
        raise NotImplementedError
```

Then:

```text
NVIDIAProvider
    ↓
NVIDIA-hosted inference/API
```

The exact NVIDIA model used by the prototype may change depending on availability, access and testing.

The model name must therefore not be unnecessarily hard-coded throughout the application.

---

# 12. Retrieval-Augmented Generation

RAG is a core feature of BuBot.

The system should not rely solely on the LLM's pre-existing knowledge.

The intended process is:

```text
User Question
      ↓
Query Preparation
      ↓
Query Embedding
      ↓
Vector Search
      ↓
Relevant Institutional Chunks
      ↓
Context Construction
      ↓
Grounding Instructions
      ↓
NVIDIA LLM
      ↓
Answer + Sources
```

The retrieved institutional information becomes evidence for the generated response.

---

# 13. Document Ingestion Pipeline

The document ingestion pipeline must support university PDFs.

The initial pipeline is:

```text
PDF
 ↓
Extraction
 ↓
Cleaning
 ↓
Structure Detection
 ↓
Chunking
 ↓
Metadata
 ↓
Embedding
 ↓
Vector Storage
 ↓
Indexed
```

A document should move through identifiable processing states.

Suggested states:

```text
UPLOADED
PROCESSING
EXTRACTED
CHUNKED
EMBEDDED
INDEXED
FAILED
```

The exact implementation may evolve.

---

# 14. PDF Text Extraction

The system must extract useful textual content from uploaded PDF documents.

The implementation should:

- Preserve page boundaries where possible.
- Preserve headings.
- Remove unnecessary extraction artefacts.
- Preserve meaningful paragraphs.
- Handle common university document structures.
- Record page numbers.

Tables should be supported where practical.

Perfect extraction of every possible PDF format is not required for the five-day prototype.

However, the implementation should not deliberately destroy document structure.

---

# 15. Structure-Aware Chunking

Do not blindly split every document into arbitrary fixed-size pieces if the document structure can be preserved.

Where possible, chunks should respect:

- Headings
- Sections
- Paragraph boundaries
- Page boundaries
- Tables
- Logical document sections

A fallback fixed-size chunking strategy may be used where structure cannot be identified.

The objective is to produce chunks that contain meaningful units of institutional information.

---

# 16. Chunk Metadata

Each knowledge chunk should preserve enough metadata to identify its origin.

Example:

```json
{
  "document_id": "123",
  "document_title": "Admissions Guide 2026/2027",
  "section": "Admission Requirements",
  "page": 27,
  "content_type": "paragraph",
  "academic_year": "2026/2027",
  "source": "Admissions Guide 2026/2027"
}
```

The exact schema may change during implementation.

The important requirement is that retrieved information can be traced back to the original document.

---

# 17. Document Model

A document should contain information such as:

```text
Document
---------
id
title
filename
source
version
status
uploaded_at
processed_at
```

Additional fields can be introduced where necessary.

---

# 18. Knowledge Chunk Model

A knowledge chunk should contain information such as:

```text
KnowledgeChunk
--------------
id
document_id
content
chunk_index
metadata
embedding
created_at
```

The vector representation should be stored in PostgreSQL using pgvector.

---

# 19. Vector Storage

The preferred prototype vector storage solution is:

```text
PostgreSQL
    +
pgvector
```

This avoids introducing a separate vector database unless a real technical requirement emerges.

The prototype should keep infrastructure simple.

The vector layer must support:

- Storing embeddings
- Similarity search
- Returning relevant chunks
- Returning document metadata
- Supporting future improvements to retrieval

---

# 20. Embeddings

The embedding model is separate from the generation model.

The system should therefore conceptually support:

```text
EmbeddingProvider
       │
       └── Current embedding implementation
```

Do not tightly couple the embedding implementation to the NVIDIA generation model.

This allows the embedding model to be changed later without redesigning the entire RAG system.

---

# 21. Retrieval

The retrieval system should:

1. Receive a user query.
2. Convert the query into an embedding.
3. Search pgvector.
4. Retrieve the most relevant chunks.
5. Preserve their document metadata.
6. Return evidence to the orchestration layer.

A retrieval result should contain information similar to:

```json
{
  "content": "Relevant institutional information...",
  "document": "Admissions Guide 2026/2027",
  "page": 27,
  "section": "Admission Requirements",
  "score": 0.87
}
```

Similarity scores are internal retrieval information and do not necessarily need to be displayed to users.

---

# 22. Grounding Rules

The LLM must be instructed to prioritize retrieved institutional evidence.

The system should not invent:

- University fees
- Admission requirements
- Academic programmes
- Registration dates
- Reporting dates
- University policies
- Procedures
- Institutional facts
- Academic years
- Other university-specific information

If the retrieved evidence does not adequately answer the question, the system should say that the available information is insufficient rather than confidently inventing an answer.

For example:

> I could not find enough information about that in the available university documents.

The exact wording can be improved later.

---

# 23. Source Attribution

When an answer is based on institutional knowledge, the response should identify the relevant source.

Example:

```text
According to the 2026/2027 Admissions Guide, diploma holders
may apply under the requirements described for the programme...

Sources:
- Admissions Guide 2026/2027 — Page 27
```

Sources must come from actual retrieved evidence.

The system must never fabricate a document title, page number or source.

---

# 24. Conversation Sessions

The frontend should maintain a session identifier.

Example:

```json
{
  "session_id": "demo-session-001",
  "message": "What are the requirements for Computer Science?"
}
```

Django should pass the appropriate conversation/session information to the relevant services.

The system may persist conversations using models such as:

```text
Conversation
------------
id
session_id
created_at
updated_at
```

and:

```text
Message
-------
id
conversation_id
role
content
created_at
```

The exact schema may evolve.

---

# 25. API Contract

The initial chat endpoint should conceptually be:

```text
POST /api/chat/
```

Request:

```json
{
  "session_id": "demo-session-001",
  "message": "What are the requirements for Computer Science?"
}
```

Response:

```json
{
  "session_id": "demo-session-001",
  "message": "According to the 2026/2027 Admissions Guide, ...",
  "sources": [
    {
      "document": "Admissions Guide 2026/2027",
      "page": 27
    }
  ]
}
```

The exact response structure may evolve during implementation, but breaking API changes must be communicated to the developers consuming the API.

---

# 26. Health Endpoint

The backend should provide a basic health endpoint:

```text
GET /api/health/
```

Example:

```json
{
  "status": "ok",
  "service": "bubot-backend"
}
```

Additional service health checks can be added later.

---

# 27. Admin Knowledge Workflow

The prototype should provide an administrative workflow for uploading institutional documents.

The basic flow is:

```text
Administrator
     ↓
Upload PDF
     ↓
Document Created
     ↓
Processing Started
     ↓
Text Extracted
     ↓
Chunks Created
     ↓
Embeddings Generated
     ↓
Vectors Stored
     ↓
INDEXED
     ↓
Available to Chatbot
```

Django Admin may be used for the initial prototype.

A completely custom administration interface is not required if Django Admin provides the necessary demonstration.

---

# 28. Recommended Repository Structure

The repository should initially follow this structure:

```text
bubot-prototype/
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── services/
│   │   ├── hooks/
│   │   └── types/
│   ├── package.json
│   └── ...
│
├── backend/
│   ├── manage.py
│   ├── config/
│   │   ├── settings.py
│   │   ├── urls.py
│   │   └── ...
│   │
│   ├── chat/
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── views.py
│   │   ├── urls.py
│   │   └── services/
│   │       ├── rasa_client.py
│   │       ├── rag_client.py
│   │       └── ...
│   │
│   └── requirements.txt
│
├── rasa/
│   ├── config.yml
│   ├── domain.yml
│   ├── endpoints.yml
│   ├── credentials.yml
│   ├── data/
│   ├── actions/
│   └── models/
│
├── ai/
│   ├── llm/
│   │   ├── base.py
│   │   ├── nvidia.py
│   │   └── ...
│   │
│   ├── rag/
│   │   ├── ingestion/
│   │   ├── chunking/
│   │   ├── embeddings/
│   │   ├── retrieval/
│   │   └── generation/
│   │
│   ├── orchestration/
│   │   └── ...
│   │
│   └── config.py
│
├── documents/
│   └── .gitkeep
│
├── scripts/
│
├── tests/
│
├── .env.example
├── .gitignore
├── docker-compose.yml
├── README.md
└── TEAM_DEVELOPMENT.md
```

The structure may be adjusted when implementation reveals a genuine technical reason.

It should not be repeatedly redesigned merely for preference.

---

# 29. Team Ownership

The initial ownership is:

```text
frontend/             → React Developer
backend/              → Django Developer
rasa/                 → Rasa Developer
ai/rag/               → RAG Developer
ai/llm/               → LLM/NVIDIA Developer
ai/orchestration/     → Shared / Team Lead coordinated
```

The five coding-capable team members are expected to work inside the same repository.

Detailed responsibilities are defined in:

```text
TEAM_DEVELOPMENT.md
```

---

# 30. Git Branch Strategy

The initial branch structure is:

```text
main
│
├── feature/frontend
├── feature/django
├── feature/rasa
├── feature/rag
└── feature/llm
```

The `main` branch should remain stable.

Developers should work on their assigned feature branches.

Typical workflow:

```bash
git checkout main
git pull origin main
git checkout -b feature/rag
```

After implementing and testing:

```bash
git add .
git commit -m "Implement PDF chunking"
git push -u origin feature/rag
```

Then create a pull request.

---

# 31. Commit Message Guidelines

Good commit messages describe the actual change.

Examples:

```text
Implement PDF text extraction
Add structure-aware chunking
Add document metadata
Implement pgvector retrieval
Add NVIDIA provider
Add Rasa session handling
Add chat API
Add source display
Add document processing status
```

Avoid vague messages such as:

```text
updates
stuff
changes
final
fix
new things
```

---

# 32. Development Principles

The project follows these principles:

### 32.1 Working Software First

A working prototype is more important than theoretical perfection.

### 32.2 Incremental Development

Build and test small pieces before integrating larger features.

### 32.3 Keep Interfaces Clear

Every component should know what it receives and what it returns.

### 32.4 Avoid Unnecessary Complexity

Do not introduce microservices, databases, frameworks or infrastructure simply because they are technically possible.

### 32.5 Do Not Fake AI

Do not hard-code answers simply to make a demonstration appear intelligent.

### 32.6 Preserve Replaceability

LLM and embedding providers should be replaceable.

### 32.7 Do Not Hard-Code University Knowledge

Institutional information should primarily come through the knowledge ingestion and retrieval system.

### 32.8 Keep the Five-Day Deadline Visible

Features that do not contribute significantly to the prototype demonstration should be postponed.

---

# 33. Five-Day Prototype Plan

## Day 1 — System Skeleton

Goal:

Make the basic end-to-end communication path work.

```text
React
 ↓
Django
 ↓
Rasa
 ↓
AI Layer
 ↓
NVIDIA
 ↓
Django
 ↓
React
```

Tasks:

- Repository structure
- Django project
- React project
- Rasa project
- Basic API
- Basic Rasa communication
- Basic NVIDIA communication
- Session ID
- Basic chat UI
- Environment configuration

Do not spend the entire first day building advanced RAG before the basic vertical path works.

---

# Day 2 — Knowledge Engine

Goal:

Make university documents searchable.

Tasks:

- PDF upload
- PDF extraction
- Cleaning
- Structure detection
- Chunking
- Metadata
- Embeddings
- PostgreSQL
- pgvector
- Indexing
- Load genuine university documents

---

# Day 3 — RAG + NVIDIA

Goal:

Connect retrieved institutional evidence to generation.

Pipeline:

```text
Question
 ↓
Embedding
 ↓
Vector Search
 ↓
Relevant Chunks
 ↓
Context
 ↓
NVIDIA
 ↓
Grounded Answer
 ↓
Sources
```

Test:

- Correct retrieval
- Correct answers
- Source attribution
- Insufficient evidence
- Obvious hallucination cases

---

# Day 4 — Semantic Understanding + Context

Goal:

Improve conversational intelligence.

Tasks:

- Query understanding
- Contextual follow-up
- Query rewriting where necessary
- Retrieval improvements
- Context handling
- Low-confidence handling
- Natural language variations

Do not build a huge autonomous agent.

---

# Day 5 — Hardening and Demonstration

Goal:

Make the prototype reliable enough to demonstrate.

Tasks:

- Improve UI
- Improve error handling
- Improve document processing status
- Improve answer quality
- Improve source display
- Test response latency
- Test uploaded documents
- Prepare demonstration questions
- Remove obvious failures
- Perform complete end-to-end testing

No major architecture redesign should happen on Day 5.

---

# 34. Integration Checkpoints

The team should integrate progressively.

## Checkpoint 1

```text
React → Django
```

The frontend can send a message and receive a response.

## Checkpoint 2

```text
React → Django → Rasa
```

Django successfully communicates with Rasa.

## Checkpoint 3

```text
React → Django → Rasa → AI
```

Rasa can participate in AI processing.

## Checkpoint 4

```text
React
 ↓
Django
 ↓
Rasa
 ↓
AI
 ├── RAG
 └── NVIDIA
```

## Final Checkpoint

```text
React
 ↓
Django
 ↓
Rasa
 ↓
AI Orchestration
 ├── RAG
 │    ↓
 │ PostgreSQL + pgvector
 │
 └── NVIDIA
 ↓
Django
 ↓
React
```

And the knowledge ingestion path:

```text
Admin
 ↓
Upload PDF
 ↓
RAG Ingestion
 ↓
Extraction
 ↓
Chunking
 ↓
Embeddings
 ↓
pgvector
 ↓
User Question
 ↓
Retrieved Evidence
 ↓
NVIDIA
 ↓
Grounded Answer + Source
```

---

# 35. Prototype Success Criteria

The prototype is considered functionally successful when it can demonstrate:

- React chat interface works.
- Django API works.
- Rasa participates in the conversation flow.
- NVIDIA-hosted inference works.
- Session IDs are supported.
- Follow-up questions can use conversational context.
- A university PDF can be uploaded.
- Text can be extracted.
- Document structure can be processed.
- Chunks can be created.
- Metadata is preserved.
- Embeddings can be generated.
- Embeddings can be stored in pgvector.
- Semantic retrieval works.
- Retrieved evidence reaches the LLM.
- The LLM produces a grounded answer.
- Sources can be displayed.
- A newly uploaded document becomes searchable.
- The system can indicate insufficient evidence.
- The complete system works end-to-end.

---

# 36. Explicit Prototype Scope Exclusions

The following are not priorities for the five-day prototype:

- Federated learning
- Multimodal learning
- Voice interfaces
- Mobile application
- Fine-tuning
- Complex multi-agent systems
- Arbitrary autonomous tool execution
- Website-wide crawling
- Kubernetes
- Microservice explosion
- Production-grade enterprise security
- Sophisticated analytics
- Knowledge graphs
- Advanced ontology systems
- Large-scale distributed infrastructure

These may become future research or development areas.

They should not delay the core prototype.

---

# 37. Future Scalability

The prototype should be designed so that future research can investigate:

- Multiple universities
- Institution-specific knowledge bases
- More advanced retrieval
- Hybrid search
- Reranking
- Better document understanding
- Multilingual interaction
- Voice
- Multimodal inputs
- Federated approaches
- More advanced personalization
- Analytics
- Mobile applications
- Additional LLM providers
- Local LLM deployment
- Larger-scale infrastructure

However, these are future directions rather than requirements for the initial prototype.

---

# 38. Important Engineering Rule

The architecture described in this README is the current source of truth for the prototype.

Developers should not independently replace:

- Django with another backend
- Rasa with another conversational framework
- PostgreSQL/pgvector with another vector database
- NVIDIA with a different LLM provider

unless a serious technical issue is identified and discussed with the team lead.

Technology choices should be changed because of an actual requirement or blocker, not personal preference.

---

# 39. Final Prototype Vision

The completed prototype should make the following demonstration possible:

```text
1. User opens BuBot.

2. User asks:
   "What are the requirements for Computer Science?"

3. BuBot retrieves relevant university information.

4. BuBot answers naturally.

5. BuBot identifies the source.

6. User asks:
   "What about diploma holders?"

7. BuBot understands the previous context.

8. BuBot retrieves the relevant information.

9. An administrator uploads a new university PDF.

10. The system processes and indexes it.

11. User asks a question about information contained
    only in the newly uploaded document.

12. BuBot retrieves the new information.

13. BuBot produces a grounded answer.

14. BuBot identifies the document/page used.
```

That complete flow is the core proof-of-concept for BuBot.

## Development Environment Setup

This section describes the standard development environment and setup process for the BuBot prototype. Every team member should follow these steps before working on their assigned component.

### 1. Prerequisites

Install the following before setting up the project:

- Git
- Python 3.10 or later
- Node.js 20 or later
- npm
- PostgreSQL 16
- PostgreSQL command-line tools
- A code editor such as VS Code

Docker is **not required** for the BuBot prototype.

### 2. Clone the Repository

Clone the project from GitHub:

```bash
git clone <REPOSITORY_URL>
cd bubot-prototype
```

Check the repository status:

```bash
git status
```

The working tree should be clean after cloning.

### 3. Python Virtual Environment

From the project root, create the shared project-level Python virtual environment:

```bash
python3 -m venv .venv
```

Activate it:

```bash
source .venv/bin/activate
```

Upgrade the Python packaging tools:

```bash
python -m pip install --upgrade pip setuptools wheel
```

The virtual environment should be activated whenever working with the Django backend or AI components.

### 4. Backend Setup

Move into the backend directory:

```bash
cd backend
```

Install the backend dependencies:

```bash
python -m pip install -r requirements.txt
```

The backend uses Django, Django REST Framework, PostgreSQL and the PostgreSQL Python driver.

### 5. Environment Configuration

Return to the project root:

```bash
cd ..
```

Create the local environment file:

```bash
cp .env.example .env
```

Open `.env` and provide the values required for the local environment.

Example:

```env
DJANGO_SECRET_KEY=
DEBUG=True
DATABASE_URL=
RASA_URL=
NVIDIA_API_KEY=
NVIDIA_MODEL=
DB_PASSWORD=
```

The `.env` file is for local development only and must **never be committed to Git**.

Do not put API keys, passwords, tokens or other secrets into source code.

### 6. PostgreSQL Database

Create a PostgreSQL database and dedicated application user for BuBot.

Example:

```sql
CREATE USER bubot_user WITH PASSWORD 'your_password';
CREATE DATABASE bubot OWNER bubot_user;
GRANT ALL PRIVILEGES ON DATABASE bubot TO bubot_user;
```

The password used for the database user should be placed in the local `.env` file:

```env
DB_PASSWORD=your_password
```

The application should use the dedicated `bubot_user` account rather than the PostgreSQL administrator account.

### 7. Enable pgvector

Connect to the `bubot` database using a PostgreSQL administrator account and enable the pgvector extension:

```sql
\c bubot

CREATE EXTENSION IF NOT EXISTS vector;
```

Verify that the extension is available:

```sql
SELECT extversion
FROM pg_extension
WHERE extname = 'vector';
```

The `vector` extension is required for the project's semantic-vector storage and retrieval layer.

### 8. Run Django Migrations

From the project root:

```bash
cd backend
python manage.py migrate
```

If the command completes successfully, the Django application can communicate with the PostgreSQL database.

### 9. Start the Django Backend

From the `backend` directory:

```bash
python manage.py runserver
```

The development server should start locally.

The initial health endpoint is:

```text
/api/health/
```

Open:

```text
http://127.0.0.1:8000/api/health/
```

Expected response:

```json
{
  "status": "ok",
  "service": "bubot-backend"
}
```

Stop the server with:

```text
Ctrl + C
```

### 10. Frontend Setup

Open another terminal and move to the project root:

```bash
cd bubot-prototype/frontend
```

Install the JavaScript dependencies:

```bash
npm install
```

Start the React development server:

```bash
npm run dev
```

Vite will display the local development URL in the terminal.

The frontend must communicate with Django rather than communicating directly with Rasa or the NVIDIA API.

### 11. Rasa

Rasa is part of the BuBot architecture, but it is **not installed during the initial project foundation setup**.

The `rasa/` directory currently serves as the integration location for the Rasa component.

Rasa-specific dependencies and configuration will be added when the Rasa component is implemented.

### 12. AI Module

The `ai/` directory contains the AI and RAG components of the project.

Current structure:

```text
ai/
├── __init__.py
├── llm/
│   └── __init__.py
├── orchestration/
│   └── __init__.py
└── rag/
    ├── __init__.py
    ├── ingestion/
    │   └── __init__.py
    ├── chunking/
    │   └── __init__.py
    ├── embeddings/
    │   └── __init__.py
    ├── retrieval/
    │   └── __init__.py
    └── generation/
        └── __init__.py
```

The AI module is intentionally separated from Django views. AI orchestration, RAG processing, embeddings, retrieval and generation logic should be implemented inside this module.

The LLM integration should use the planned provider abstraction:

```text
LLMProvider
    ↓
NVIDIAProvider
```

This keeps the orchestration layer independent of a specific NVIDIA model or provider implementation.

### 13. Project Structure

The main project structure is:

```text
bubot-prototype/
├── frontend/
├── backend/
├── rasa/
├── ai/
│   ├── llm/
│   ├── orchestration/
│   └── rag/
│       ├── ingestion/
│       ├── chunking/
│       ├── embeddings/
│       ├── retrieval/
│       └── generation/
├── documents/
├── scripts/
├── tests/
├── .env.example
├── .gitignore
├── README.md
└── TEAM_DEVELOPMENT.md
```

### 14. Git Workflow

The `main` branch contains the shared stable project state.

Developers should create feature branches before making changes.

Example:

```bash
git checkout main
git pull origin main
git checkout -b feature/<component>
```

Examples:

```text
feature/frontend
feature/django
feature/rasa
feature/rag
feature/llm
```

Commit changes regularly using clear commit messages:

```bash
git add .
git commit -m "feat: add chat interface"
```

Push the feature branch:

```bash
git push -u origin feature/<component>
```

Changes should be merged into `main` through a Pull Request after review.

Do not push unfinished experimental work directly to `main`.

### 15. Keeping the Environment Consistent

Before starting development each day, update the local repository:

```bash
git checkout main
git pull origin main
```

Then return to the appropriate feature branch.

When dependencies are added or changed, update the relevant dependency file so other team members can reproduce the environment.

For Python backend dependencies:

```bash
cd backend
python -m pip freeze > requirements.txt
```

For frontend dependencies, update `package.json` and `package-lock.json` through npm.

### 16. Setup Verification Checklist

A developer is ready to begin component development when the following checks pass:

- [ ] Repository cloned successfully
- [ ] Python virtual environment created and activated
- [ ] Backend dependencies installed
- [ ] `.env` created from `.env.example`
- [ ] PostgreSQL is running
- [ ] `bubot` database exists
- [ ] `bubot_user` can access the database
- [ ] pgvector extension is enabled
- [ ] Django migrations complete successfully
- [ ] Django health endpoint returns `status: ok`
- [ ] Frontend dependencies installed
- [ ] React development server starts
- [ ] Rasa directory exists
- [ ] AI module structure exists
- [ ] No secrets are committed
- [ ] Git branches and Pull Request workflow are understood

### 17. Development Architecture

The intended application flow is:

```text
User
  ↓
React
  ↓
Django
  ↓
Rasa
  ↓
AI / RAG Orchestration
  ↓
Relevant Institutional Knowledge
  ↓
NVIDIA-hosted LLM
  ↓
Grounded Response + Sources
  ↓
Rasa
  ↓
Django
  ↓
React
```

The knowledge pipeline is:

```text
Administrator
  ↓
University Document Upload
  ↓
Text Extraction
  ↓
Document Structure Detection
  ↓
Structure-aware Chunking
  ↓
Metadata Generation
  ↓
Embeddings
  ↓
PostgreSQL + pgvector
  ↓
Searchable Knowledge Base
```

This architecture is the agreed prototype direction. New components or architectural changes should be discussed with the team before being introduced.
