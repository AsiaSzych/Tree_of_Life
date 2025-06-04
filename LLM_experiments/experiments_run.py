import os
import json
import uuid
import yaml
from loguru import logger
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder, HumanMessagePromptTemplate
from langchain_openai import ChatOpenAI
from langchain_deepseek import ChatDeepSeek
from langchain_anthropic import ChatAnthropic
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.runnables.history import RunnableWithMessageHistory


logger.info("Set API keys as environment variables")
with open("./api_keys.json", 'r') as f:
    api_keys = json.loads(f.read())

for key in api_keys.keys():
    os.environ[key] = api_keys[key]

class Model:
    model_name: str
    model: ChatOpenAI|ChatDeepSeek|ChatAnthropic|ChatGoogleGenerativeAI

    def __init__(self, short_name, model_name, provider):
       self.model_name = short_name
       self.temperature = 0.2
       self.verbose = False
       self.max_tokens = 4096
       match provider:
           case "anthropic":
               self.model = ChatAnthropic(model=model_name, temperature=self.temperature, verbose=self.verbose)
           case "google":
                self.model = ChatGoogleGenerativeAI(model=model_name, temperature=self.temperature, verbose=self.verbose) 
           case "deepseek":
                self.model = ChatDeepSeek(model=model_name, temperature=self.temperature, verbose=self.verbose) 
           case "openai":
               self.model = ChatOpenAI(model=model_name, temperature=self.temperature, verbose=self.verbose) 

def read_prompts(path_to_file:str):
    logger.info(f"Reading prompts from file {path_to_file}")
    with open(path_to_file, "r") as f:
        prompt_data = yaml.safe_load(f)
    prompt_list=[]
    for task in prompt_data["tasks"]:
        prompt_list.append(task["text"])
    return prompt_list

def run_conversation(llm:Model, prompts:list):
    
    logger.info(f"Setting up LLMChain for conversatiom with model {llm.model_name}")

    chat_prompt = ChatPromptTemplate.from_messages([
        MessagesPlaceholder(variable_name="history"),
        HumanMessagePromptTemplate.from_template("{input}")
    ])

    chain = chat_prompt | llm.model #pipe style, replaces LLMChain()
    
    logger.info("Setting up memory to keep context")
    message_history = InMemoryChatMessageHistory()
    chain_with_memory = RunnableWithMessageHistory(
        chain,
        lambda session_id: message_history,
        input_messages_key="input",
        history_messages_key="history"
    )

    markdown_output = ["# Conversational Code Generation\n"]

    logger.info("Executing prompts and collecting responses")
    for i, p in enumerate(prompts, start=1):
        result = chain_with_memory.invoke({"input": p},config={"configurable": {"session_id": str(uuid.uuid4())}})
        markdown_output.append(f"## Prompt {i}\n")
        markdown_output.append(f"**User:** {p}\n")
        markdown_output.append(f"**LLM Response:**\n\n{result.content.strip()}\n")
    logger.info("Prompt execution finished")

    return markdown_output

def save_results(llm:Model, language:str, try_number:int, content:list):
    file_path = f"./results/conversation_{llm.model_name}_{language}_try_{try_number}.md"
    logger.info(f"Saving results to file {file_path}")
    with open(file_path, "w", encoding="utf-8") as f:
        f.write("\n".join(content))

    logger.info("Results saved")

if __name__=="__main__":
    logger.info("Initialize models")
    gpt = Model(short_name="gpt-4.1",model_name="gpt-4.1", provider="openai") #https://platform.openai.com/docs/models/gpt-4.1
    deepseek = Model(short_name="deepseek-reasoner",model_name="deepseek-reasoner", provider="deepseek") #https://api-docs.deepseek.com/
    claude = Model(short_name="claude-opus-4",model_name="claude-opus-4-20250514", provider="anthropic") #https://docs.anthropic.com/en/docs/about-claude/models/overview
    # gemini = Model(short_name="gemini-2.5-flash", model_name="gemini-2.5-flash-preview-05-20", provider="google") #https://ai.google.dev/gemini-api/docs/models

    prompts = read_prompts("./prompts_final.yaml")

    for llm in [claude]:
        logger.info(f"Start flow for {llm.model_name}, try 1")
        output = run_conversation(llm, prompts)
        save_results(llm, "python", 1, output)