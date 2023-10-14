from ctransformers import AutoModelForCausalLM

import config

prompt = "AI is going to"
print(prompt)

# Set gpu_layers to the number of layers to offload to GPU. Set to 0 if no GPU acceleration is available on your system.
llm = AutoModelForCausalLM.from_pretrained(
        config.HF_PROJECT,
        model_file=config.ACTIVE_MODEL_FILE,
        model_type=config.MODEL_TYPE,
        gpu_layers=config.GPU_LAYERS,
        max_new_tokens = config.MAX_NEW_TOKENS,
        repetition_penalty = config.REPETITION_PENALTY,
        temperature = config.TEMPERATURE
        )

print(llm(prompt))
