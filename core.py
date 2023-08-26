import os
import pydot

import config
import service_chat

# DEV note: NOT using langchain.
# Tried using langchain but it's validation gets in the way of more complex prompts.
# And seems simpler to code direct, not via a complicated framework.

def create_command_messages(expert_commands):
    messages = []
    for command in expert_commands:
        messages.append({'role':'system', 'content': command.expert_template })

    return messages

DOT_GRAPH_START = "digraph G"

def process_response(rsp, prompt_id):
    if DOT_GRAPH_START not in rsp:
        return rsp
    parts = rsp.split(DOT_GRAPH_START)
    dot_string = DOT_GRAPH_START + parts[1]
    graphs = pydot.graph_from_dot_data(dot_string)
    path_to_png = os.path.join(config.PATH_TO_PNG_OUTDIR, f"dot_graph_{prompt_id}.png")
    print(f"Writing png to '{path_to_png}'")
    graphs[0].write_png(path_to_png)
    return dot_string

def execute_prompt(user_prompt, previous_messages, command_messages, prompt_id):
    # TODO: Route to the right 'expert' chain
    # Falls back to the default chain, which means sending the plain user prompt to the LLM

    user_message = {'role':'user', 'content': user_prompt }

    messages = command_messages + previous_messages + [user_message]

    rsp = service_chat.send_prompt_messages(messages)

    previous_messages.append(user_message)
    previous_messages.append({'role':'assistant', 'content': rsp })
    return process_response(rsp, prompt_id)
