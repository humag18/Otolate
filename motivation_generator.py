import os

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

openai.api_key = "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"

cred = credentials.Certificate("key.json")
firebase_admin.initialize_app(cred, {"databaseURL": "https://otolate-bcc65-default-rtdb.europe-west1.firebasedatabase.app/"})

userid = getUserIdByName("cameron")
user = getUserById(userid)
score = user['score']
previous = user['previous_score']

if score<previous:
    form = 0
else:
    form = 1 

llm_model = "gpt-3.5-turbo"
llm = ChatOpenAI(temperature=0.7, model=llm_model)
response = ResponseSchema(
    name="message",
    description="message depend of the score"
    )

schemas = [response]

output_parser = StructuredOutputParser.from_response_schemas(schemas)
format_instructions = output_parser.get_format_instructions()

template = """\

You are a funny game master in a society. You must find a message thats fits in one or two sentences depending on which score is higher or lower than the previously score.

-If the {form} = 0 find a little sentences tell to the worker he is vired be trash and don't forget to tell him he's a real looser

"""

prompt = ChatPromptTemplate.from_template(template=template)

messages = prompt.format_messages(form = form, format_instructions=format_instructions)

response = llm(messages)

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

print("Utilisateur ajouté avec succès!")
