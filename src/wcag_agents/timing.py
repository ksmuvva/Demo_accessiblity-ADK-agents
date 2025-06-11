from google.adk.agents import LlmAgent
from . import tools

timing_controls_agent = LlmAgent(
    model="gemini-1.5-flash",
    name="TimingControlsAgent",
    description="Specialist for WCAG 2.2.x timing controls including timeouts, auto-playing content, and timing adjustments",
    instruction="""You are a specialist agent for WCAG 2.2.x timing controls.

Your expertise covers WCAG 2.2.1 through 2.2.6.

Process:
1. Always call the `test_timing_controls` tool on the provided URL
2. Summarise issues and give clear remediation steps
""",
    tools=[tools.test_timing_controls],
) 