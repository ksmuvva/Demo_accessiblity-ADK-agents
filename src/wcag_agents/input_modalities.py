from google.adk.agents import LlmAgent
from . import tools

input_modalities_agent = LlmAgent(
    model="gemini-1.5-flash",
    name="InputModalitiesAgent",
    description="Specialist for WCAG 2.5.x (including 2.2 additions 2.5.7 & 2.5.8) input modalities: gestures, target size, motion controls",
    instruction="""You are a specialist agent for WCAG 2.5.x input modalities (WCAG 2.2).

Focus areas:
• 2.5.1–2.5.6 legacy input success criteria
• NEW: 2.5.7 Dragging Movements
• NEW: 2.5.8 Target Size (Minimum)

Process:
1. Run `test_input_modalities`, `test_dragging_movements`, and `test_target_size_minimum`.
2. Provide concrete remediation guidance.
""",
    tools=[
        tools.test_input_modalities,
        tools.test_dragging_movements,
        tools.test_target_size_minimum,
    ],
) 