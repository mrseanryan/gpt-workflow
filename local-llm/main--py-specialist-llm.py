# ref = https://huggingface.co/codellama/CodeLlama-13b-Python-hf
#
# The 13B *Python specialist* version in the Hugging Face Transformers format.
# This model is designed for general code synthesis and understanding.

# Use a pipeline as a high-level helper
from transformers import pipeline

pipe = pipeline("text-generation", model="codellama/CodeLlama-13b-Python-hf")

prompt = """
create a DOT graph to decide a mortgage loan. if credit score is greater than 700 then check years employed. else reject.

if years employed is greater than 3 then approve.
else reject.

name the DOT nodes with a prefix decision_ or end_ or other_.

In the labels, refer to the available properties: applicant.credit_score, applicant.years_employed, applicant.other

DOT:
"""

print(prompt)

response = pipe(prompt)

print(f"RSP>> ${response}")
