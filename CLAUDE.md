# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

ArkUI Lifecycle Analysis RAG System - A modular Python project that uses RAG (Retrieval-Augmented Generation) to analyze ArkUI custom component lifecycle from PDF documentation. The system extracts lifecycle function call sequences from ArkTS code examples using vector search and LLM analysis.

## Key Commands

### Initial Setup
```bash
# Install dependencies
pip install -r requirements.txt

# Copy and configure environment variables
cp .env.example .env
# Edit .env and add your OPENAI_API_KEY
```

### Running the System

**First-time indexing** (only needed once):
```bash
python main.py index
```
This creates the vector store in `./vector_store/` from the PDF in `data/docs/`.

**Normal analysis run**:
```bash
python main.py analyze
# or simply
python main.py
```
Reads from `data/inputs/input.txt` by default, outputs to `data/outputs/`.

**Advanced usage**:
```bash
# Custom input file
python main.py analyze --input data/inputs/custom.txt

# Custom output filename (automatically saves as .json)
python main.py analyze --output result.json

# Force reindex
python main.py index --force

# Custom config file
python main.py analyze --config custom_config.yaml
```

### Jupyter Notebook
```bash
jupyter notebook notebooks/arkUI.ipynb
```

### Legacy Script
The old monolithic script still works:
```bash
python arkui_lifecycle_rag.py
```

## Architecture

### Modular Structure

The codebase is organized into clean, separated modules:

**src/config.py** - Configuration management:
- `Config` class: Centralizes all configuration with default values
- `load_from_yaml()`: Loads settings from YAML file
- `PROMPT_TEMPLATE`: Structured prompt for extracting lifecycle functions in JSON format
- Supports both default values and YAML overrides

**src/vectorstore.py** - Vector database operations:
- `VectorStoreManager` class: Encapsulates all vector store operations
- `load_and_index_pdf()`: Loads PDF, splits into chunks, creates Chroma vector store
- `load_vectorstore()`: Loads existing vector store with validation
- `get_retriever()`: Returns configured retriever for RAG chain

**src/rag_engine.py** - Core RAG logic:
- `RAGEngine` class: Orchestrates the RAG analysis pipeline
- `build_chain()`: Constructs the RAG pipeline (retriever → format → prompt → LLM → parser)
- `analyze()`: Main analysis method that processes queries

**src/utils.py** - Helper functions:
- `read_input_file()`: Safe file reading with validation
- `save_output()`: Saves results with timestamp support
- `format_docs()`: Formats retrieved documents with metadata
- `print_banner()`: Console output formatting

**main.py** - Command-line interface:
- Uses `argparse` for CLI with subcommands (index, analyze)
- Coordinates all modules: Config → VectorStoreManager → RAGEngine
- Supports flexible configuration via command-line arguments

### Data Flow

1. **Indexing Phase** (one-time):
   ```
   PDF (data/docs/)
     → PyPDFLoader
     → RecursiveCharacterTextSplitter
     → OpenAIEmbeddings
     → Chroma vector store (vector_store/)
   ```

2. **Analysis Phase** (repeated use):
   ```
   Input scenario (data/inputs/)
     → Retriever (Top-k search)
     → Format context with metadata
     → Prompt template
     → LLM (OpenAI-compatible)
     → JSON extraction & normalization
     → JSON output (data/outputs/*.json)
   ```

   **Output Processing**:
   - Extracts JSON from markdown code blocks (if present)
   - Normalizes `scope` values (`both` → `component`)
   - Handles instance-based function names (e.g., `Component.method`)
   - Saves as formatted `.json` file directly

### Configuration System

Configuration is layered:
1. **Default values** in `src/config.py`
2. **YAML file** (`config.yaml`) overrides defaults
3. **Command-line args** override both

Key parameters in `config.yaml`:
- `chunk_size`: 1000 (document splitting size)
- `chunk_overlap`: 200 (overlap for context continuity)
- `retriever_k`: 4 (number of chunks to retrieve)
- `model_name`: "deepseek-chat" (any OpenAI-compatible model)
- `temperature`: 0 (deterministic JSON output)

### Output Format

The system generates JSON with this structure:
```json
{
  "lifecycle": {
    "functions": [{"name": "...", "scope": "...", "description": "..."}],
    "order": [{"pred": "...", "succ": "..."}],
    "dynamicBehavior": "..."
  }
}
```

### Directory Organization

```
src/                  # All source code (modular)
data/                 # All data files
  ├── docs/           # PDF documentation
  ├── inputs/         # ArkTS code scenarios
  └── outputs/        # Generated analysis results (organized)
      ├── json/       # Python RAG generated JSON files
      ├── visualizations/  # TypeScript generated DOT files
      ├── legacy/     # Old .txt format files
      └── archives/   # Archived/temporary files
scripts/              # Utility scripts
  └── organize_outputs.py  # Organize output directory
notebooks/            # Jupyter notebooks for exploration
vector_store/         # Chroma DB (auto-generated, in .gitignore)
```

## Key Implementation Details

**Vector Store**: Uses Chroma with OpenAI embeddings. VectorStoreManager handles all operations and validates store existence before use.

**Error Handling**: Each module has proper error handling with informative messages. VectorStoreManager raises `FileNotFoundError` if indexing hasn't been performed (src/vectorstore.py:54-58).

**Context Formatting**: Retrieved documents include source metadata (file path and page number) before being passed to the LLM (src/utils.py:40-49).

**Prompt Engineering**: The template in `src/config.py` explicitly requests JSON-only output with structured examples to guide the LLM response format.

**CLI Design**: The main.py uses argparse with subcommands for clean separation of index and analyze operations. Default command is "analyze" for convenience.

## Recommended Parameter Tuning

- **Beginners**: Use defaults (`chunk_size=1000`, `chunk_overlap=200`, `retriever_k=4`, `temperature=0`)
- **Missing context**: Increase `retriever_k` or `chunk_size/overlap` in `config.yaml`
- **Too much noise**: Decrease `retriever_k` or `chunk_overlap`
- **Unstable output**: Ensure `temperature=0` for deterministic JSON

## Legacy Code

The old monolithic `arkui_lifecycle_rag.py` is still present for backward compatibility but is not the recommended approach. All new development should use the modular structure in `src/` with `main.py` as the entry point.
