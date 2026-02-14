import asyncio
from claude_agent_sdk import query, ClaudeAgentOptions, AssistantMessage, ResultMessage, TextBlock


SYSTEM_PROMPT = (
    "You are an expert academic researcher helping draft responses to peer review comments. "
    "Given a reviewer's comment, write a clear, professional, and constructive response. "
    "Be concise and address the reviewer's concern directly. "
    "If the user provides a file path instead of pasted text, use the Read tool to read the file first, "
    "then draft responses to the reviewer comments found in it."
)


async def main():
    reviewer_comment = input("Paste a reviewer comment (or provide a file path):\n> ")

    print("\n--- Generating response ---\n")

    async for message in query(
        prompt=f"Reviewer comment:\n{reviewer_comment}\n\nDraft a response to this reviewer comment.",
        options=ClaudeAgentOptions(
            system_prompt=SYSTEM_PROMPT,
            permission_mode="bypassPermissions",
            max_turns=3,
            allowed_tools=["Read"],
        ),
    ):
        if isinstance(message, AssistantMessage):
            for block in message.content:
                if isinstance(block, TextBlock):
                    print(block.text)
        elif isinstance(message, ResultMessage):
            if message.is_error:
                print(f"Error: {message.result}")


asyncio.run(main())
