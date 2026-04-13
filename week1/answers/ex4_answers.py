"""
Exercise 4 — Answers
====================
Fill this in after running exercise4_mcp_client.py.
"""

# ── Basic results ──────────────────────────────────────────────────────────

# Tool names as shown in "Discovered N tools" output.
TOOLS_DISCOVERED = [
    "search_venues",
    "get_venue_details"
  ]

QUERY_1_VENUE_NAME    = "The Haymarket Vaults"
QUERY_1_VENUE_ADDRESS = "1 Dalry Road, Edinburgh"
QUERY_2_FINAL_ANSWER  = "<think>\nOkay, let me go through the user's request again. They wanted venues in Edinburgh for 160 guests with vegan options and the full address of the best match.\n\nFirst, I used the search_venues function with min_capacity 160 and requires_vegan true. It returned two venues: The Albanach (capacity 180) and The Haymarket Vaults (capacity 160). The user probably prefers a venue that exactly matches their capacity, so The Haymarket Vaults is the better choice here.\n\nNext, I called get_venue_details for The Haymarket Vaults to get the full address. The response confirmed the address as \"1 Dalry Road, Edinburgh\". \n\nSince the user asked for the best match, and The Haymarket Vaults meets the exact capacity and vegan requirements, I should present this as the answer. The address from the details is the same as in the search results, so no new info there, but it's good to confirm. \n\nI need to make sure there's no other venue that's a better fit. The other option has a higher capacity, which might be less ideal if they want to avoid overcapacity. So sticking with The Haymarket Vaults makes sense. \n\nFinal answer should include the name and address, confirming it meets all requirements.\n</think>\n\nThe best matching venue for 160 guests with vegan options is **The Haymarket Vaults**. Its full address is:\n\n**1 Dalry Road, Edinburgh**\n\nThis venue exactly matches your guest capacity requirement and offers a vegan menu."

# ── The experiment ─────────────────────────────────────────────────────────
# Required: modify venue_server.py, rerun, revert.

EX4_EXPERIMENT_DONE = True   # True or False

# What changed, and which files did or didn't need updating? Min 30 words.
EX4_EXPERIMENT_RESULT = """
Before the change both The Haymarket and The Albanach were returned as valid venues.
Afterwards only The Haymarket was returned.
We just changed the `sovereign_agent/tools/mcp_venue_server.py` file.
No other files needed changing, it was just a change to the MCP server,
so the consumers of it needed no changes at all.
"""

# ── MCP vs hardcoded ───────────────────────────────────────────────────────

LINES_OF_TOOL_CODE_EX2 = 40   # count in exercise2_langgraph.py
LINES_OF_TOOL_CODE_EX4 = 25   # count in exercise4_mcp_client.py

# What does MCP buy you beyond "the tools are in a separate file"? Min 30 words.
MCP_VALUE_PROPOSITION = """
You can create a single resource with an abstraction boundary -
the same MCP server can serve many clients, sitting in a separate trust environment,
and can be tested separately.
Many LLM clients now support being passed an MCP URL directly as well,
so the integration is easy for them (less relevant for our use case where we're running these locally).
You can also update the MCP server in isolation and all the clients will see the updates
without needing any change in their code or configuration.
"""

# ── PyNanoClaw architecture — SPECULATION QUESTION ─────────────────────────
#
# (The variable below is still called WEEK_5_ARCHITECTURE because the
# grader reads that exact name. Don't rename it — but read the updated
# prompt: the question is now about PyNanoClaw, the hybrid system the
# final assignment will have you build.)
#
# This is a forward-looking, speculative question. You have NOT yet seen
# the material that covers the planner/executor split, memory, or the
# handoff bridge in detail — that is what the final assignment (releases
# 2026-04-18) is for. The point of asking it here is to check that you
# have read PROGRESS.md and can imagine how the Week 1 pieces grow into
# PyNanoClaw.
#
# Read PROGRESS.md in the repo root. Then write at least 5 bullet points
# describing PyNanoClaw as you imagine it at final-assignment scale.
#
# Each bullet should:
#   - Name a component (e.g. "Planner", "Memory store", "Handoff bridge",
#     "Rasa MCP gateway")
#   - Say in one clause what that component does and which half of
#     PyNanoClaw it lives in (the autonomous loop, the structured agent,
#     or the shared layer between them)
#
# You are not being graded on getting the "right" architecture — there
# isn't one right answer. You are being graded on whether your description
# is coherent and whether you have thought about which Week 1 file becomes
# which PyNanoClaw component.
#
# Example of the level of detail we want:
#   - The Planner is a strong-reasoning model (e.g. Nemotron-3-Super or
#     Qwen3-Next-Thinking) that takes the raw task and produces an ordered
#     list of subgoals. It lives upstream of the ReAct loop in the
#     autonomous-loop half of PyNanoClaw, so the Executor never sees an
#     ambiguous task.

WEEK_5_ARCHITECTURE = """
- Long-term memory: Stores memory between sessions, needs to be accessible to both halves.
- Planner: This is a powerful model that can determine what to do next and then hand over tasks to the weaker models, lives upstream of the main ReAct loop in the autonomous loop.
- Observability: Determine what happened and why. Lives in in the shared layer as we need unified observability no matter which half is acting.
- MCP Server: Both sides need access to tools - the autonomous loop can make better use of the flexibility of an MCP server, but this is more dangerous than the structured approach.
- Handoff bridge: This component lets the two halves signal that the task is being passed back to the other, it's necessarily in the shared layer.
"""

# ── The guiding question ───────────────────────────────────────────────────
# Which agent for the research? Which for the call? Why does swapping feel wrong?
# Must reference specific things you observed in your runs. Min 60 words.

GUIDING_QUESTION_ANSWER = """
Research is probably best handled by the autonomous loop - we don't have a fixed flow for what needs to happen,
although we still need proper safety checks from the tool that handles web search.
Its capacity for destructive action is limited.

The call, on the other hand, needs to achieve certain clear goals, and no more.
It's more expensive, has higher impact on the outside world,
and has a flow we can define in advance.

Swapping these would require research to follow a set path (a problem if there is no answer available,
as we saw when I tried to give nonsense answers like '-5 guests'),
or let the autonomous loop get hijacked and taken off topic due to a user response (as we saw when we asked about train times).
"""