# Legal-Insights-RAG (India)

A **Retrieval-Augmented Generation (RAG)** system for querying and analyzing Indian legal decisions, case laws, and statutory documents.

This system allows users to ask natural language questions and receive accurate answers grounded in indexed Indian legal documents, utilizing semantic search, lexical retrieval, and local LLM generation.

## Architecture

The project relies on a **Hybrid RAG architecture**, combining vector search (semantic) with lexical search (keyword-based) to handle the complexities of Indian legal terminology.

Data Pipeline:

```
PDFs (Judgments/Acts)
↓
Loader
↓
Chunking
↓
Embeddings
↓
FAISS Vector Store
↓
Retriever
↓
Reranker
↓
LLM
↓
Output
```

## Tech Stack

* Python
* LangChain (Orchestration framework)
* FAISS (Local vector database)
* Sentence Transformers (Embedding generation)
* BM25 Retriever (Lexical/keyword search)
* CrossEncoder Reranker (Context optimization)
* Ollama (Local LLM for privacy and cost-efficiency)
* UV (Lightning-fast Python package manager)

**Core Libraries:**
* langchain
* langchain-community
* faiss-cpu
* sentence-transformers
* pymupdf

## Project Structure

```text
legal-insights-rag/
│
├── data/
│   └── raw/
│       └── pdfs               # Place Indian judgments (e.g., from eCourts/IndiaKanoon) here
│
├── vector_store/              # FAISS index files will be saved here
│
├── notebooks/                 # Jupyter notebooks for testing and EDA
│
├── src/
│   ├── ingestion/
│   │   ├── pdf_loader.py      # Extracts text from legal PDFs
│   │   └── chunking.py        # Splits text (semantic chunking recommended for legal text)
│   │
│   ├── embeddings/
│   │   └── embedding_model.py # Initializes HuggingFace sentence-transformers
│   │
│   ├── vector_store/
│   │   └── faiss_store.py     # Manages the FAISS index
│   │
│   ├── retrievers/
│   │   └── hybrid_retriever.py# Combines BM25 and FAISS
│   │
│   ├── reranker/
│   │   └── cross_encoder.py   # Re-ranks the combined results
│   │
│   ├── prompts/
│   │   └── legal_prompt.py    # System prompts tailored to Indian law
│   │
│   └── rag/
│       └── rag_chain.py       # The final LangChain orchestration
│
├── scripts/
│   ├── build_index.py         # Script to run ingestion and build FAISS
│
└── main.py                    # Application entry point
```

## Installation & Setup

This project uses **uv** for dependency management.

1. **Install dependencies:**

```bash
uv sync
```
*(Alternatively, use `pip install -r requirements.txt`)*

2. **Data Preparation:**
Place your downloaded legal PDFs (e.g., Supreme Court rulings, High Court bail orders) into the raw data folder:

```text
data/raw/pdfs/SC_Judgment_Kesavananda.pdf
data/raw/pdfs/HC_Bail_Order_001.pdf
```

# Build the Vector Index

To create the FAISS index, execute the ingestion script:

```bash
uv run python scripts/build_index.py
```

This process executes:
```
PDF → Chunking → Embeddings → FAISS
```
The output index files will be saved in the `vector_store/` directory.

## Execution & Example Usage

Run the main query interface:

```bash
uv run python main.py
```

**Example Interaction:**

```text
Question:
What are the primary grounds for rejecting an anticipatory bail application under Indian law?

Answer:
Based on the retrieved documents, anticipatory bail can be rejected if there is a prima facie case against the accused, a likelihood of the applicant fleeing from justice, or a risk of tampering with evidence and influencing witnesses.
```

## Under the Hood: Search & Reranking

### Hybrid Search
The system supports **Hybrid Retrieval** to capture both exact legal statutes and semantic intent:
* **BM25**: Lexical search (great for finding exact Section numbers like "Section 438 CrPC" or specific case citations).
* **FAISS**: Semantic search (great for conceptual queries like "protection against self-incrimination").

This approach significantly improves the retrieval of context from complex legal documents.

### Reranking Pipeline
Because legal accuracy is critical, initial documents are re-ordered using a **CrossEncoder Reranker**, ensuring the LLM only reads the most highly relevant context.
Pipeline:
```text
Retriever (Top 10)
↓
Reranker
↓
Refined Top 5
↓
LLM
```

## Future Enhancements

* **FastAPI Backend:** Expose the RAG pipeline as a RESTful API.
* **Web Interface:** Build a frontend using Streamlit or Gradio.
* **Automated RAG Evaluation:** Implement RAGAS to evaluate answer faithfulness and answer relevance.
* **Query Rewriting:** Automatically expand user queries with relevant Indian legal synonyms (e.g., mapping "murder" to "Section 302 IPC / Section 103 BNS").
* **Advanced Vector Stores:** Migrate from FAISS to Qdrant or Weaviate for metadata filtering (e.g., filtering by "Year" or "Court").

## Objective

This project aims to explore **RAG applied to the legal domain**, enabling intelligent natural language querying across large volumes of complex legal documents and rulings.
