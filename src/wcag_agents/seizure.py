from google.adk.agents import LlmAgent
from . import tools

seizure_prevention_agent = LlmAgent(
    model="gemini-1.5-flash",
    name="SeizurePreventionAgent",
    description="Specialist for WCAG 2.3.x seizure prevention including flashing content and animation controls",
    instruction="""You are a SAFETY-CRITICAL agent for WCAG 2.3.x seizure prevention.
Always run the `test_seizure_prevention` tool first.
Provide guidance to remove content that flashes more than 3 times per second or violates thresholds.
""",
    tools=[tools.test_seizure_prevention],
) 