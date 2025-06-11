from google.adk.agents import LlmAgent
from . import tools

navigation_structure_agent = LlmAgent(
    model="gemini-1.5-flash",
    name="NavigationStructureAgent",
    description="Specialist for WCAG 2.4.x (including new 2.2 additions 2.4.11-2.4.13) navigation structure: headings, skip links, focus visibility, and page organization",
    instruction="""You are a specialist agent for WCAG 2.4.x navigation structure (WCAG 2.2).

Your focus areas include:
• 2.4.1–2.4.10 traditional navigation criteria
• NEW: 2.4.11 Focus Not Obscured (Minimum)
• NEW: 2.4.12 Focus Not Obscured (Enhanced)
• NEW: 2.4.13 Focus Appearance

Process:
1. Always run `test_navigation_structure`, `test_focus_not_obscured`, and `test_focus_appearance`.
2. Optionally call automated scanners (axe, Lighthouse) when deeper inspection is needed.
3. Summarise issues and provide actionable fixes.
""",
    tools=[
        tools.test_navigation_structure,
        tools.test_focus_not_obscured,
        tools.test_focus_appearance,
        tools.run_axe_devtools,
        tools.run_lighthouse_accessibility,
    ],
) 