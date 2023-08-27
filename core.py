import service_dot_parser
import service_chat

# DEV note: NOT using langchain.
# Tried using langchain but it's validation gets in the way of more complex prompts.
# And seems simpler to code direct, not via a complicated framework.

def create_command_messages(expert_commands):
    messages = []
    for command in expert_commands:
        messages.append({'role':'system', 'content': command.expert_template })

    return messages

def process_response(rsp, prompt_id):
    if service_dot_parser.is_dot_response(rsp):
        return service_dot_parser.parse_dot_and_return_human(rsp, prompt_id)
    return rsp

def execute_prompt(user_prompt, previous_messages, command_messages, prompt_id):
    # TODO: Route to the right 'expert' chain
    # Falls back to the default chain, which means sending the plain user prompt to the LLM

    user_message = {'role':'user', 'content': user_prompt }

    messages = command_messages + previous_messages + [user_message]

    rsp = service_chat.send_prompt_messages(messages)

    previous_messages.append(user_message)
    previous_messages.append({'role':'assistant', 'content': rsp })
    return process_response(rsp, prompt_id)
