# Local LLM - Quantized for less RAM

## References

https://huggingface.co/TheBloke/CodeLlama-13B-GGUF

https://www.youtube.com/watch?v=rZz5AORu8zE

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

- warning: this downloads the `Code Llama 13B Quantized` LLM which is about 10 GB (multiple files).

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

## Results

### Model: codellama-13b.Q5_K_M.gguf

- REPETITION_PENALTY = 1 (default)
- TEMPERATURE = 0.5

Prompt :

```
create a DOT graph to decide a mortgage loan.
if credit score is greater than 700 then check years employed. else reject.
if years employed is greater than 3 then approve. else reject.

digraph G {
```

Response:

```
    rankdir=LR;
    node [shape=record];
    credit_score [label="{credit score: 700}"];
    years_employed [label="{years employed: 5}"];
    credit_score -> years_employed [label="700 > 700"];
    years_employed -> approve [label="5 > 3"];
    years_employed -> reject [label="5 <= 3"];
    approve [label="approve"];
    reject [label="reject"];
}
```
