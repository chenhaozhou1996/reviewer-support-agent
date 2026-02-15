import asyncio
import os
from claude_agent_sdk import (
    query,
    ClaudeAgentOptions,
    AssistantMessage,
    ResultMessage,
    SystemMessage,
    TextBlock,
)


SYSTEM_PROMPT = (
    "You are an expert academic researcher helping draft responses to peer review comments "
    "for top-tier journals (Nature, Science, Cell, Lancet, NEJM, etc.). "
    "You have access to powerful tools:\n"
    "- Read/Glob/Grep: Read and search local manuscript files and data\n"
    "- Write: Save response drafts to files\n"
    "- WebSearch/WebFetch: Search the web for supporting references and evidence\n"
    "- paper_search: Search academic papers across arXiv, PubMed, bioRxiv, medRxiv, Google Scholar, and Semantic Scholar\n\n"
    "When responding to reviewer comments:\n"
    "1. Acknowledge the reviewer's concern respectfully\n"
    "2. Use paper_search and WebSearch to find supporting citations and evidence\n"
    "3. Provide a point-by-point response with evidence\n"
    "4. Quote or reference specific sections of the manuscript when relevant\n"
    "5. Be diplomatic but firm when pushing back with evidence\n"
    "6. Suggest specific manuscript revisions where appropriate\n\n"
    "Format responses in standard point-by-point rebuttal style:\n"
    "- 'Reviewer Comment:' (summarize)\n"
    "- 'Response:' (your drafted reply)\n"
    "- 'Action:' (changes made to manuscript, if any)\n\n"
    "If the user provides a file path, use Read to access the file first."
)


async def main():
    reviewer_comment = input(
        "Paste a reviewer comment (or provide a file path):\n> "
    )

    print("\n--- Generating response ---\n")

    options = ClaudeAgentOptions(
        system_prompt=SYSTEM_PROMPT,
        permission_mode="bypassPermissions",
        max_turns=10,
        model="claude-opus-4-6",
        thinking={"type": "enabled", "budget_tokens": 10000},
        # Built-in Claude Code tools
        allowed_tools=[
            "Read",
            "Write",
            "Glob",
            "Grep",
            "WebSearch",
            "WebFetch",
            "mcp__paper_search__*",
        ],
        # MCP servers for academic paper search
        mcp_servers={
            "paper_search": {
                "command": "uv",
                "args": [
                    "run",
                    "--from",
                    "paper-search-mcp",
                    "-m",
                    "paper_search_mcp.server",
                ],
                "env": {
                    "SEMANTIC_SCHOLAR_API_KEY": os.environ.get(
                        "SEMANTIC_SCHOLAR_API_KEY", ""
                    ),
                },
            },
        },
    )

    async for message in query(
        prompt=f"Reviewer comment:\n{reviewer_comment}\n\nDraft a response to this reviewer comment.",
        options=options,
    ):
        # Log MCP server connection status
        if isinstance(message, SystemMessage) and message.subtype == "init":
            mcp_servers = message.data.get("mcp_servers", [])
            for server in mcp_servers:
                status = server.get("status", "unknown")
                name = server.get("name", "unknown")
                if status != "connected":
                    print(f"⚠ MCP server '{name}' status: {status}")

        if isinstance(message, AssistantMessage):
            for block in message.content:
                if isinstance(block, TextBlock):
                    print(block.text)
        elif isinstance(message, ResultMessage):
            if message.is_error:
                print(f"Error: {message.result}")


asyncio.run(main())
