from google.adk.agents import LlmAgent
from .keyboard import keyboard_accessibility_agent
from .timing import timing_controls_agent
from .seizure import seizure_prevention_agent
from .navigation import navigation_structure_agent
from .input_modalities import input_modalities_agent

operable_coordinator = LlmAgent(
    model="gemini-1.5-flash",
    name="OperableCoordinator",
    description="WCAG Principle 2 'Operable' coordinator managing 5 specialist agents",
    instruction="""You are the coordinator for WCAG Principle 2 (Operable).
Route user requests to the correct specialist using transfer_to_agent.
- Keyboard/focus → KeyboardAccessibilityAgent
- Timing/timeouts → TimingControlsAgent
- Flashing/seizures → SeizurePreventionAgent
- Navigation/heading → NavigationStructureAgent
- Touch/pointer → InputModalitiesAgent
If the request is generic (e.g. "check accessibility" or no clear keyword), sequentially ask **all five sub-agents** to run their default tests and aggregate the results. Only ask a clarifying question when truly necessary to choose between overlapping specialties.
""",
    sub_agents=[
        keyboard_accessibility_agent,
        timing_controls_agent,
        seizure_prevention_agent,
        navigation_structure_agent,
        input_modalities_agent,
    ],
) 