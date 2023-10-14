pip install -r requirements.txt

REM no-binary to force a local build, in case some dependency issues
pip install ctransformers==0.2.24 --no-binary ctransformers --force

REM TODO -try ctransformers[cuda] instead of ctransformers and then bump up the GPU_LAYERS
