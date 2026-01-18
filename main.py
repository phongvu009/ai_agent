import click
from openai import OpenAI
#calling to openrouter 
client = OpenAI(
    api_key="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",
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

    #agent response
    response = completion.choices[0].message.content

    print(response)



if __name__ == "__main__":
    main()
