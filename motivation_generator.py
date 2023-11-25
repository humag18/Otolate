import os
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

load_dotenv()

openai.api_key = os.environ['OPENAI_API_KEY']

form = """{
    "challenge": "",
    "output": "", 
}"""

llm_model = "gpt-3.5-turbo"
llm = ChatOpenAI(temperature=0.7, model=llm_model)

FirstName = ResponseSchema(
    name="challenge",
    description="challenge fun a réaliser dans un bureau devant ou avec un ordinateur devant ses collègues."
    )
LastName = ResponseSchema(
    name="output",
    description="Format du challenge: vidéo, photo, audio, ..."
    )

schemas = [FirstName, LastName]

output_parser = StructuredOutputParser.from_response_schemas(schemas)
format_instructions = output_parser.get_format_instructions()

template = """\
Dans ton bureau de travail, tu as décidé de faire des challenges fun avec ton équipe\
Le principe est de réaliser un challenge fun et rapide à réalise devant ou avec son ordinateur\

Cela peut etre de prendre un photo, faire une vidéo à remplir ou complété un texte à trou\

Comme sortie il faut: 

challenge: une description nouveau challenge. Fait en sorte qu'elle soit très brève et facile à comprendre\

output: le format du challenge à réaliser. Choisit entre: photo, vidéo et texte.

Format l'output as JSON avec les clés suivantes:
challenge
output


Voici le formulaire à compléter {form}
"""

prompt = ChatPromptTemplate.from_template(template=template)

messages = prompt.format_messages(form=form, 
                                format_instructions=format_instructions)

response = llm(messages)

print(response.content)