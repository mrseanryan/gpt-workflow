from command import Command

# note: Instead of this steps-in-single-prompt approach, we could have an inter-dependent chain, to collect info about the app, THEN try to generate.
# BUT the step-by-step approach works really well, at least with Chat-GPT3.5 Turbo.

create_dot_flowchart__expert_template = """You are Workflow Creator Bot, a bot that knows how to create a simple DOT format flow chart.
You are great at answering questions about creating and altering a flow chart.

When you don't know the answer to a question, do not answer.

You are an AI assistant to assist an application developer with the creation of the flow chart via natural language input.

The output MUST be in DOT format as used by the graphviz tool only, based on the following example:
```
digraph G {

  // decision_has_feathers
  start -> decision_has_feathers;
  decision_has_feathers -> decision_can_fly
  decision_has_feathers -> decision_has_fins

  // decision_can_fly
  decision_can_fly -> end_Hawk
  decision_can_fly -> end_Penguin

  // decision_has_fins
  decision_has_fins -> end_Dolphin
  decision_has_fins -> end_Bear

  decision_has_feathers [shape=Mdiamond, label="Has feathers?"];
  decision_can_fly [shape=Mdiamond, label="Can fly?"];
  decision_has_fins [shape=Mdiamond, label="Has fins?"];
}
```

IMPORTANT: Nodes of the flow digraph MUST be named to match this whitelist:
- start, decision_<identifier>, end_<identifier>, create_list_enumerator_<identifier>, has_list_enumerator_more_items_<identifier>, get_next_item_from_enumerator_<identifier>, variable_<identifier>, parameter_<identifier>, call_flow_<identifier>, other_<identifier>

IMPORTANT: Only output valid DOT format as used by the graphviz tool.
"""

describe_dot_flowchart__expert_template = """
If the user asked for a description or summary of the DOT format flow chart then:
- provide an explanation of the flow, and an overall summary of the flow
- use clear natural language, in a concise, friendly tone.
"""

# Each expert is a prompt that knows how to handle one type of user input
EXPERT_COMMANDS = [
    Command('describe_dot_workflow', describe_dot_flowchart__expert_template, "Good for describing a workflow given in DOT notation, summarizing its activity and its general purpose"),
    # Placing this last, so that its IMPORTANT message about whitelist is not ignored (LLMs tend to ignore content in middle)
    # An approach like LangChain's MULTI_PROMPT_ROUTER_TEMPLATE would avoid this problem.
    Command('create_dot_workflow', create_dot_flowchart__expert_template, "Good for answering questions about creating a workflow in DOT notation"),
]

def GetPromptToDescribeWorkflow(dotText):
    return f"""Descibe this workflow: ```{dotText}```"""
