import gradio as gr
import time
from ctransformers import AutoModelForCausalLM

import config
import util_time

# ref https://huggingface.co/TheBloke/CodeLlama-13B-GGUF
# ref https://www.youtube.com/watch?v=rZz5AORu8zE
def load_llm():
    llm = AutoModelForCausalLM.from_pretrained(
        config.HF_PROJECT,
        model_file=config.ACTIVE_MODEL_FILE,
        model_type=config.MODEL_TYPE,
        gpu_layers=config.GPU_LAYERS,
        max_new_tokens = config.MAX_NEW_TOKENS,
        repetition_penalty = config.REPETITION_PENALTY,
        temperature = config.TEMPERATURE
        )
    return llm

print("Loading LLM...")
llm = load_llm()
print("[done]")

def print_config():
    print(f"GPU layers used: {config.GPU_LAYERS}")

print_config()

def llm_function(message, chat_history):
    global llm

    print(f">> {message}")
    start = util_time.start_timer()

    response = llm(message)
    print(response)

    time_elapsed = util_time.end_timer(start)
    print(f"Time taken: {util_time.describe_elapsed_seconds(time_elapsed)}")

    return response

title = "CodeLlama 13B GGUF (quantized) Demo"

examples = [
# best DOT prompt with the quantized model MODEL_FILE__CODELLAMA_13B__Q3_K_M
"""
create a DOT graph to decide a mortgage loan.
if credit score is greater than 700 then check years employed. else reject.
if years employed is greater than 3 then approve. else reject.

digraph G {
""",
# This prompt works better, just with the separate lines!
"""
create a DOT graph to decide a mortgage loan.
if credit score is greater than 700 then check years employed. else reject.
if years employed is greater than 3 then approve. else reject.

DOT:
""",
"""
create a DOT graph to decide a mortgage loan. if credit score is greater than 700 then check years employed. else reject.

DOT:
""",
"""
create a DOT graph to decide a mortgage loan. if credit score is greater than 700 then check years employed. else reject.

if years employed is greater than 3 then approve.
else reject.

name the DOT nodes with a prefix decision_ or end_ or other_.

In the labels, refer to the available properties: applicant.credit_score, applicant.years_employed, applicant.other

DOT:
""",
"""
What is the overal purpose of this DOT graph:

```
digraph {
    rankdir=LR;
    node [shape = box];
    start [label="start"];
    end [label="end"];
    start -> a [label="credit score > 700"];
    start -> b [label="credit score < 700"];
    a -> c [label="years employed > 3"];
    a -> d [label="years employed < 3"];
    b -> e [label="reject"];
    c -> f [label="approve"];
    d -> g [label="reject"];
    f -> end;
    g -> end;
}
```
""",
'Write a python code to connect with a SQL database and list down all the tables.',
'Write the python code to train a linear regression model using scikit learn.',
'Write the code to implement a binary tree implementation in C language.',
'What are the benefits of the python programming language?',
'AI is going to'
]

print(f"Hosting local LLM - you do NOT need to be logged in to HF")

gr.ChatInterface(
    fn = llm_function,
    title=title,
    examples = examples
    ).launch()
