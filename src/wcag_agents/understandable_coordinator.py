from google.adk.agents import LlmAgent
from .readable import readable_agent
from .predictable import predictable_agent
from .input_assistance import input_assistance_agent

understandable_coordinator = LlmAgent(
    model="gemini-1.5-flash",
    name="UnderstandableCoordinator",
    description="WCAG Principle 3 'Understandable' coordinator managing 3 specialist agents",
    instruction="""You are the coordinator for WCAG Principle 3 (Understandable).
Route user requests to the correct specialist using transfer_to_agent.
 - Readability/language → ReadableAgent
 - Predictability/context-change → PredictableAgent
 - Forms/errors/authentication → InputAssistanceAgent
If the request is generic (e.g., 'check understandable compliance') or no clear keyword, sequentially ask all three sub-agents to run their default tests and aggregate the results. Only ask a clarifying question when truly necessary to choose between overlapping specialties.
""",
    sub_agents=[
        readable_agent,
        predictable_agent,
        input_assistance_agent,
    ],
) 