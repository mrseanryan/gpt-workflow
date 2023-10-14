HF_PROJECT = "TheBloke/CodeLlama-13B-GGUF"

#this one works
MODEL_FILE__CODELLAMA_13B__Q3_K_M = "codellama-13b.q3_K_M.gguf"
MODEL_FILE__CODELLAMA_13B__Q3_K_M__MAX_TOKENS = 512 # max

MODEL_FILE__CODELLAMA_13_B__Q5_K_M = "codellama-13b.Q5_K_M.gguf"
MODEL_FILE__CODELLAMA_13B__Q5_K_M__MAX_TOKENS = 512 # max

#ACTIVE_MODEL_FILE = MODEL_FILE__CODELLAMA_13B__Q3_K_M
ACTIVE_MODEL_FILE = MODEL_FILE__CODELLAMA_13_B__Q5_K_M
MAX_NEW_TOKENS = MODEL_FILE__CODELLAMA_13B__Q5_K_M__MAX_TOKENS #4096, 1096

MODEL_TYPE = "llama"

GPU_LAYERS = 31 # 0 means 'no GPU' - if GPU try 50 or less - then probably need ctransformers[cuda] instead of ctransformers
#
# If too high - can actually be slower! - see https://www.reddit.com/r/LocalLLaMA/comments/14kt3hz/nvidia_user_make_sure_you_dont_offload_too_many/
# - depends on graphics card + the model
#
# Times for 24GB [only 8GB dedicated which seems to be the limit!] NVIDIA card with model MODEL_FILE__CODELLAMA_13B__Q3_K_M:
# - note in Task manager, the Shared GPU memory should stay low, else is slower.
# 0 = CPU only = 1m 34s
# 50, 45, 44, 43, 42 was too high for that card and model
# 41 = best time - 49.76s
# 40 = 50s+
# 37 = 53s
# 30 = 1m 38s
# 25 = 1m 7s
# 20 = 1m 22s
# 10 = 1m 58s
#
# model MODEL_FILE__CODELLAMA_13_B__Q5_K_M
# GPU layers, DOT prompt, quality good!
# 31 (max this h/w) = 21s ! (once)
# 28 = 20m 17s (!)

# getting GPU to work was tricky - ran this on command line:
# pip install "ctransformers[cuda]>=0.2.24"

REPETITION_PENALTY = 1 # 1.13 - range is 1 (no penalty, default) to 'infinity'

# TEMPERATURE = 0.5
TEMPERATURE = 0.5 # range is normally 0 (consistent) to 1 (more 'creative')
