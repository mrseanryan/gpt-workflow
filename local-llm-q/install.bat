pip install -r requirements.txt

REM no-binary to force a local build, in case some dependency issues
pip install ctransformers>=0.2.24 --no-binary ctransformers --force

REM FAIL - try ctransformers[cuda] instead of ctransformers and then bump up the GPU_LAYERS
REM pip uninstall ctransformers
REM pip install ctransformers[cuda]==0.2.24 --no-binary ctransformers --force
