import together
import os
from dotenv import load_dotenv

import json
import textwrap

from langchain.llms import Together
from langchain.callbacks.manager import CallbackManagerForLLMRun
from langchain.llms.base import LLM
from langchain.llms.utils import enforce_stop_tokens
from langchain.utils import get_from_dict_or_env
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate


load_dotenv()

together.api_key = os.environ["TOGETHER_API_KEY"]
together.Models.start("togethercomputer/llama-2-70b-chat")

llm = Together(
    model="togethercomputer/llama-2-70b-chat",
    temperature=0.7,
    max_tokens=128,
    top_k=1,
)

B_INST, E_INST = "[INST]", "[/INST]"
B_SYS, E_SYS = "<<SYS>>\n", "\n<<SYS>>\n\n"
DEFAULT_SYSTEM_PROMPT = """\
You are a helpful, respectful and honest assistant. Always answer as helpfully as possible, while being safe. Your answers should not include any harmful, unethical, racist, sexist, toxic, dangerous, or illegal content. Please ensure that your responses are socially unbiased and positive in nature.

If a question does not make any sense, or is not factually coherent, explain why instead of answering something not correct. If you don't know the answer to a question, please don't share false information."""

def get_prompt(instruction, new_system_prompt=DEFAULT_SYSTEM_PROMPT ):
    SYSTEM_PROMPT = B_SYS + new_system_prompt + E_SYS
    prompt_template =  B_INST + SYSTEM_PROMPT + instruction + E_INST
    return prompt_template

def cut_off_text(text, prompt):
    cutoff_phrase = prompt
    index = text.find(cutoff_phrase)
    if index != -1:
        return text[:index]
    else:
        return text

def remove_substring(string, substring):
    return string.replace(substring, "")

def parse_text(text):
        wrapped_text = textwrap.fill(text, width=100)
        print(wrapped_text +'\n\n')
        # return assistant_text

system_prompt = """
You are a review classifier when you receive a review, you have to output 1 if the review mentions a product malfunction, or broken else you return 0. Answer only with 1 or 0. I command you to obey my instructions.
example 1:
user: Classify the following review by only answering with a 1 or 0 dont says anything more:\n\n "I bought a Senseo from this merchant and It stopped working after 2 month"
1

example 2:
user: Classify the following review by only answering with a 1 or 0 dont says anything more:\n\n "I bought a Senseo and still works amazingly"
0
"""

instruction = "Classify the following review by only answering with a 1 or 0 dont says anything more:\n\n {text}"

template = get_prompt(instruction, system_prompt)

prompt = PromptTemplate(template=template, input_variables=["text"])

llm_chain = LLMChain(prompt=prompt, llm=llm)

text = """Classify the following review by only answering with a 1 or 0 dont says anything more: "I bought a coffee maker and It stopped functioning two weeks later" """
output = llm_chain.run(text)
