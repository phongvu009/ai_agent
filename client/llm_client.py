import os 
from typing import Any
import json

from openai import OpenAI
from dotenv import load_dotenv

from client.response import TextDelta, TokenUsage,StreamEvent,StreamEventType

#load variables form .env
load_dotenv()

api_key = os.getenv("OPEN_ROUTER_API_KEY")
base_url = os.getenv("OPEN_ROUTER_BASE_URL")


class LLMClient:
    def __init__(self):
        self.client = None

    def get_client(self):
        if self.client is None:
        #create openai client to call to openrouter 
            self.client = OpenAI(
                api_key=api_key,
                base_url=base_url,
            )
        return self.client

    def chat_completion(self, messages: list[dict[str,Any]]):
        client = self.get_client()
        response = client.chat.completions.create(
            model="mistralai/devstral-2512:free",
            messages= messages,
        )

        # force json reponse to data contract 
        message = response.choices[0].message
        
        text_delta = None
        #wrap message content to TextDelta
        if message.content:
            text_delta = TextDelta(content=message.content)

        usage = None
        if response.usage:
            usage = TokenUsage(
                prompt_tokens=response.usage.prompt_tokens,
                completion_tokens=response.usage.completion_tokens,
                total_tokens=response.usage.total_tokens,
                cached_tokens=response.usage.prompt_tokens_details.cached_tokens

            )
        
        return(StreamEvent(
            type=StreamEventType.MESSAGE_COMPLETE,
            text_delta=text_delta,
            finish_reason=response.choices[0].finish_reason,
            usage=usage,

        ))
    
    def chat_chunk(self, messages: list[dict[str,Any]]):
        client = self.get_client()

        response = client.chat.completions.create(
            model="mistralai/devstral-2512:free",
            messages= messages,
            stream=True
        )

        #print(response)

        #keep track of finish_reason to know when stream end
        finish_reason = None
        #accumulate all chunk to get final one
        final_response = ""

        for chunk in response:
            #print(chunk)
            #print(json.dumps(chunk.model_dump(), indent=2))

            #each chunk has delta
            delta = chunk.choices[0].delta
            if delta.content:
                #print(delta.content)
                #To-do: force each data chunk event into StreamEvent
                final_response += delta.content
                print(StreamEvent(type=StreamEventType.TEXT_DELTA, text_delta=TextDelta(content=delta.content)))

            if chunk.choices[0].finish_reason:
                finish_reason = chunk.choices[0].finish_reason

        if final_response:
            print(f"final respone is:\n {final_response}")
        print(finish_reason)
        

        


        

    
