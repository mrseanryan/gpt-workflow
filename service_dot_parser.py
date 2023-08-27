import os
import pydot

import config
import util_file

DOT_GRAPH_START = "digraph G"
DOT_SECTION_DELIMITER = "```"

def generate_output_file_path(prompt_id, extension):
    return os.path.join(config.PATH_TO_PNG_OUTDIR, f"dot_graph_{prompt_id}.{extension}")

def generate_png_from_dot(dot_string, prompt_id):
    graphs = pydot.graph_from_dot_data(dot_string)
    path_to_png = generate_output_file_path(prompt_id, "png")
    print(f"Writing png to '{path_to_png}'")
    graphs[0].write_png(path_to_png)

def write_dot_to_file(dot_string, prompt_id):
    path_to_dot = generate_output_file_path(prompt_id, "dot")
    print(f"Writing dot to '{path_to_dot}'")
    util_file.write_text_to_file(dot_string, path_to_dot)

def is_dot_response(rsp):
    return DOT_GRAPH_START in rsp

def parse_dot_and_return_human(rsp, prompt_id):
    parts = rsp.split(DOT_GRAPH_START)
    human_output = parts[0].replace(DOT_SECTION_DELIMITER, "").strip()
    dot_string = DOT_GRAPH_START + parts[1]
    if DOT_SECTION_DELIMITER in dot_string:
        parts_after_dot = dot_string.split(DOT_SECTION_DELIMITER)
        dot_string = parts_after_dot[0]
        human_output += config.END_LINE + config.END_LINE.join(parts_after_dot[1:])
    print(f"  == BEGIN DOT ==")
    print(dot_string)
    print(f"  == END DOT ==")
    write_dot_to_file(dot_string, prompt_id)
    generate_png_from_dot(dot_string, prompt_id)

    return human_output
