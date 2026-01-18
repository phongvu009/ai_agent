import json

from client.llm_client import LLMClient

import click

@click.command()
@click.argument("prompt", required=False)
def main(prompt: str|None = None):
    print(f'your pompt is: {prompt}')

    #create message
    messages = [{"role": "user", "content": prompt}]

    #get llm_client
    llm = LLMClient()

    event = llm.chat_completion(messages)

    print(event)
    
    #print(completion)
    #print(json.dumps(completion.model_dump(), indent=2))


    #agent response
    #response = completion.choices[0].message.content

    #print(response)




if __name__ == "__main__":
    main()
