# ollama-server

```
virtualenv env -p python3
source env/bin/activate
pip install -r requirements.txt
```
Set the ollama LLM model to the 
ollama model you wish to use

```
# main.py
#********************************************************
# set ollama model
#********************************************************
LLM_MODEL = "llama3.1:8b"
#********************************************************
```

Then run the local server

```
./run_ollama_server.sh
```
