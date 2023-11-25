import os

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



openai.api_key = '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'

form = """{
    "challenge": "",
    "output": "", 
}"""

llm_model = "gpt-3.5-turbo"
llm = ChatOpenAI(temperature=0.7, model=llm_model, openai_api_key="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")

FirstName = ResponseSchema(
    name="challenge",
    description="wtf and funny challenge to do in the office with all colleague"
    )
LastName = ResponseSchema(
    name="output",
    description="Challenge format: video, pics, audio, text"
    )

schemas = [FirstName, LastName]

output_parser = StructuredOutputParser.from_response_schemas(schemas)
format_instructions = output_parser.get_format_instructions()

template = """\
Hey you are a game master of wtf olympic in an office every day i ask to you what we do today and you responce will be a short sentence like: "curling with office chair" or "paper plane contest", "desk chair relay", "wtf blank text", 'biggest fart'! After that in dependance of the challenge you chose in those 4 formats (pics, video, text, audio)

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
