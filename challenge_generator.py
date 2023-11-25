import together
import os
import logging
from typing import Any, Dict, List, Mapping, Optional

from pydantic import Extra, Field, root_validator

from langchain.callbacks.manager import CallbackManagerForLLMRun
from langchain.llms.base import LLM
from langchain.llms.utils import enforce_stop_tokens
from langchain.utils import get_from_dict_or_env
os.environ["TOGETHER_API_KEY"] = "api_key"

class TogetherLLM(LLM):
    model: str = "togethercomputer/llama-2-70b-chat"
    together_api_key : str = os.environ["TOGETHER_API_KEY"]
    temperature : float = 0.7
    max_tokens : int = 512

    class Config:
        extra = Extra.forbid

    @root_validator()
    def validate_environement(cls, values :Dict) -> Dict:
        api_key = get_from_dict_or_env( values, "together_api_key", "TOGETHER_API_KEY")
        values["together_api_key"] = api_key
        return values
    @poperty
    def _llm_type(self) -> str:
        """The _llm type"""
        return "together"
    
    def _call(self, prompts : str, **kwargs : Any) -> str:
        together.api_key = self.together_api_key
        output = together.Complete.create(prompt, model = self.model, max_tokens = self.max_tokens, temperature=self.temperature)
        text = output['output']['choices'][0]['text']
        return text


together.api_key = "9894800278097398cd3c35ead8d37d5e2d8405a99c472a13c4932db807f50448"
models = together.Models.list()

together.Models.start("togethercomputer/llama-2-70b-chat")

test_llm = TogetherLLM(model = "togethercomputer/llama-2-70b-chat", temperature=0.8, max_tokens=512)
type(test_llm), test_llm.model, test_llm.temperature
test_llm("What are the olympics? ")
