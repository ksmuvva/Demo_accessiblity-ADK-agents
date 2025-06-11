from google.adk.agents import LlmAgent
from . import tools

keyboard_accessibility_agent = LlmAgent(
    model="gemini-1.5-flash",
    name="KeyboardAccessibilityAgent",
    description="Specialist for WCAG 2.2 keyboard accessibility (includes retained criteria 2.1.1–2.1.4) including navigation, traps, focus indicators, and character shortcuts",
    instruction="""You are a specialist agent for WCAG 2.2 keyboard accessibility testing.

Your expertise covers the keyboard-related success criteria retained in WCAG 2.2:
• 2.1.1 Keyboard navigation
• 2.1.2 No keyboard traps
• 2.1.3 Keyboard navigation (no exception)
• 2.1.4 Character key shortcuts

Process:
1. Always call the `test_keyboard_accessibility` tool
2. Analyse results and explain issues clearly
3. Give actionable recommendations
4. Do NOT ask the user follow-up questions—run the tool and respond
""",
    tools=[
        tools.test_keyboard_accessibility,
        tools.run_pa11y,
        tools.get_accessibility_tree,
    ],
) 