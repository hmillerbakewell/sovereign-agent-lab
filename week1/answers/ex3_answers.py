"""
Exercise 3 — Answers
====================
Fill this in after completing the three Rasa conversations.

CALM vs Old Rasa — what changed
---------------------------------
The old open-source Rasa approach used:
  - nlu.yml: intent training examples
  - rules.yml: explicit dialogue rules
  - FormValidationAction: Python class to parse slot values

Rasa Pro CALM uses:
  - flows.yml: natural language descriptions of what each flow does
  - from_llm slots: the LLM extracts values from conversation
  - ONE custom action: ActionValidateBooking for the business rules

The conversation is the same from the manager's perspective.
The machinery underneath is completely different.

CONVERSATION SCRIPTS
---------------------
Conversation 1 (happy path):
  You:    calling to confirm a booking
  Agent:  [asks guest count]
  You:    160 guests
  Agent:  [asks vegan count]
  You:    about 50 need vegan
  Agent:  [asks deposit]
  You:    £200 deposit
  Agent:  [confirms or escalates?]

Conversation 2 (deposit too high):
  Same as above but use a deposit above £300 (e.g. "£500 deposit").

Conversation 3 (out of scope):
  Start normally, then when asked for vegan count say something like
  "can you arrange parking for the speakers?" and observe what happens.
  Does CALM handle this differently than the old rules approach?
"""

# ── Conversation 1: Happy path ─────────────────────────────────────────────

CONVERSATION_1_TRACE = """
Your input ->  calling to confirm a booking                                                                                                                                            
How many guests are you confirming for tonight's event?
Your input ->  160 guests                                                                                                                                                              
And how many of those guests will need vegan meals?
Your input ->  about 50 need vegan                                                                                                                                                     
What deposit amount in GBP are you proposing to secure the booking?
Your input ->  £200 deposit                                                                                                                                                            
Thank you — booking confirmed. 160 guests, 50 requiring vegan meals, £200 deposit accepted. I'll send written confirmation to the organiser shortly.
Is there anything else I can help you with?
"""

CONVERSATION_1_OUTCOME = "confirmed"   # "confirmed" or "escalated"

# ── Conversation 2: Deposit too high ───────────────────────────────────────

CONVERSATION_2_TRACE = """
Your input ->  calling to confirm a booking                                                                                                                                            
How many guests are you confirming for tonight's event?
Your input ->  160 guests                                                                                                                                                              
And how many of those guests will need vegan meals?
Your input ->  about 50 need vegan                                                                                                                                                     
What deposit amount in GBP are you proposing to secure the booking?
Your input ->  £500 deposit                                                                                                                                                            
I need to check one thing with the organiser before I can confirm. The issue is: a deposit of £500 exceeds the organiser's authorised limit of £300. Can I call you back within 15 minutes?
Is there anything else I can help you with?
"""

CONVERSATION_2_OUTCOME = "escalated"   # "confirmed" or "escalated"
CONVERSATION_2_REASON  = "a deposit of £500 exceeds the organiser's authorised limit of £300"   # the reason the agent gave for escalating

# ── Conversation 3: Out of scope ───────────────────────────────────────────

CONVERSATION_3_TRACE = """
Your input ->  calling to confirm a booking                                                                                                                                            
How many guests are you confirming for tonight's event?
Your input ->  160 guests      
And how many of those guests will need vegan meals?
Your input ->  can you arrange parking for the speakers?                                                                                                                               
I can only help with confirming tonight's venue booking. For anything else, please contact the event organiser directly.
Would you like to continue with confirm booking?
"""

# Describe what CALM did after the out-of-scope message. Min 20 words.
CONVERSATION_3_WHAT_HAPPENED = """
It continued on-track with its current goal of getting the number of vegan meals from me
"""

# Compare Rasa CALM's handling of the out-of-scope request to what
# LangGraph did in Exercise 2 Scenario 3. Min 40 words.
OUT_OF_SCOPE_COMPARISON = """
LangGraph's approach happily changed to the new context, acknowledged the limitation,
and explained what was going on. It adapted to what was needed, unbound by the flows.
Rasa stayed firmly on its current step (getting the number of vegan meals),
responded unhelpfully ("I can only help with confirming tonight's venue booking." --
parking is part of tonight's booking, it just isn't following the steps that Rasa wanted to follow),
and the grammar was unwieldy ("Would you like to continue with confirm booking?")
as though it knows it should be doing "confirm booking" as flow but does not understand how to conjugate it.
"""

# ── Task B: Cutoff guard ───────────────────────────────────────────────────

TASK_B_DONE = True   # True or False

# List every file you changed.
TASK_B_FILES_CHANGED = ["exercise3_rasa/actions/actions.py"]

# How did you test that it works? Min 20 words.
TASK_B_HOW_YOU_TESTED = """
I set the time guard to be always True, then followed the happy path conversation.
As a response I got: "I need to check one thing with the organiser before I can confirm. The issue is: it is past 16:45 — insufficient time to process the confirmation before the 5 PM deadline. Can I call you back within 15 minutes?"
Which is the correct response.
"""

# ── CALM vs Old Rasa ───────────────────────────────────────────────────────

# In the old open-source Rasa (3.6.x), you needed:
#   ValidateBookingConfirmationForm with regex to parse "about 160" → 160.0
#   nlu.yml intent examples to classify "I'm calling to confirm"
#   rules.yml to define every dialogue path
#
# In Rasa Pro CALM, you need:
#   flow descriptions so the LLM knows when to trigger confirm_booking
#   from_llm slot mappings so the LLM extracts values from natural speech
#   ONE action class (ActionValidateBooking) for the business rules
#
# What does this simplification cost? What does it gain?
# Min 30 words.


# FILL ME IN

# Think about:
# - What does the LLM handle now that Python handled before?
# - What does Python STILL handle, and why (hint: business rules)?
# - Is there anything you trusted more in the old approach?


CALM_VS_OLD_RASA = """
The LLM now handles extracting information from unstructured text (.e.g a count of people),
then handing over to Python for deterministic guardrails (what time is it, capacity, vegan meal ratio),
based on that extracted information.

LLMs excel at turning unstructured data into structured, and provided we still have deterministic guardrails
then this seems a sensible approach. The lack of determinism in LLM responses is always an issue when trying to
determine the reliability of these systems, and so that is an area I would trust the new system less.

"""

# ── The setup cost ─────────────────────────────────────────────────────────

# CALM still required: config.yml, domain.yml, flows.yml, endpoints.yml,
# rasa train, two terminals, and a Rasa Pro licence.
# The old Rasa ALSO needed nlu.yml, rules.yml, and a FormValidationAction.
#
# CALM is simpler. But it's still significantly more setup than LangGraph.
# That setup bought you something specific.
# Min 40 words.


# FILL ME IN

# Be specific. What can the Rasa CALM agent NOT do that LangGraph could?
# Is that a feature or a limitation for the confirmation use case?
# Think about: can the CALM agent improvise a response it wasn't trained on?
# Can it call a tool that wasn't defined in flows.yml?

SETUP_COST_VALUE = """
Rasa's responses and flows are pre-defined by the creator.
If there are situations that are missed at compile time then there is no adaptability.

An example response issue is when the LLM model does not accept the answer:
Giving a guest count of "-5" shows  (in the thinking tokens) that the model is aware that this isn't a valid guest count,
but the only text it can respond with is "I’m sorry I am unable to understand you, could you please rephrase?" --
it can't explain to the user what has gone wrong because it has no capacity to come up with novel phrases.


An example flow issue in in the escalation message "I need to check one thing with the organiser before I can confirm. The issue is: it is past 16:45 — insufficient time to process the confirmation before the 5 PM deadline. Can I call you back within 15 minutes?
Is there anything else I can help you with?"
This response contains two questions (a separate problem), and if the user says that it isn't okay to be called back within 15 minutes
then the flow breaks - it thinks it's at the end of the booking confirmation flow. Since it can't proceed it can only respond `I’m sorry I am unable to understand you, could you please rephrase?`.
The thinking tokens show it can understand, it just can't respond.

See below:

```
I need to check one thing with the organiser before I can confirm. The issue is: it is past 16:45 — insufficient time to process the confirmation before the 5 PM deadline. Can I call you back within 15 minutes?
Is there anything else I can help you with?
Your input ->  Actually that's not okay, what other options are there?                                                                                                                 
2026-04-13 14:58:48 WARNING  rasa.utils.log_utils  - [warning  ] CompactLLMCommandGenerator.parse_commands actions='<think>
Okay, let\'s see. The user is responding to the AI\'s message about the booking confirmation. The AI mentioned that it\'s past 16:45 and there\'s insufficient time to process the confirmation before the 5 PM deadline, so they asked if they can call back within 15 minutes. Then the user says, "Actually that\'s not okay, what other options are there?"

First, I need to determine the appropriate action based on the user\'s message. The user is rejecting the proposed solution and asking for other options. The current active flow is "pattern_completed", which seems to be part of the confirm_booking flow. However, the user\'s request for alternative options might fall outside the scope of the current flow.

Looking at the available flows, there\'s "confirm_booking" and "handle_out_of_scope". The "handle_out_of_scope" flow is for requests outside booking confirmation, like parking, AV equipment, etc. But the user\'s issue here is about the booking confirmation process itself. However, the AI has already indicated a problem with the timing, and the user is seeking alternatives. Since the system can\'t process the confirmation due to the deadline, maybe there\'s no further action in the confirm_booking flow. 

The user\'s question about other options might not be covered by the existing slots in the confirm_booking flow. The slots are guest_count, vegan_count, and deposit_amount_gbp. The user isn\'t providing new information about these slots but is instead asking for alternatives to the current situation. Therefore, this might be an out-of-scope request. 

In the "handle_out_of_scope" flow, the description includes handling non-booking topics, but the user\'s query is still related to booking. However, since the system can\'t proceed with the confirmation and the user is asking for other options beyond the standard booking details, it might be considered out of scope for the confirm_booking flow. 

Alternatively, maybe the system should provide information (provide info action) about the available options. But the user is asking for other options, which might require human intervention. The "hand over" action is available when the user seems frustrated or when the request can\'t be handled by the bot. Since the user is not getting the desired response and is asking for alternatives, handing over to a human might be appropriate here.

Wait, the current active flow is "pattern_completed" with a slot "continue_conversation" that\'s a boolean. The AI\'s last message was asking if there\'s anything else they' message='No commands were parsed from the LLM actions.'
2026-04-13 14:58:48 WARNING  rasa.utils.log_utils  - [warning  ] llm_command_generator.predict_commands message='No commands were predicted as the LLM response could not be parsed or the LLM responded with an invalid command. Returning a CannotHandleCommand instead.'
I’m sorry I am unable to understand you, could you please rephrase?
```

It also can't discover tools, but since tools are an attack surface that can be seen as either good or bad depending on context.
"""
