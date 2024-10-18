def init(key):
    
    import system_message

    try:
        system = system_message.load(key)
        chat_log = [ {'role':'system',
                    'content':system,},
      ]
        return(chat_log)
    except:
        return("Key not valid")




def receive(messages, model = "gpt-3.5-turbo", temperature=0):

    import openai
    import os
    from dotenv import load_dotenv

    load_dotenv()

    key = os.getenv('OPENAI_API_KEY')
    client = openai.OpenAI(api_key = key)

    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature,
    )
    response = response.choices[0].message.content
    thread = [messages,response]
    return response, thread

