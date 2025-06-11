from google.adk.agents import LlmAgent
from . import tools

input_assistance_agent = LlmAgent(
    model="gemini-1.5-flash",
    name="InputAssistanceAgent",
    description="Specialist for WCAG 3.3.x input assistance and error prevention criteria",
    instruction="""You are a specialist agent for WCAG 3.3 (Input Assistance).

Your scope includes criteria 3.3.1 through 3.3.9.

Process:
1. Always call the `test_input_assistance` tool on the provided URL.
2. Summarise form/input issues and provide actionable remediation steps.
""",
    tools=[tools.test_input_assistance],
) 