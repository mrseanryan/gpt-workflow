from ctransformers import AutoModelForCausalLM

prompt = "AI is going to"
print(prompt)

# Set gpu_layers to the number of layers to offload to GPU. Set to 0 if no GPU acceleration is available on your system.
llm = AutoModelForCausalLM.from_pretrained("TheBloke/CodeLlama-13B-GGUF",
                                           model_file="codellama-13b.q4_K_M.gguf",
                                           model_type="llama",
                                           gpu_layers=0,
                                           max_new_tokens = 512
                                           )

print(llm(prompt))
