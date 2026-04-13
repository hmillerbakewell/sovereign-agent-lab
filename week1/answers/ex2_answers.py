"""
Exercise 2 — Answers
====================
Fill this in after running exercise2_langgraph.py.
Run `python grade.py ex2` to check for obvious issues.
"""

# ── Task A ─────────────────────────────────────────────────────────────────

# List of tool names called during Task A, in order of first appearance.
# Look at [TOOL_CALL] lines in your terminal output.
# Example: ["check_pub_availability", "get_edinburgh_weather"]

TASK_A_TOOLS_CALLED = [
    "check_pub_availability","calculate_catering_cost","get_edinburgh_weather","generate_event_flyer"]

# Which venue did the agent confirm? Must be one of:
# "The Albanach", "The Haymarket Vaults", or "none"
TASK_A_CONFIRMED_VENUE = "The Albanach"

# Total catering cost the agent calculated. Float, e.g. 5600.0
# Write 0.0 if the agent didn't calculate it.
TASK_A_CATERING_COST_GBP = 5600.0

# Did the weather tool return outdoor_ok = True or False?
TASK_A_OUTDOOR_OK = True

# Optional — anything unexpected.
# If you used a non-default model via RESEARCH_MODEL env var, note it here.
# Example: "Used nvidia/nemotron-3-super-120b-a12b for the agent loop."
TASK_A_NOTES = ""

# ── Task B ─────────────────────────────────────────────────────────────────
#
# The scaffold ships with a working generate_event_flyer that has two paths:
#
#   - Live mode: if FLYER_IMAGE_MODEL is set in .env, the tool calls that
#     model and returns a real image URL.
#   - Placeholder mode: otherwise (the default) the tool returns a
#     deterministic placehold.co URL with mode="placeholder".
#
# Both paths return success=True. Both count as "implemented" for grading.
# This is not the original Task B — the original asked you to write a direct
# FLUX image call, but Nebius removed FLUX on 2026-04-13. See CHANGELOG.md
# §Changed for why we pivoted the task.

# Did your run of the flyer tool produce a success=True result?
# (This will be True for both live and placeholder mode — both are valid.)
TASK_B_IMPLEMENTED = True   # True or False

# Which path did your run take? "live" or "placeholder"
# Look for the "mode" field in the TOOL_RESULT output of Task B.
# If you didn't set FLYER_IMAGE_MODEL in .env, you will get "placeholder".
TASK_B_MODE = "placeholder"

# The image URL returned by the tool. Copy exactly from your terminal output.
# In placeholder mode this will be a placehold.co URL.
# In live mode it will be a provider CDN URL.
TASK_B_IMAGE_URL = "https://placehold.co/1200x628/1a1a2e/eaeaea?text=The+Haymarket+Vaults+%7C+160+guests&id=2ef939fbbaf6"

# The prompt sent to the image model. Copy from terminal output.
TASK_B_PROMPT_USED = "FILL_ME_IN"

# Why did the agent's behaviour NOT change when Nebius removed FLUX?
# One sentence. This is the point of the lesson.
TASK_B_WHY_AGENT_SURVIVED = """
Because the tool provided an abstraction to the model - the model has no notion
of what the tool does, only that what it has sent to the tool and what the tool has responded.
"""

# ── Task C ─────────────────────────────────────────────────────────────────

# Scenario 1: first choice unavailable
# Quote the specific message where the agent changed course. Min 20 words.
SCENARIO_1_PIVOT_MOMENT = """
  [TOOL_RESULT]  ← check_pub_availability: {"success": true, "pub_name": "The Bow Bar", "address": "80 West Bow, Edinburgh", "capacity": 80, "vegan": true, "status": "full", "meets_all_constraints": false}
The pub does not meet all requirements, so it didn't follow through with the usual plan.
"""

SCENARIO_1_FALLBACK_VENUE = "The Albanach"

# Scenario 2: impossible constraint (300 guests)
# Did the agent recommend a pub name not in the known venues list?
SCENARIO_2_HALLUCINATED = False   # True or False

# Paste the final [AI] message.
SCENARIO_2_FINAL_ANSWER = """
<think>\nOkay, let's see. The user is looking for a venue in Edinburgh that can accommodate 300 people with vegan options. The known venues are The Albanach, The Haymarket Vaults, The Guilford Arms, and The Bow Bar. I've checked each one using the check_pub_availability function.\n\nThe Albanach has a capacity of 180, which is too small. The Haymarket Vaults can only hold 160, also too small. The Guilford Arms has 200 capacity but doesn't offer vegan options. The Bow Bar has 80 capacity and is already full. None of these venues meet both the capacity and vegan requirements. So, I need to inform the user that none of the available venues can handle their request. They might need to look for alternative options or adjust their requirements.\n</think>\n\nNone of the known Edinburgh venues can accommodate 300 guests with vegan options. The maximum capacity among available venues is 200 (The Guilford Arms), but it doesn't offer vegan options. The Bow Bar, while vegan-friendly, is currently full and only holds 80 guests. Would you like me to suggest alternative solutions or adjust any requirements?
"""

# Scenario 3: out of scope (train times)
# Did the agent try to call a tool?
SCENARIO_3_TRIED_A_TOOL = False   # True or False

SCENARIO_3_RESPONSE = "<think>\nOkay, the user is asking about the last train time from Edinburgh Waverley to London tonight. Let me check the tools provided.\n\nLooking at the available functions: check_pub_availability, get_edinburgh_weather, calculate_catering_cost, generate_event_flyer. None of these are related to train schedules. The functions are for checking pub availability, weather, catering costs, and generating flyers. \n\nSince there's no tool for train times, I can't use any of the provided functions to answer this. I need to inform the user that I don't have access to that information and suggest they check a train service website or app.\n</think>\n\nI don't have access to real-time train schedules or transportation data. For the most accurate information about the last train from Edinburgh Waverley to London, I recommend checking:\n1. The National Rail website (www.nationalrail.co.uk)\n2. Train service apps like Citymapper or Trainline\n3. The specific train operator's website (e.g., LNER)\n\nWould you like help with anything related to Edinburgh pubs, weather, or event planning instead?"

# Would this behaviour be acceptable in a real booking assistant? Min 30 words.
SCENARIO_3_ACCEPTABLE = """
It's definitely better than mistakenly trying to book a pub (which it can do, but which the user didn't want it to do),
and the hint back to the user of what it can do is helpful.
Recommending places to look up train timetables is potentially helpful (if not hallucinated),
and it's very good that it didn't make up a time when it has no actual access to the data.
"""

# ── Task D ─────────────────────────────────────────────────────────────────

# Paste the Mermaid output from `python exercise2_langgraph.py task_d` here.
TASK_D_MERMAID_OUTPUT = """
---
config:
  flowchart:
    curve: linear
---
graph TD;
        __start__([<p>__start__</p>]):::first
        agent(agent)
        tools(tools)
        __end__([<p>__end__</p>]):::last
        __start__ --> agent;
        agent -.-> __end__;
        agent -.-> tools;
        tools --> agent;
        classDef default fill:#f2f0ff,line-height:1.2
        classDef first fill-opacity:0
        classDef last fill:#bfb6fc
"""

# Compare the LangGraph graph to exercise3_rasa/data/flows.yml. Min 30 words.
TASK_D_COMPARISON = """
Rasa explicitly defines two flows:
- confirm_booking
- handle_out_of_scope

The langgraph diagram only shows a core loop.

Rasa's flows also allow for asking questions of the user (remaining statefully within the flow),
but the langgraph diagram only responds to the user once and then stops (stateless between user messages).
"""

# ── Reflection ─────────────────────────────────────────────────────────────

# The most unexpected thing the agent did. Min 40 words.
# Must reference a specific behaviour from your run.

MOST_SURPRISING = """
In Task A the agent did check both venues, even though the first one was already meeting all constraints.
This is in line with the user's request ("Check The Albanach and The Haymarket Vaults")
but not in line with the user's intent (find a suitable venue).
I do not know which behaviour I would prefer to see here - the observed one is probably the better one
(it's a non-destructive action so safe to perform an extra call).
"""