from prompts_dot_graph_creator import EXPERT_COMMANDS, GetPromptToDescribeWorkflow
import core

def test():
    command_messages = core.create_command_messages(EXPERT_COMMANDS)

    decisions_tests_first = [
        {
            "name": "Simple workflow to model a tree of decisions",
            "prompts": [
                "Create a flow that makes a series of decisions about whether to approve a mortgage application"
            ]
        }
    ]

    decisions_tests = [
        {
            "name": "Simple workflow to model a tree of decisions",
            "prompts": [
                "Create a flow that makes a series of decisions about whether to approve a mortgage application. The criteria are: good credit score, income at least 50000 USD, employed at least 2 years, can make a down payment of at least 20%, has no criminal record in last 5 years.",
                "Create a flow that makes a series of decisions about whether to recommend a job interview candidate.",
                "Create a flow that makes a series of decisions about an animal, to decide what kind of animal is it",
            ]
        }
    ]

    list_tests = [
        {
            "name": "Simple workflow adding an item to a list",
            "prompts": [
                "Create a flow that takes a list and adds an item of the same type",
                "Create a flow that takes two lists and concatenates them",
                "Create a flow that takes a list and an object. Call another flow to get a boolean result. If the boolean is true, then add the item to the list."
            ]
        },
        {
            "name": "Workflow that iterates over items in a list",
            "prompts": [
                "Create a flow that iterates over items in a list, performing an action on each item",
                "Create a flow that iterates over Job Applications in a list. For each Job Application, call another flow that checks if the application should proceed to interview stage",
            ]
        }
    ]

    describe_tests = [
        {
            "name": "Describe the given workflow",
            "prompts": [
                GetPromptToDescribeWorkflow(""""
digraph G {

  // start
  start [shape=ellipse, label="Start"];

  // decision_credit_score
  start -> decision_credit_score;
  decision_credit_score [shape=Mdiamond, label="Credit Score > 700?"];

  // decision_income
  decision_credit_score -> decision_income;
  decision_income [shape=Mdiamond, label="Income > $50,000?"];

  // decision_employment
  decision_income -> decision_employment;
  decision_employment [shape=Mdiamond, label="Employment > 2 years?"];

  // decision_down_payment
  decision_employment -> decision_down_payment;
  decision_down_payment [shape=Mdiamond, label="Down Payment > 20%?"];

  // approve
  decision_down_payment -> approve;
  approve [shape=box, label="Approve"];

  // reject
  decision_credit_score -> reject;
  reject [shape=box, label="Reject"];

  decision_income -> reject;
  decision_employment -> reject;
  decision_down_payment -> reject;
}
                """),
                GetPromptToDescribeWorkflow(""""
digraph G {

  // start
  start [shape=ellipse, label="Start"];

  // decision_has_feathers
  start -> decision_has_feathers;
  decision_has_feathers [shape=Mdiamond, label="Has feathers?"];

  // decision_can_fly
  decision_has_feathers -> decision_can_fly;
  decision_can_fly [shape=Mdiamond, label="Can fly?"];

  // decision_has_fins
  decision_has_feathers -> decision_has_fins;
  decision_has_fins [shape=Mdiamond, label="Has fins?"];

  // Hawk
  decision_can_fly -> Hawk;
  Hawk [shape=box, label="Hawk"];

  // Penguin
  decision_can_fly -> Penguin;
  Penguin [shape=box, label="Penguin"];

  // Dolphin
  decision_has_fins -> Dolphin;
  Dolphin [shape=box, label="Dolphin"];

  // Bear
  decision_has_fins -> Bear;
  Bear [shape=box, label="Bear"];
}
                """)
            ]
        }
    ]

    irrelevant_tests = [
        {
            "name": "Irrelevant prompts",
            "prompts": [
                # other prompts, that should NOT be handled by the Commands:
                "what is 2 + 5 divided by 10 ?",
                "Who won the battle of Agincourt, and why was it fought?",
                "What is my favourite color?",
           ]
        }
    ]

    tests = decisions_tests_first + decisions_tests + list_tests + describe_tests + irrelevant_tests

    # for debugging:
    # tests = decisions_tests_first # xxx

    prompt_id = 1
    for test in tests:
        previous_messages = []
        print(f"[[[TEST {test['name']}]]]")
        for user_prompt in test['prompts']:
            print("---")
            print(f">> {user_prompt}")
            # should route to the right 'expert' chain!
            rsp = core.execute_prompt(user_prompt, previous_messages, command_messages, prompt_id)
            print(rsp)
            prompt_id += 1
