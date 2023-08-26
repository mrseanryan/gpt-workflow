from config__database_schema_creator import EXPERT_COMMANDS
import core

command_messages = core.create_command_messages(EXPERT_COMMANDS)
previous_messages = []

def output_capabilities():
    print("Hello, I am gpt-workflow, an AI assistant. Here are my capabilities:")
    for command in EXPERT_COMMANDS:
        print(f" - {command.description.replace('Good for answering questions about', '')}")
    print("")

output_capabilities()

initial_prompt = "What is the name of your workflow? >>"
user_prompt = input(initial_prompt)

prompt_id = 1
input_prompt = "(To exit, just press ENTER) >"
while(user_prompt != None and len(user_prompt) > 0):
    print("=== === === ===")
    print(f">> {user_prompt}")
    # should route to the right 'expert'!
    rsp = core.execute_prompt(user_prompt, previous_messages, command_messages, prompt_id)
    print("=== RESPONSE ===")
    print(rsp)
    user_prompt = input(input_prompt)
    prompt_id += 1
