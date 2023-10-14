from ctransformers import AutoModelForCausalLM

import config
import util_time

prompt = "AI is going to"
print(prompt)

start = util_time.start_timer()

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

time_elapsed = util_time.end_timer(start)
print(f"Time taken: {util_time.describe_elapsed_seconds(time_elapsed)}")
