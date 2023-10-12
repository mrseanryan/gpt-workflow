pip install -r requirements.txt

# no-binary to force a local build, in case some dependency issues
pip install ctransformers==0.2.24 --no-binary ctransformers --force
