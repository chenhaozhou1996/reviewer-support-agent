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
    "for top-tier journals (Nature, Science, Cell, Lancet, NEJM, JOM, etc.). "
    "You have access to powerful tools:\n"
    "- Read/Glob/Grep: Read and search local manuscript files and data\n"
    "- Write: Save response drafts to files\n"
    "- WebSearch/WebFetch: Search the web for supporting references and evidence\n"
    "- paper_search: Search academic papers across arXiv, PubMed, bioRxiv, medRxiv, Google Scholar, and Semantic Scholar\n"
    "- pubmed: Search PubMed for biomedical literature, fetch article details, find related articles\n"
    "- arxiv: Search arXiv preprints, download and read papers\n\n"
    "When responding to reviewer comments:\n"
    "1. Acknowledge the reviewer's concern respectfully\n"
    "2. Use paper_search, pubmed, arxiv, and WebSearch to find supporting citations and evidence\n"
    "3. Provide a point-by-point response with evidence\n"
    "4. Quote or reference specific sections of the manuscript when relevant\n"
    "5. Be diplomatic but firm when pushing back with evidence\n"
    "6. Suggest specific manuscript revisions where appropriate\n\n"
    "Format responses in standard point-by-point rebuttal style:\n"
    "- 'Reviewer Comment:' (summarize)\n"
    "- 'Response:' (your drafted reply)\n"
    "- 'Action:' (changes made to manuscript, if any)\n\n"
    "If the user provides a file path, use Read to access the file first. "
    "If it is a directory, use Glob to find relevant files inside it."
)


async def main():
    print("=== Reviewer Support Agent ===")
    print("Tools: Read, Write, WebSearch, PubMed, arXiv, Paper Search")
    print()

    reviewer_comment = input(
        "Paste a reviewer comment, file path, or directory path:\n> "
    )

    manuscript_path = input(
        "Path to your manuscript (optional, press Enter to skip):\n> "
    ).strip()

    print("\n--- Generating response ---\n")

    # Build the prompt
    prompt_parts = [f"Reviewer comment:\n{reviewer_comment}"]
    if manuscript_path:
        prompt_parts.append(
            f"\nThe manuscript is located at: {manuscript_path}\n"
            "Read the manuscript to reference specific sections in your response."
        )
    prompt_parts.append("\nDraft a response to this reviewer comment.")
    prompt = "\n".join(prompt_parts)

    options = ClaudeAgentOptions(
        system_prompt=SYSTEM_PROMPT,
        permission_mode="bypassPermissions",
        max_turns=10,
        model="claude-opus-4-6",
        thinking={"type": "enabled", "budget_tokens": 10000},
        env={"CLAUDE_SKIP_PERMISSIONS": "1"},
        # Built-in Claude Code tools
        allowed_tools=[
            "Read",
            "Write",
            "Glob",
            "Grep",
            "WebSearch",
            "WebFetch",
            "mcp__paper_search__*",
            "mcp__pubmed__*",
            "mcp__arxiv__*",
        ],
        # MCP servers for academic research
        mcp_servers={
            "paper_search": {
                "command": "uvx",
                "args": [
                    "--from",
                    "paper-search-mcp",
                    "python",
                    "-m",
                    "paper_search_mcp.server",
                ],
                "env": {
                    "SEMANTIC_SCHOLAR_API_KEY": os.environ.get(
                        "SEMANTIC_SCHOLAR_API_KEY", ""
                    ),
                },
            },
            "pubmed": {
                "command": "npx",
                "args": ["-y", "@cyanheads/pubmed-mcp-server"],
                "env": {
                    "NCBI_API_KEY": os.environ.get("NCBI_API_KEY", ""),
                },
            },
            "arxiv": {
                "command": "uvx",
                "args": ["arxiv-mcp-server"],
                "env": {
                    "ARXIV_STORAGE_PATH": os.environ.get(
                        "ARXIV_STORAGE_PATH",
                        os.path.expanduser("~/.arxiv-papers"),
                    ),
                },
            },
        },
    )

    async for message in query(prompt=prompt, options=options):
        # Log MCP server connection status
        if isinstance(message, SystemMessage) and message.subtype == "init":
            mcp_servers = message.data.get("mcp_servers", [])
            connected = []
            for server in mcp_servers:
                status = server.get("status", "unknown")
                name = server.get("name", "unknown")
                if status == "connected":
                    connected.append(name)
                else:
                    print(f"  ⚠ {name}: {status}")
            if connected:
                print(f"  ✓ Connected: {', '.join(connected)}")
            print()

        if isinstance(message, AssistantMessage):
            for block in message.content:
                if isinstance(block, TextBlock):
                    print(block.text)
                elif hasattr(block, "name"):
                    # Tool use block — show what the agent is doing
                    tool_name = block.name
                    if tool_name.startswith("mcp__"):
                        parts = tool_name.split("__")
                        tool_name = f"{parts[1]}.{parts[2]}" if len(parts) >= 3 else tool_name
                    tool_input = getattr(block, "input", {})
                    summary = ""
                    if isinstance(tool_input, dict):
                        for key in ["file_path", "pattern", "query", "url", "prompt"]:
                            if key in tool_input:
                                val = str(tool_input[key])
                                summary = val[:80] + "..." if len(val) > 80 else val
                                break
                    print(f"  >> {tool_name}: {summary}")
        elif isinstance(message, ResultMessage):
            if message.is_error:
                print(f"Error: {message.result}")
            else:
                print("\n--- Done ---")


asyncio.run(main())
