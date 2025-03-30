import os
from dotenv import load_dotenv
from groq import Groq

def chat_reply(question:str, helping_data:str = '') -> str:
    """Takes question and returns chatbots reply. also takes weather data for help.

    Args:
        response (dict): weather data for helping AI understand weather.
        question (str): user question.

    Returns:
        str: AI reply in string format.
    """
    
    #loading api key from .env file.
    load_dotenv()
    api_key=os.getenv('GROQ_API_KEY')
    
    
    #initializes groq clint and sends request to the llama 3 model.
    client = Groq(api_key=api_key)
    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content":helping_data #adds helping data and context for AI.
                },
                {
                    "role": "user",
                    "content": question,#user question.
                }
            ],
            model="llama3-70b-8192",#model name(change model by changing name all names listed here: https://console.groq.com/docs/rate-limits)
            
            #warning: make sure model allows large numbers of calls such as llama models.
        )

        return chat_completion.choices[0].message.content # returns answer from ai in string format.
    
    except Exception as e:
        print(f"Error in chat response: {e}") 
        return "Uh-oh! Something went wrong. Please try again later."
