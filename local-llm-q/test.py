from ctransformers import AutoModelForCausalLM

prompt = "AI is going to"
print(prompt)

# Set gpu_layers to the number of layers to offload to GPU. Set to 0 if no GPU acceleration is available on your system.
llm = AutoModelForCausalLM.from_pretrained(#"codellama-13b-instruct.Q4_K_M.gguf",
                                           "TheBloke/CodeLlama-13B-GGUF",
                                           #failed - model_file="codellama-13b.q4_K_M.gguf",
                                           model_file="codellama-13b.Q3_K_M.gguf",
                                           model_type="llama",
                                           gpu_layers=0,
                                           #max_new_tokens = 512
                                           #repetition_penalty=1.13,
                                           #temperature=0.1
                                           )

print(llm(prompt))
