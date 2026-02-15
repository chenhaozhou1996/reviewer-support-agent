# Reviewer Support Agent

An AI agent that drafts professional responses to peer review comments for top-tier journals, built with the [Claude Agent SDK](https://docs.anthropic.com/en/docs/agents/claude-agent-sdk).

## Features

- **Opus 4.6 with extended thinking** for deep reasoning on complex reviewer concerns
- **Academic paper search** via [paper-search-mcp](https://github.com/openags/paper-search-mcp) — searches arXiv, PubMed, bioRxiv, medRxiv, Google Scholar, and Semantic Scholar
- **Web search** for finding supporting references and evidence
- **File access** — read your manuscript, search across files, and save response drafts
- **Point-by-point rebuttal format** following top-tier journal conventions

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

Optional:
- `SEMANTIC_SCHOLAR_API_KEY` — for enhanced paper search (get one at https://www.semanticscholar.org/product/api)

## Usage

```bash
python main.py
```

You can either:
- **Paste** a reviewer comment directly
- **Provide a file path** to a file containing reviewer comments

## Tools

| Tool | Purpose |
|------|---------|
| Read / Glob / Grep | Read and search your manuscript files |
| Write | Save response drafts to files |
| WebSearch / WebFetch | Search the web for references |
| paper-search-mcp | Search academic papers across 7 databases |
