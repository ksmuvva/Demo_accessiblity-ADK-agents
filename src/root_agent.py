"""Root Accessibility Testing Agent
Entry point for the WCAG multi-agent system built with Google ADK.
"""

from google.adk.agents import LlmAgent
from .wcag_agents.operable_coordinator import operable_coordinator
from .wcag_agents.understandable_coordinator import understandable_coordinator
from .wcag_agents.tools import test_website_accessibility

root_agent = LlmAgent(
    model="gemini-1.5-flash",
    name="AccessibilityTestingSystem",
    description="Root coordinator for comprehensive WCAG Principles 2 & 3 accessibility testing",
    instruction="""You are the root coordinator for the WCAG Accessibility Testing System.

Routing rules:
• WCAG 2.x questions → transfer_to_agent(agent_name='OperableCoordinator')
• WCAG 3.x questions → transfer_to_agent(agent_name='UnderstandableCoordinator')
• If the user provides a URL with no specific principle, first run `test_website_accessibility`, then route to both coordinators sequentially and aggregate the results.
• Handle high-level WCAG questions directly when simple enough.
""",
    tools=[test_website_accessibility],
    sub_agents=[operable_coordinator, understandable_coordinator],
) 