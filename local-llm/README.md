# Local LLM README

Self-Hosting an LLM (`Code Llama 13B`), rather than using an Open-AI service.

ref - https://huggingface.co/codellama/CodeLlama-13b-hf

## Usage on Windows - Quick start (for Unix, use the .sh scripts)

Open a command prompt.

Create a Python environment, to be able to install dependencies without interfering with other Python projects on the same machine:

```
create_env.bat

where Python

env\Scripts\python -v
```
- output: should output the location and version of Python, at env\Scripts\python.exe.

Install and run the LLM.

- warning: this downloads the `Code Llama 13B` LLM which is about 26 GB (multiple files).

- the files are downloaded to this folder:

`dir %USERPROFILE%\.cache\huggingface\hub`

```
install.bat
go.bat
```

- output: prompt sent to LLM, and its response:

```
``` //`begin delimiter
digraph {
  rankdir=LR
  node [shape=box]
  start_ [label="start"]
  decision_credit_score [label="credit score > 700"]
  decision_years_employed [label="years employed > 3"]
  end_approved [label="approved"]
  end_rejected [label="
  ``` //` end delimiter
```

When done, deactivate the Python environment:

```
env\Scripts\deactivate

where python
```

- output: should output the usual location of Python

## Usage on Windows - DETAILED

Ref = https://github.com/mrseanryan/gpt-dm/issues/6

To use via transformers (locally)

- First, use a pip environment:

On Windows, Command prompt:
```
cd my-project
py -m venv env

env\Scripts\activate

where python

.\env\Scripts\python.exe

# when done:
env\Scripts\deactivate
```

ref = https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/#:~:text=To%20create%20a%20virtual%20environment,virtualenv%20in%20the%20below%20commands.&text=The%20second%20argument%20is%20the,project%20and%20call%20it%20env%20.

Then install special version of transformers for this model:

```
env\Scripts\pip install git+https://github.com/huggingface/transformers.git@main accelerate

env\Scripts\pip freeze > requirements.txt
```

Next time around, with the environment activated, can install via:

```
env\Scripts\pip install -r requirements.txt
```

Using the LLM:
```
# Use a pipeline as a high-level helper
from transformers import pipeline

pipe = pipeline("text-generation", model="codellama/CodeLlama-13b-Python-hf")

rsp = pipe("Generate the first 10 numbers of fibonacci in Python")
```

OR:

```
# Load model directly
from transformers import AutoTokenizer, AutoModelForCausalLM

tokenizer = AutoTokenizer.from_pretrained("codellama/CodeLlama-13b-Python-hf")
model = AutoModelForCausalLM.from_pretrained("codellama/CodeLlama-13b-Python-hf")
```
