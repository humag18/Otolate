import os
import random

from dotenv import load_dotenv

import json
import textwrap

from langchain.callbacks.manager import CallbackManagerForLLMRun
from langchain.llms.base import LLM
from langchain.llms.utils import enforce_stop_tokens
from langchain.utils import get_from_dict_or_env
from langchain.prompts import PromptTemplate

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

load_dotenv()

openai.api_key = os.environ["OPENAI_API_KEY"]

cred = credentials.Certificate("key.json")
firebase_admin.initialize_app(cred, {"databaseURL": "https://otolate-bcc65-default-rtdb.europe-west1.firebasedatabase.app/"})

form = """{
    "challenge": "",
    "output": "", 
}"""

llm_model = "gpt-3.5-turbo"
llm = ChatOpenAI(temperature=0.7, model=llm_model)

FirstName = ResponseSchema(
    name="challenge",
    description="Describe the challenge"
    )
LastName = ResponseSchema(
    name="output",
    description="video, pics, audio, text"
    )

schemas = [FirstName, LastName]

output_parser = StructuredOutputParser.from_response_schemas(schemas)
format_instructions = output_parser.get_format_instructions()

coin = random.randint(0,5)

print(coin)

template = """\
You are a crazy organiser of fun challenges inside the office. 
You allways find new fun and crazy new challenges easy to do around the office.\
Find new challenges easy todo in front of a computer camera. The challenge shouldn't take more than 1 min to relise.

Here are some examples for the challenges Find other on the same register:  
    -Write an unexpeted ending: It's raining cats and dogs...
    -Say merry christmas the best possible way. 
    -Try to imitate the bullet time from Matrix
    -Pretend your desk is a battlefield of incoming "bullets."
    -do the spiderman pose. 
    -sing all I want for chirstmas is you.
    -Reenact Forrest Gump's iconic running scene.

Do not ask: 
    -to write poems or texts. 
    -to write about an image or a caption.
    -to write dialogs
    

In the output you only have to say the desired format: 
    -text if you want the user to write a very short text
    -video if the user has to make a video

Format Ouput with the following keys:
challenge
output

Here is the following form: {form}

To choose what king of challenges you are going to flip a coin if it is 2,3,4,5 you ask for a text challenge 
If 0,1 ask for a video.

coin value: {coin}
"""

prompt = ChatPromptTemplate.from_template(template=template)

messages = prompt.format_messages(form= form, coin=coin, format_instructions=format_instructions)

response = llm(messages)

print(response.content)

res_json = json.loads(response.content)

# envoi à la db 
ref_chall = db.reference("/challenges")

chall_data = {
    "id": 6,
    "content": res_json["challenge"],
    "output": res_json["output"],
    "userOutput": [],
    "time_start": "2023-11-10T12:00:00+01:00",
    "time_stop": "2023-11-15T18:00:00+01:00",
}

ref_chall.child(str(chall_data["id"])).set(chall_data)

print("challenge créer avec succès!")

