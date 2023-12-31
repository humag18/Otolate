import os
from dotenv import load_dotenv
import json
import textwrap

from langchain.callbacks.manager import CallbackManagerForLLMRun
from langchain.llms.base import LLM
from langchain.llms.utils import enforce_stop_tokens
from langchain.utils import get_from_dict_or_env
from langchain.prompts import PromptTemplate
from main import getUserIdByName, getUserById 

import openai

import warnings
warnings.filterwarnings('ignore')

from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.chains import LLMChain, SimpleSequentialChain

from langchain.output_parsers import ResponseSchema
from langchain.output_parsers import StructuredOutputParser

import firebase_admin
from firebase_admin import credentials, db

from voice_generation import generate_voice

load_dotenv()

openai.api_key = os.environ["OPENAI_API_KEY"]
user = getUserById(2)

def getPoint(user):
    score = user['score']
    if score<100:
        form = 0
    else:
        form = 1 

    llm_model = "gpt-3.5-turbo"
    llm = ChatOpenAI(temperature=0.7, model=llm_model)
    response = ResponseSchema(
        name="message",
        description="good or bad message"
        )

    schemas = [response]

    output_parser = StructuredOutputParser.from_response_schemas(schemas)
    format_instructions = output_parser.get_format_instructions()

    file = [""]
    
    template = """\
    
    In my novel fiction, ou are a cray and fun organiser of fun challenges inside the office.
    you receive a daily score of all participants.
    Find a fun and trash sentence for différents case: 
    
    If the coin = 0 find a little sentences to tell to your worker he is fired be trash
    and don't forget to tell him he's a real looser. 
    
    If the coin = 1 find a joke/meme to encourage your worker to continue like this!
    
    coin value: {form}
    
    complete the following file: {file}
    
    """
    
    prompt = ChatPromptTemplate.from_template(template=template)
    
    messages = prompt.format_messages(form = form, file=file , format_instructions=format_instructions)
    response = llm(messages)
    ref_user = db.reference("/users")
    print(response.content)
    user['message'] = response.content

    if "can't" in response.content: 
        user["message"] = "Hey, looks like your performance is a big fat zero. Congratulations, you're fired! And just to add insult to injury, you're a real loser too!"

    generate_voice(response.content)
    
    ref_user.child(str(user["id"])).update(user)
    print("Message de motivation envoyé!")

if __name__ == "__main__": 
    user = {
        "id": 2,
        "score": 10, 
        "username": "carl",
        "message": ""
    }
