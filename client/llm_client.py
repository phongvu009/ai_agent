import os 
from typing import Any

from openai import OpenAI
from dotenv import load_dotenv

from client.response import TextDelta, TokenUsage,StreamEvent

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
            text_delta=text_delta,
            finish_reason=response.choices[0].finish_reason,
            usage=usage,

        ))
        


        

    
