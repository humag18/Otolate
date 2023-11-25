import together
import os 

"""os.environ["TOGETHTER_API_KEY"] = "9894800278097398cd3c35ead8d37d5e2d8405a99c472a13c4932db807f50448"""
together.api_key = "9894800278097398cd3c35ead8d37d5e2d8405a99c472a13c4932db807f50448"
models = together.Models.list()

together.Models.start("togethercomputer/llama-2-70b-chat")

test_llm = TogetherLLM(model = "togethercomputer/llama-2-70b-chat", temperature=0.8, max_tokens=512)
type(test_llm), test_llm.model, test_llm.temperature
test_llm("What are the olympics? ")
