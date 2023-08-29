import os
import sys

from workflow_trainingset_creator import EXPERT_COMMANDS
import core

if len(sys.argv) != 2:
    print(f"USAGE: {sys.argv[0]} <path to output file CSV to append to>")

csv_file_path = sys.argv[1]

command_messages = core.create_command_messages(EXPERT_COMMANDS)

# TODO xxx how to make more random? up temperature could risk the format...
user_prompt = "Create training data with 10 workflows"

previous_messages = []
print("---")
print(f">> {user_prompt}")
rsp = core.execute_prompt(user_prompt, previous_messages, command_messages)
print(rsp)

LLM_LINE_SEP = '\n'

def remove_header_line(rsp):
    lines = rsp.split(LLM_LINE_SEP)
    return LLM_LINE_SEP.join(lines[1:])

def write_or_append_out(rsp, csv_file_path):
    file_exists = os.path.isfile(csv_file_path)
    file_mode = 'a' if file_exists else 'w'
    file_mode_description = 'Appending' if file_exists else 'Writing'
    print(f"  {file_mode_description} to {csv_file_path}")
    if file_exists:
        rsp = remove_header_line(rsp)
    with open(csv_file_path, file_mode, encoding='utf-8') as f:
        f.write(rsp + LLM_LINE_SEP)

write_or_append_out(rsp, csv_file_path)
