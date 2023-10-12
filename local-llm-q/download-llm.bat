pip3 install huggingface-hub>=0.17.1

REM huggingface-cli download TheBloke/CodeLlama-13B-GGUF codellama-13b.q4_K_M.gguf --local-dir . --local-dir-use-symlinks False

huggingface-cli download TheBloke/CodeLlama-13B-GGUF --local-dir . --local-dir-use-symlinks False --include=*q4_K_M*gguf*
