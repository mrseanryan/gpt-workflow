from config__database_schema_creator import EXPERT_COMMANDS
import core

def test():
    command_messages = core.create_command_messages(EXPERT_COMMANDS)

    tests = [
        {
            "name": "Simple workflow to model a tree of decisions",
            "prompts": [
                "Create a flow that makes a series of decisions about whether to approve a mortgage application",
                "Create a flow that makes a series of decisions about whether to recommend a job interview candidate.",
                "Create a flow that makes a series of decisions about an animal, to decide what kind of animal is it",
            ]
        },
        {
            "name": "Simple workflow adding an item to a list",
            "prompts": [
                "Create a flow that takes a list and adds an item of the same type",
                "Create a flow that takes two lists and concatenates them",
                "Create a flow that takes a list and an object. Call another flow to get a boolean result. If the boolean is true, then add the item to the list."
            ]
        },
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
