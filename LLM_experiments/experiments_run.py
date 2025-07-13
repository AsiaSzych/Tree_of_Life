import os
import json
import uuid
import yaml
import argparse
import datetime
import time
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
               self.model = ChatAnthropic(model=model_name, temperature=self.temperature, verbose=self.verbose, max_tokens=self.max_tokens)
               print(f"Anthropic model initialized, max tokens {self.model.max_tokens}, temperature {self.model.temperature}")
           case "google":
                self.model = ChatGoogleGenerativeAI(model=model_name, temperature=self.temperature, verbose=self.verbose, max_output_tokens=self.max_tokens) 
                print(f"Google model initialized, max tokens {self.model.max_output_tokens}, temperature {self.model.temperature}")
           case "deepseek":
                self.model = ChatDeepSeek(model=model_name, temperature=self.temperature, verbose=self.verbose, max_tokens=self.max_tokens) 
                print(f"DeepSeekModel initialized, max tokens {self.model.max_tokens}, temperature {self.model.temperature}")
           case "openai":
               self.model = ChatOpenAI(model=model_name, temperature=self.temperature, verbose=self.verbose, max_tokens=self.max_tokens)  
               print(f"OpenAI model initialized, max tokens {self.model.max_tokens}, temperature {self.model.temperature}")

def read_prompts(path_to_file:str):
    logger.info(f"Reading prompts from file {path_to_file}")
    with open(path_to_file, "r") as f:
        prompt_data = yaml.safe_load(f)
    prompt_list=[]
    for task in prompt_data["tasks"]:
        prompt_list.append(task["text"])
    return prompt_list

def run_conversation_and_save(llm:Model, prompts:list,language:str, try_number:int,):
    
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
    output_dir = f"./{language}/results_{llm.model_name}/solution_try_{try_number}"
    os.makedirs(output_dir)
    output_file_path = os.path.join(output_dir, f"conversation_{llm.model_name}_{language}_try_{try_number}.md")
    time_start = datetime.datetime.now().strftime("%d/%m/%Y, %H:%M:%S")
    markdown_output = [f"# Conversational Code Generation - {llm.model_name} with {language}, {time_start}\n"]
    with open(output_file_path, "w", encoding="utf-8") as f:
        f.write("\n".join(markdown_output))

    logger.info("Executing prompts and collecting responses")
    for i, p in enumerate(prompts, start=1):
        markdown_output = []
        markdown_output.append(f"## Prompt {i}\n")
        markdown_output.append(f"**User:** {p}\n")
        with open(output_file_path, "a", encoding="utf-8") as f:
            f.write("\n".join(markdown_output))

        if llm.model_name=='claude-opus-4':
            time.sleep(60)

        result = chain_with_memory.invoke({"input": p},config={"configurable": {"session_id": str(uuid.uuid4())}})
        markdown_output = []
        if result.content != '':
            markdown_output.append(f"**LLM Response:**\n\n{result.content.strip()}\n")
        else:
            markdown_output.append(f"**LLM Response - content not available, saving full reasoning:**\n\n{result}\n")
        with open(output_file_path, "a", encoding="utf-8") as f:
            f.write("\n".join(markdown_output))
    logger.info("Prompt execution finished")

    time_end = datetime.datetime.now().strftime("%d/%m/%Y, %H:%M:%S")
    markdown_output = [f"# The end - {llm.model_name} with {language}, {time_end}\n"]
    with open(output_file_path, "a", encoding="utf-8") as f:
        f.write("\n".join(markdown_output))

    return True

if __name__=="__main__":
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('-l', '--language', help='Path to yaml file with prompts to execute.', required=True)
    parser.add_argument('-v', '--version', help='Version of the run.', required=True)
    args = parser.parse_args()
        
    logger.info("Initialize models")
    gpt = Model(short_name="gpt-4.1",model_name="gpt-4.1", provider="openai") #https://platform.openai.com/docs/models/gpt-4.1
    deepseek = Model(short_name="deepseek-chat",model_name="deepseek-chat", provider="deepseek") #https://api-docs.deepseek.com/
    claude = Model(short_name="claude-opus-4",model_name="claude-opus-4-20250514", provider="anthropic") #https://docs.anthropic.com/en/docs/about-claude/models/overview
    gemini = Model(short_name="gemini-2.5-pro", model_name="gemini-2.5-pro", provider="google") #https://ai.google.dev/gemini-api/docs/models

    prompts = read_prompts(f"./prompts_final_{args.language}.yaml")

    for llm in [gpt, claude, deepseek]:
        logger.info(f"Start flow for {llm.model_name}, try {args.version}")
        output = run_conversation_and_save(llm, prompts, args.language, args.version)