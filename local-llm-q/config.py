HF_PROJECT = "TheBloke/CodeLlama-13B-GGUF"

#this one works
MODEL_FILE__CODELLAMA_13B__Q3_K_M = "codellama-13b.q3_K_M.gguf"
MODEL_FILE__CODELLAMA_13B__Q3_K_M__MAX_TOKENS = 512

MODEL_FILE__CODELLAMA_13_B__Q5_K_M = "codellama-13b.Q5_K_M.gguf"
MODEL_FILE__CODELLAMA_13B__Q5_K_M__MAX_TOKENS = 512 # try higher?

ACTIVE_MODEL_FILE = MODEL_FILE__CODELLAMA_13B__Q3_K_M
#ACTIVE_MODEL_FILE = MODEL_FILE__CODELLAMA_13_B__Q5_K_M
MAX_NEW_TOKENS = MODEL_FILE__CODELLAMA_13B__Q3_K_M__MAX_TOKENS #4096, 1096

MODEL_TYPE = "llama"

GPU_LAYERS = 0 # 0 means 'no GPU' - if GPU try 50 or less - then probably need ctransformers[cuda] instead of ctransformers

REPETITION_PENALTY = 1.13
TEMPERATURE = 0.5
