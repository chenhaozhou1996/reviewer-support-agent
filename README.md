# Reviewer Support Agent

An AI agent that drafts professional responses to peer review comments for top-tier journals, built with the [Claude Agent SDK](https://docs.anthropic.com/en/docs/agents/claude-agent-sdk).

## Features

- **Opus 4.6 with extended thinking** for deep reasoning on complex reviewer concerns
- **3 academic MCP servers** for comprehensive literature search:
  - [paper-search-mcp](https://github.com/openags/paper-search-mcp) — arXiv, PubMed, bioRxiv, medRxiv, Google Scholar, Semantic Scholar
  - [pubmed-mcp-server](https://github.com/cyanheads/pubmed-mcp-server) — PubMed search, article details, related articles
  - [arxiv-mcp-server](https://github.com/blazickjp/arxiv-mcp-server) — arXiv search, paper download, content reading
- **Web search** for finding supporting references and evidence
- **Manuscript-aware** — optionally provide your manuscript path for context-aware responses
- **File access** — read your manuscript, search across files, and save response drafts
- **Point-by-point rebuttal format** following top-tier journal conventions

## Prerequisites

- Python 3.10+
- [uv](https://github.com/astral-sh/uv) (`brew install uv`)
- Node.js / npm (for PubMed MCP server)

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Copy `.env.example` to `.env` and add your API keys:

```bash
cp .env.example .env
```

Required:
- `ANTHROPIC_API_KEY` — your Anthropic API key

Optional (enhance search capabilities):
- `SEMANTIC_SCHOLAR_API_KEY` — [get one here](https://www.semanticscholar.org/product/api)
- `NCBI_API_KEY` — [get one here](https://www.ncbi.nlm.nih.gov/account/settings/)

## Usage

```bash
python main.py
```

You can:
- **Paste** a reviewer comment directly
- **Provide a file path** (e.g., `/path/to/reviewer_comments.tex`)
- **Provide a directory path** — the agent will search for relevant files
- **Optionally provide your manuscript path** for context-aware responses

## Tools

| Tool | Purpose |
|------|---------|
| Read / Glob / Grep | Read and search your manuscript files |
| Write | Save response drafts to files |
| WebSearch / WebFetch | Search the web for references |
| paper-search-mcp | Multi-source academic paper search (7 databases) |
| pubmed-mcp-server | PubMed biomedical literature search |
| arxiv-mcp-server | arXiv preprint search and download |
