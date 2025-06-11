"""Root Accessibility Testing Agent
Entry point for the WCAG multi-agent system built with Google ADK.
"""

from google.adk.agents import LlmAgent
from .wcag_agents.operable_coordinator import operable_coordinator
from .wcag_agents.tools import test_website_accessibility

root_agent = LlmAgent(
    model="gemini-1.5-flash",
    name="AccessibilityTestingSystem",
    description="Root coordinator for comprehensive WCAG 2.2 accessibility testing",
    instruction="""You are the root coordinator for the WCAG Accessibility Testing System.

Routing rules:
• Any WCAG 2.2 question → transfer_to_agent(agent_name="OperableCoordinator")
• If the user provides a URL, first run `test_website_accessibility`, then decide whether to route.
• Handle general WCAG 2.2 accessibility questions directly when appropriate.
""",
    tools=[test_website_accessibility],
    sub_agents=[operable_coordinator],
) 