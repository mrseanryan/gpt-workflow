# ref = https://huggingface.co/codellama/CodeLlama-13b-hf
#
# The base 7B or 13B version in the Hugging Face Transformers format.
# This model is designed for general code synthesis and understanding

import sys
from transformers import AutoTokenizer
import transformers
import torch

if len(sys.argv) != 2:
    print(f"USAGE: {sys.argv[0]} <7B|13B>")

model_size = sys.argv[1]

model = None
if model_size == "13B":
    model = "codellama/CodeLlama-13b-hf"
elif model_size == "7B":
    model = "codellama/CodeLlama-7b-hf"
else:
    raise("Model size must be 7B or 13B")

tokenizer = AutoTokenizer.from_pretrained(model)
pipeline = transformers.pipeline(
    "text-generation",
    model=model,
    # needs GPU ? - torch_dtype=torch.float16,
    torch_dtype=torch.float32, # ok for CPU?
    device_map="auto",
)

prompt = """
create a DOT graph to decide a mortgage loan. if credit score is greater than 700 then check years employed. else reject.

if years employed is greater than 3 then approve.
else reject.

name the DOT nodes with a prefix decision_ or end_ or other_.

In the labels, refer to the available properties: applicant.credit_score, applicant.years_employed, applicant.other

DOT:
"""

print(prompt)

sequences = pipeline(
    prompt,
    #'import socket\n\ndef ping_exponential_backoff(host: str):',
    do_sample=True,
    top_k=10,
    temperature=0.1,
    top_p=0.95,
    num_return_sequences=1,
    eos_token_id=tokenizer.eos_token_id,
    max_length=200,
)
for seq in sequences:
    print(f"Result: {seq['generated_text']}")
