from google.adk.agents import LlmAgent
from . import tools

readable_agent = LlmAgent(
    model="gemini-1.5-flash",
    name="ReadableAgent",
    description="Specialist for WCAG 3.1.x readability and language criteria",
    instruction="""You are a specialist agent for WCAG 3.1 (Readable).

Your domain covers criteria 3.1.1 through 3.1.6.

Process:
1. Always call the `test_readability` tool on the provided URL.
2. Summarise detected issues and provide concrete remediation guidance.
""",
    tools=[tools.test_readability],
) 