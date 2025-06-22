from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from threading import Thread
import re
import traceback
import pprint
import json
import io  
import asyncio
from fastapi.responses import StreamingResponse

import ollama
from ollama import chat
import time


#********************************************************
# set ollama model
#********************************************************
LLM_MODEL = ""
#********************************************************

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)


class AgentQuestionModel(BaseModel):
    question: str


if LLM_MODEL == "":
    raise Exception("ollama model needs to be set")

@app.post("/ask")
async def ask_question(question: AgentQuestionModel):
    prompt = question.question
    messages = json.loads(prompt)["messages"]
    print("ASK")
    text_response = ""
   
    streamer = chat(
        model=LLM_MODEL,
        messages=messages,
        stream=True
    )

    for chunk in streamer:
        text = chunk['message']['content'] 
        text = text.replace("<|eot_id|>", "")
        text_response += text
        print(text, end='', flush=True)

    return {"question": question.question,  "answer": text_response}





@app.post("/ask-stream")
async def ask_question_stream(question: AgentQuestionModel):
    print("ASK STREAM")

    prompt = question.question
    messages = json.loads(prompt)["messages"]
    
    streamer = chat(
        model=LLM_MODEL,
        messages=messages,
        stream=True
    )
    
    # Define a generator function for the streaming response
    async def serve_data():
        # while True:
        try:
            for chunk in streamer:
                text = chunk['message']['content']
                print(text, end='', flush=True)
                yield text
                # await asyncio.sleep(0.00000001)
                await asyncio.sleep(0)

            yield "<|eot_id|>"

        except Exception as e:
            print(f"Error during streaming: {e}")
            yield f"Error: {str(e)}"

    # Return a single streaming response that contains all the generated chunks
    return StreamingResponse(
        serve_data(),
        media_type='text/event-stream'
    )
