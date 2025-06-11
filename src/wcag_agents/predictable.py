from google.adk.agents import LlmAgent
from . import tools

predictable_agent = LlmAgent(
    model="gemini-1.5-flash",
    name="PredictableAgent",
    description="Specialist for WCAG 3.2.x predictable interaction criteria",
    instruction="""You are a specialist agent for WCAG 3.2 (Predictable).

Your scope covers criteria 3.2.1 through 3.2.6.

Process:
1. Always call the `test_predictability` tool on the provided URL.
2. Summarise any potential unpredictability and propose fixes.
""",
    tools=[tools.test_predictability],
) 