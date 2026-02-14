# Reviewer Support Agent

An AI agent that drafts professional responses to peer review comments, built with the [Claude Agent SDK](https://docs.anthropic.com/en/docs/agents/claude-agent-sdk).

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Copy `.env.example` to `.env` and add your Anthropic API key:

```bash
cp .env.example .env
```

## Usage

```bash
python main.py
```

You can either:
- **Paste** a reviewer comment directly
- **Provide a file path** to a file containing reviewer comments
