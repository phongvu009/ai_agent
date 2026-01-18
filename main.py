import os 
import json

import click
from openai import OpenAI
from dotenv import load_dotenv

from client.response import TextDelta, TokenUsage,StreamEvent

#load variables form .env
load_dotenv()

api_key = os.getenv("OPEN_ROUTER_API_KEY")
#calling to openrouter 
client = OpenAI(
    api_key=api_key,
    base_url="https://openrouter.ai/api/v1",
)

@click.command()
@click.argument("prompt", required=False)
def main(prompt: str|None = None):
    print(f'your pompt is: {prompt}')

    #create message
    messages = [{"role": "user", "content": prompt}]

    #use prompt send to server
    completion = client.chat.completions.create(
        model="mistralai/devstral-2512:free",
        messages= messages,
    )

    #print(completion)
    #print(json.dumps(completion.model_dump(), indent=2))


    #agent response
    #response = completion.choices[0].message.content

    #print(response)

    message = completion.choices[0].message

    text_delta = None
    #wrap message content to TextDelta
    if message.content:
        text_delta = TextDelta(content=message.content)

    usage = None
    if completion.usage:
        usage = TokenUsage(
            prompt_tokens=completion.usage.prompt_tokens,
            completion_tokens=completion.usage.completion_tokens,
            total_tokens=completion.usage.total_tokens,
            cached_tokens=completion.usage.prompt_tokens_details.cached_tokens

        )
    
    print(StreamEvent(
        text_delta=text_delta,
        finish_reason=completion.choices[0].finish_reason,
        usage=usage,

    ))
    



if __name__ == "__main__":
    main()
