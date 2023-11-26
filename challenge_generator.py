import os
import random
from datetime import datetime, timedelta

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
    description="camera, text"
    )

schemas = [FirstName, LastName]

output_parser = StructuredOutputParser.from_response_schemas(schemas)
format_instructions = output_parser.get_format_instructions()

coin = random.randint(0,1)

print(coin)

template = """\
You are a crazy organiser of fun challenges inside the office. 
You allways find new fun and crazy new challenges easy to do around the office.\
Find new challenges easy todo in front of a computer camera. The challenge shouldn't take more than 1 minunte to relise.
Only 

Types examples of challenges with text: 
    -Explain the plot of The movie [COMPLETE] in the worst possible way. Example: Lord of The Rings, Terminator, ...
    -Write an alternative ending to [COMPLETE]. Example: Harry Potter, Game Of Thrones, ...
    -Write [COMPLETE] the best possible way. Example: a lazy excuse, presentation starter, ...
Types examples of challenges with videos:
    -Try to imitate [COMPLETE] example: Jack Nicolson, Donald Trump
    -Pretend your desk is [COMPLETE] example: battlefield of incoming bullets, uracain.
    -Do the [COMPLETE] pose. example: spiderman, superman, ...
    -Sing the liriks [COMPLETE]. example: All I want for christmas is you..
    -Reenact [COMPLETE] scene. example: Forrest Gump's iconic running

Choose only a challenge from these uption on top.

In the output you only have to say the desired format: 
    -text if you want the user to write a very short text
    -camera if the user has to make a video

Format Ouput with the following keys:
challenge
output

Here is the following form: {form}

To choose what king of challenges you are going to flip a coin if it is 0 you ask for a text challenge 
If 1 ask for a video.

coin value: {coin}
"""

prompt = ChatPromptTemplate.from_template(template=template)

messages = prompt.format_messages(form= form, coin=coin, format_instructions=format_instructions)

response = llm(messages)

print(response.content)

exit()
res_json = json.loads(response.content)

# envoi à la db 
ref_chall = db.reference("/challenges")

current_time = datetime.now()

# Ajoutez 20 minutes pour obtenir l'heure de fin
end_time = current_time + timedelta(seconds=30)

# Formattez les heures au format souhaité (par exemple, "HH:MM")
formatted_current_time = current_time.strftime("%H:%M")
formatted_end_time = end_time.strftime("%H:%M")

chall_data = {
    "id": 9,
    "content": res_json["challenge"],
    "output": res_json["output"],
    "userOutput": {2: "text"},
    "time_start": formatted_current_time,
    "time_stop": formatted_end_time,
}

ref_chall.child(str(chall_data["id"])).set(chall_data)

print("challenge créer avec succès!")

