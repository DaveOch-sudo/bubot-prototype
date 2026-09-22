# BuBot Team Development Guide

## Team Development and Collaboration Plan

This document defines how the BuBot prototype will be developed collaboratively by the five coding-capable team members.

The purpose is to make sure every developer understands:

* What they own
* What they need to build
* How their component connects to the rest of the system
* What interfaces they must provide
* How Git should be used
* When integration must happen
* What should and should not be changed independently

The team should work toward one integrated prototype rather than five independent projects.

---

# 1. Development Team

The coding team consists of five developers:

1. React Developer
2. Django Developer
3. Rasa Developer
4. RAG + LLM Integration Developer
5. Team Lead / Integration Developer

---

# 2. Shared Architecture

Every developer must understand the complete system before implementing their individual component.

```text
User
  ↓
React
  ↓
Django
  ↓
Rasa
  ↓
AI Orchestration
  ↓
RAG
  ↓
NVIDIA LLM
  ↓
Django
  ↓
React
```

Knowledge ingestion:

```text
Administrator
  ↓
Django Admin
  ↓
PDF Upload
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
```

---

# 3. Repository Ownership

The repository should follow this structure:

```text
bubot-prototype/
│
├── frontend/
├── backend/
├── rasa/
├── ai/
├── documents/
├── scripts/
├── tests/
├── docker-compose.yml
├── README.md
└── TEAM_DEVELOPMENT.md
```

Ownership:

| Area                | Primary Owner                            |
| ------------------- | ---------------------------------------- |
| `frontend/`         | React Developer                          |
| `backend/`          | Django Developer                         |
| `rasa/`             | Rasa Developer                           |
| `ai/rag/`           | RAG Developer                            |
| `ai/llm/`           | RAG/LLM Developer                        |
| `ai/orchestration/` | Team Lead + LLM Developer                |
| Integration         | Team Lead                                |
| Tests               | Everyone                                 |
| Documentation       | Team Lead + Everyone for their component |

Ownership does not mean that only one person can edit an area.

It means that the primary owner is responsible for understanding and maintaining that area.

---

# 4. Developer 1 — React Developer

## Main Responsibility

Build the user-facing React application.

Primary directory:

```text
frontend/
```

---

## Required Features

### Chat Interface

The interface should provide:

* Message input
* Send button
* User messages
* Assistant messages
* Loading indicator
* Error display
* Source display
* Conversation/session handling

---

## Session Handling

The frontend must maintain a session ID.

Example:

```text
demo-session-001
```

Every message should be sent with the session ID.

Request:

```json
{
  "session_id": "demo-session-001",
  "message": "What are the requirements for Computer Science?"
}
```

---

## API Communication

The frontend communicates with Django rather than directly with Rasa or NVIDIA.

```text
React
  ↓
Django
```

Do not make the browser directly responsible for calling the LLM provider.

---

## Response Display

The frontend should be able to display:

```text
Assistant response

Sources:
Admissions Guide 2026/2027 — Page 27
```

If no sources are available, the interface should handle that gracefully.

---

## Day 1 Tasks

* Create React application.
* Create basic chat page.
* Create API service.
* Connect to Django.
* Display user and assistant messages.
* Implement session ID.
* Handle loading/error states.

---

## Day 2–3

* Improve chat interface.
* Add source display.
* Handle structured API responses.
* Improve error handling.

---

## Day 4–5

* Improve usability.
* Improve response presentation.
* Add document/processing status UI if required.
* Fix integration issues.

---

# 5. Developer 2 — Django Developer

## Main Responsibility

Build the central application backend.

Primary directory:

```text
backend/
```

---

## Main Responsibilities

* Django project
* Django REST Framework
* API endpoints
* Database models
* Conversations
* Messages
* Sessions
* Document management
* Authentication where needed
* Rasa communication
* AI communication
* Django Admin
* Configuration

---

# 6. Django API

At minimum:

```text
POST /api/chat/
GET  /api/health/
```

Chat request:

```json
{
  "session_id": "demo-session-001",
  "message": "What are the requirements for Computer Science?"
}
```

Chat response:

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

The exact structure can evolve, but changes must be communicated.

---

# 7. Django Models

At minimum, consider models for:

```text
Conversation
Message
Document
DocumentChunk
```

Potential document fields:

```text
id
title
filename
source
version
status
uploaded_at
processed_at
```

Potential chunk fields:

```text
id
document
content
chunk_index
metadata
embedding
created_at
```

---

# 8. Django Admin

Django Admin should provide a simple way to:

* Upload documents.
* View documents.
* View processing status.
* Trigger processing if necessary.
* Inspect basic metadata.

The prototype does not require a custom enterprise administration dashboard.

---

# 9. Service Separation

Django should not contain all AI logic directly inside views.

Prefer service classes/modules such as:

```text
services/
├── rasa_client.py
├── rag_client.py
└── ...
```

This keeps the API layer clean.

---

# 10. Day 1 Tasks

* Create Django project.
* Configure database.
* Create health endpoint.
* Create chat endpoint.
* Create basic models.
* Create Rasa client.
* Establish React → Django communication.

---

# 11. Day 2–3

* Document models.
* Django Admin.
* Document upload.
* RAG service integration.
* Persist conversations.
* Persist messages.

---

# 12. Day 4–5

* Context handling.
* Error handling.
* Integration fixes.
* API cleanup.
* Final testing.

---

# 13. Developer 3 — Rasa Developer

## Main Responsibility

Build and maintain the Rasa conversational layer.

Primary directory:

```text
rasa/
```

---

# 14. Rasa Responsibilities

Rasa should provide:

* Dialogue management
* Session handling
* Conversation state
* Basic NLU where useful
* Conversation events
* Controlled routing toward the AI layer

Rasa should not become a huge hard-coded university knowledge system.

---

# 15. Avoid Intent Explosion

Do not create hundreds of intents such as:

```text
ask_fees
ask_registration
ask_admission
ask_computer_science
ask_diploma
ask_accommodation
ask_exam_dates
```

The system needs to understand semantic variations through the AI/RAG layer.

Rasa should focus on conversational control rather than manually representing the entire university knowledge base.

---

# 16. Example Conversation

```text
User:
What are the requirements for Computer Science?

Bot:
According to the admissions guide...

User:
What about diploma holders?

Bot:
For diploma holders, the guide states...
```

Rasa should preserve the conversational state needed to understand the follow-up.

---

# 17. Day 1 Tasks

* Create Rasa project.
* Configure basic domain.
* Configure session handling.
* Create minimal required intents/actions.
* Establish Django ↔ Rasa communication.

---

# 18. Day 2–3

* Connect Rasa to AI orchestration.
* Pass conversation context.
* Handle AI-generated responses.
* Test session continuity.

---

# 19. Day 4

Focus heavily on:

* Follow-up questions
* Context
* Query routing
* Conversation state

---

# 20. Day 5

* Fix conversation bugs.
* Test common flows.
* Test unexpected input.
* Support final integration.

---

# 21. Developer 4 — RAG + LLM Developer

## Main Responsibility

Build the AI knowledge and generation layer.

Primary directories:

```text
ai/rag/
ai/llm/
```

This is one of the most important parts of the prototype.

---

# 22. RAG Pipeline

Implement:

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
Embeddings
 ↓
pgvector
 ↓
Retrieval
 ↓
Context
 ↓
LLM
```

---

# 23. Document Extraction

The system should extract text from university PDFs.

The implementation should preserve useful document information such as:

* Page number
* Headings
* Sections
* Paragraphs
* Tables where practical

---

# 24. Chunking

Do not blindly split every document into arbitrary fixed-size blocks if structure-aware chunking is possible.

Prefer:

```text
Heading
 ↓
Section
 ↓
Paragraphs
 ↓
Chunk
```

Use token/character limits as fallback.

Each chunk should remain understandable when retrieved independently.

---

# 25. Metadata

Each chunk should retain metadata similar to:

```json
{
  "document_id": "doc-001",
  "document_title": "Admissions Guide 2026/2027",
  "section": "Bachelor of Computer Science",
  "page": 27,
  "academic_year": "2026/2027",
  "source": "Busitema University Admissions Guide"
}
```

The exact structure can evolve.

---

# 26. Embeddings

The embedding model should be separate from the LLM.

Create an abstraction where practical:

```text
EmbeddingProvider
```

This allows the embedding model to be changed later.

---

# 27. Vector Storage

Use:

```text
PostgreSQL
+
pgvector
```

unless an actual technical limitation requires a different solution.

The prototype does not need a separate vector database unless there is a clear reason.

---

# 28. Retrieval

When a user asks a question:

```text
Question
 ↓
Query embedding
 ↓
Vector search
 ↓
Relevant chunks
 ↓
Ranking
 ↓
Context
```

Retrieval should preserve source metadata.

---

# 29. LLM Integration

The prototype uses NVIDIA-hosted inference.

Use an abstraction:

```text
LLMProvider
    └── NVIDIAProvider
```

The rest of the application should not depend directly on NVIDIA-specific implementation details.

---

# 30. Grounded Generation

The LLM should receive retrieved institutional evidence as context.

The generation layer should instruct the model to:

* Use retrieved evidence.
* Avoid inventing institutional facts.
* Say when information is insufficient.
* Preserve relevant context.
* Return source references based on actual retrieval metadata.

---

# 31. Source Attribution

The response should retain:

```text
Document
Page
Section
```

Example:

```text
Sources:
Admissions Guide 2026/2027 — Page 27
```

Never generate fake sources.

---

# 32. Day 1 Tasks

The first priority is not advanced RAG.

Help establish:

```text
Django
 ↓
Rasa
 ↓
AI
 ↓
NVIDIA
```

Confirm that NVIDIA inference can be called successfully.

---

# 33. Day 2

Build:

```text
PDF
 ↓
Extraction
 ↓
Chunking
 ↓
Metadata
 ↓
Embeddings
 ↓
pgvector
```

---

# 34. Day 3

Build:

```text
Question
 ↓
Retrieval
 ↓
Context
 ↓
NVIDIA
 ↓
Grounded Answer
```

Add sources.

---

# 35. Day 4

Improve:

* Query understanding
* Query rewriting
* Retrieval
* Contextual questions
* Low-confidence handling

---

# 36. Day 5

Focus on:

* Accuracy
* Latency
* Error handling
* Integration
* Demonstration reliability

---

# 37. Developer 5 — Team Lead / Integration Developer

## Main Responsibility

The Team Lead is responsible for keeping the entire system coherent.

Primary responsibilities:

* Architecture
* Integration
* Shared interfaces
* AI orchestration
* Testing
* Documentation
* Git coordination
* Integration checkpoints
* Final prototype

The Team Lead should still contribute code.

---

# 38. AI Orchestration

The orchestration layer coordinates:

```text
Rasa
 ↓
Query understanding
 ↓
RAG
 ↓
LLM
 ↓
Response
```

Possible structure:

```text
ai/
└── orchestration/
    └── ...
```

The orchestration layer should remain simple.

Do not create an unnecessarily complex autonomous agent.

---

# 39. Integration Responsibilities

The Team Lead coordinates these checkpoints:

### Checkpoint 1

```text
React → Django
```

### Checkpoint 2

```text
Django → Rasa
```

### Checkpoint 3

```text
Django → Rasa → AI
```

### Checkpoint 4

```text
AI → RAG → NVIDIA
```

### Checkpoint 5

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
 ↓
Django
 ↓
React
```

---

# 40. Shared API Contract

The Team Lead should maintain the agreed API contract.

Initial chat request:

```json
{
  "session_id": "demo-session-001",
  "message": "What are the requirements for Computer Science?"
}
```

Initial response:

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

If the contract changes, the affected developers must be informed.

---

# 41. Git Strategy

Use one shared Git repository.

Recommended branches:

```text
main
feature/frontend
feature/django
feature/rasa
feature/rag
feature/llm
```

Developers should not directly push unfinished work to `main`.

---

# 42. Basic Git Workflow

Before starting work:

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

Then create a Pull Request.

---

# 43. Commit Messages

Good examples:

```text
Implement PDF text extraction
Add structure-aware chunking
Add document metadata
Implement pgvector retrieval
Add NVIDIA provider
Add Rasa session handling
Add chat API
Add source display
```

Avoid vague commits such as:

```text
updates
stuff
fix
final
changes
working
```

---

# 44. Pull Requests

Every PR should explain:

1. What was implemented.
2. Which files/components changed.
3. How it was tested.
4. Whether another developer needs to change anything.

Example:

```text
Implemented PDF extraction and structure-aware chunking.

Tested with:
- Admissions Guide PDF
- Academic Calendar PDF

Output:
- Page metadata preserved
- Section metadata preserved
- Chunks stored successfully

No API changes.
```

---

# 45. Integration Rules

## Rule 1

Do not redesign the architecture individually.

If you believe the architecture needs to change, discuss it with the team.

---

## Rule 2

Do not silently change shared interfaces.

If a developer changes:

```text
API response
database field
function signature
service contract
```

the affected developers must know.

---

## Rule 3

Do not commit broken code to `main`.

Test locally first.

---

## Rule 4

Do not build duplicate implementations.

For example, there should not be:

```text
Developer A's RAG
Developer B's RAG
Developer C's RAG
```

Build one agreed RAG layer.

---

## Rule 5

Avoid unnecessary dependencies.

Every dependency should have a purpose.

---

# 46. Five-Day Team Schedule

## Day 1 — Integration Skeleton

Everyone works toward one basic vertical path.

Target:

```text
React
 ↓
Django
 ↓
Rasa
 ↓
NVIDIA
 ↓
Django
 ↓
React
```

### React

Build basic chat interface.

### Django

Build API and Rasa communication.

### Rasa

Build minimal conversation/session handling.

### RAG/LLM Developer

Establish NVIDIA inference.

### Team Lead

Coordinate integration and resolve interface problems.

---

# 47. Day 2 — Knowledge Engine

Target:

```text
PDF
 ↓
Extraction
 ↓
Chunking
 ↓
Embeddings
 ↓
pgvector
```

### React

Improve response/source display.

### Django

Document models and upload workflow.

### Rasa

Connect conversational input to AI layer.

### RAG

Build ingestion pipeline.

### Team Lead

Integrate document processing with Django.

---

# 48. Day 3 — RAG + Generation

Target:

```text
Question
 ↓
Retrieval
 ↓
Evidence
 ↓
NVIDIA
 ↓
Answer
```

Everyone should work toward one functioning path.

The demonstration should now answer questions from real Busitema documents.

---

# 49. Day 4 — Context and Semantic Understanding

Target:

```text
Natural Question
 ↓
Understanding
 ↓
Context
 ↓
Retrieval
 ↓
Grounded Answer
```

Test:

```text
What are the requirements for Computer Science?

What about diploma holders?
```

and:

```text
When does registration begin?

What about first years?

And when should they report?
```

---

# 50. Day 5 — Hardening and Demo

Focus on:

* Reliability
* Error handling
* UI
* Sources
* Loading states
* Document status
* Response quality
* Latency
* Demo preparation

Do not make major architectural changes unless something is fundamentally broken.

---

# 51. Daily Integration Practice

At the end of each development session, developers should answer:

```text
What did I implement?

What works?

What is still broken?

Did I change any shared interface?

Does another developer need to change anything?

What will I work on next?
```

This should be communicated in the team's development channel.

---

# 52. Testing Responsibilities

Everyone tests their own component.

However, integration testing is shared.

Minimum tests should include:

```text
React → Django
Django → Rasa
Rasa → AI
AI → RAG
RAG → pgvector
RAG → NVIDIA
Full end-to-end
```

---

# 53. Demo Test Questions

The team should prepare real questions based on the uploaded Busitema documents.

Example:

```text
What are the requirements for Computer Science?
```

Variation:

```text
I'm a diploma holder and I want to study Computer Science. What do I need?
```

Follow-up:

```text
What about diploma holders?
```

Another flow:

```text
When does registration begin?
```

Follow-up:

```text
What about first years?
```

Follow-up:

```text
And when should they report?
```

---

# 54. Knowledge Acquisition Demo

The final demonstration should include:

```text
1. Open Django Admin
2. Upload a university PDF
3. Show processing status
4. Show that the document is indexed
5. Ask a question based on that document
6. Receive an answer
7. Display the source document/page
```

This is one of the most important proof points of the prototype.

---

# 55. What Not To Do

Do not:

* Build hundreds of university-specific intents.
* Hard-code answers just for the demo.
* Build unnecessary microservices.
* Add Kubernetes.
* Add federated learning now.
* Add multimodal learning now.
* Add voice now.
* Fine-tune an LLM now.
* Build a complicated multi-agent system.
* Introduce multiple vector databases without need.
* Rewrite the architecture every day.
* Commit unfinished experiments to `main`.

---

# 56. Definition of Team Success

The team has succeeded when the five developers' components operate as one system:

```text
                 ┌───────────────┐
                 │    React      │
                 └───────┬───────┘
                         │
                         ▼
                 ┌───────────────┐
                 │    Django     │
                 └───────┬───────┘
                         │
                         ▼
                 ┌───────────────┐
                 │     Rasa      │
                 └───────┬───────┘
                         │
                         ▼
               ┌───────────────────┐
               │ AI Orchestration  │
               └───────┬───────────┘
                       │
             ┌─────────┴─────────┐
             ▼                   ▼
       ┌───────────┐       ┌────────────┐
       │    RAG    │       │  NVIDIA    │
       └─────┬─────┘       │    LLM     │
             │             └─────┬──────┘
             │                   │
             └─────────┬─────────┘
                       ▼
                  Grounded
                   Response
                       │
                       ▼
                    React
```

The objective is not for each developer to produce an impressive isolated component.

The objective is to produce one functioning BuBot prototype that demonstrates the research concept end-to-end.
