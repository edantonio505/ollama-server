# ollama-server


```
git clone https://github.com/edantonio505/ollama-server.git
cd ollama-server/
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



Create a new Bot Plugin in LLM Fastrack
and copy this to the code section
```
import json
from typing import Any, List, Mapping, Optional
import requests
from langchain.callbacks.manager import CallbackManagerForLLMRun
from langchain.llms.base import LLM
from typing import Dict


#****************************************************
# LLM HOST
#****************************************************
URL_HOST = "{HOST_TO_LOCAL_LLM}"
#****************************************************


config = {
    # if "fixable" is True, the plugin will allow you to fix the message response 
    # and whatever fields are specified in "fixable_fields"
    # with fixable fields, the user can only select from the values provided
    "fixable_fields": [
     	{"field": "default", "values": "anystring"}
    ],
  	# This contains the name of the field that ends the conversation
} 


# this block of code needs to go insdie the set llm 
# function
class RestApiPlugin(LLM):

    # ==============================
    # To change to your own REST API
    # This should be pointing to the colab later
    # ==============================
    # llm_host = 'http://www.ouichef.ai:5000'
    # llm_url = f'{llm_host}/api/bot' # or whatever your REST path is...

    llm_host = ""
    llm_url = f'{llm_host}/ask'
    system_prompt:str = None
    knowledgebase:str = None
    # ==============================

    def __init__(self, system_prompt: str, knowledgebase:str, HOST:str=None):
        super().__init__()
        self.system_prompt = system_prompt
        self.knowledgebase = knowledgebase

        if HOST is not None:
            self.llm_url = HOST
            self.llm_url = f'{self.llm_url}/ask'
            
    def set_llm_url(self, llm_url:str):
        self.llm_url = llm_url
      
      
    @property
    def _llm_type(self) -> str:
        return "Llama3.1 8B"

    def _call(
        self,
        prompt: str,
        stop: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
        **kwargs: Any,
    ) -> str:
        if stop is not None:
            raise ValueError("stop kwargs are not permitted.")
        prompt = self._transform_input(prompt)

        # ==============================
        # To change to your own REST API
        # ==============================
        headers = {
            'Content-Type': 'application/json',
        }

        data = {
            "question": prompt
        }

        r = requests.post(self.llm_url, headers=headers, data=json.dumps(data))
        # ==============================

        r.raise_for_status()
        return r.json()['answer'] # get the response from the API





    # This should have a function that will modify the propmt before 
    # sending it to the LLM
    # ==============================
    def _transform_input(self, prompt: str) -> str:    
        messages = [
            { "role": "system", "content": self.system_prompt},
            {"role": "context", "content": self.knowledgebase },
            {"role": "user", "content": prompt },
        ]
        prompt = json.dumps({"messages": messages })
        return prompt
    # ==============================





    @property
    def _identifying_params(self) -> Mapping[str, Any]:
        """Get the identifying parameters."""
        return {"llmUrl": self.llm_url}

      
      
def set_llm(context):
    # =============================================================
    # Change the URL_HOST to your own REST API
    # =============================================================
    URL_HOST = "http://127.0.0.1:5000"
    # =============================================================
    llm = RestApiPlugin("", context, URL_HOST)
    return llm
      
      


def transform_question(prompt):
    return prompt




def transform_answer(answer):
    return answer



# from bots.Plugins.RestApiPlugin import test_plugin; test_plugin();
def test_plugin():
    print("test")



if __name__ == "__main__":
    test_plugin()
```


If you need a starting template for your bot then click `Edit Bot` and the modify the temaplate prompt
```
System: Ere un asistente que responde a todo lo que el usuario requiere o pregunta.

Example
<example_context>
[EXAMPLE_CONTEXT]
</example_context>

Current conversation history:
<history>
[HISTORY]
</history>

User: {question}
Assistant:
```
