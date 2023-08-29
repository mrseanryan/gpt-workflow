from workflow_trainingset_creator import EXPERT_COMMANDS
import core

def test():
    command_messages = core.create_command_messages(EXPERT_COMMANDS)

    tests = [
        {
            "name": "Generate training data for 10 workflows",
            "prompts": [
                "Create training data with 10 workflows"
            ]
        }
    ]

    for test in tests:
        previous_messages = []
        print(f"[[[TEST {test['name']}]]]")
        for user_prompt in test['prompts']:
            print("---")
            print(f">> {user_prompt}")
            # should route to the right 'expert' chain!
            rsp = core.execute_prompt(user_prompt, previous_messages, command_messages)
            print(rsp)
