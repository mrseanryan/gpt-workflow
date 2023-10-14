pip install -r requirements.txt

REM The non-CUDA ctransformers?
REM no-binary to force a local build, in case some dependency issues
REM pip install "ctransformers>=0.2.24" --no-binary ctransformers --force

REM Try ctransformers[cuda] instead of ctransformers and then bump up the GPU_LAYERS
pip uninstall ctransformers
pip install "ctransformers[cuda]>=0.2.24" --no-binary ctransformers --force
