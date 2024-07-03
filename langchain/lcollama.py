import os
import time
import _pickle as pickle
from langchain_community.chat_models import ChatOllama
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

def pickle_write(filename, input_var, mode):
    """Function to save INPUT_VAR (dict) that is passed in to a FILENAME (string).
    If the file already exists, its content is overwritten. Returns INPUT_VAR"""
    with open(filename, mode) as save: #for MODE: w is overwrite, a is append, etc. Add b for binary pickles.
        save.write(pickle.dumps(input_var))
    return input_var #returns in case we want to reuse this somewhere

def pickle_read(filename):
    """Function to read FILENAME and return the stuff inside"""
    with open(filename, 'rb') as read:
        return pickle.load(read) #return contents with their correct type

def string_save(filename, input):
    """Function to save a string to a file.
    Takes in an INPUT (string), and overwrites to FILENAME (string)"""
    with open(filename, "w") as file:
        file.write(input)

def wait_modified(filename):
    """Function that looks at the time at which a FILENAME (string) was last edited.
    If that time changes, it means FILENAME was edited, and we return its new contents."""
    last_modified=os.path.getmtime(filename)
    while last_modified == os.path.getmtime(filename):
        time.sleep(2.0) #adjust as necessary as to not burn out your processor
    else:
        with open(filename, "r") as read:
            return read.read().rstrip() #rstrip removes the extra newline at the end

class NeuralCloud:
    """Neural Cloud class."""
    def __init__(self, name, model, system_prompt, memory={}):
        """Initialize the Neural Cloud. Needs:
        NAME: name of the AI, also used as the session_id for config (string)
        MODEL: name of the Ollama model (string)
        SYSTEM_PROMPT: system prompt for AI to follow (string)
        MEMORY: dictionary used to hold message history (dict)"""
        self.name = name
        self.model_llm = ChatOllama(model=model)
        self.system_prompt_string = system_prompt
        self.system_prompt = ChatPromptTemplate.from_messages([("system", system_prompt), MessagesPlaceholder(variable_name="messages")])
        self.memory = memory
        self.config = {"configurable": {"session_id": name}} #used with self.memory
        self.chain = self.system_prompt | self.model_llm #this chains the prompt and model objects together
        if not self.memory: #if memory was blank...
            self.memory[self.name] = ChatMessageHistory() #...create a new memory
            self.with_memory = RunnableWithMessageHistory(self.chain, lambda x: self.memory[x]) #basically, memory[config's session id], lambda returns message history

    def api_request(self, user_input, bridge_active=False):
        """Ask langchain to generate an AIMessage given a HumanMessage with input USER_INPUT."""
        print("User:", user_input)
        response = self.with_memory.invoke([HumanMessage(content=user_input)], config=self.config).content
        pickle_write(ncb, [self.memory, self.system_prompt_string], 'wb')
        print(f"{self.name}:", response)
        if bridge_active:
            string_save(ai_file, response) #The LLM API returns something, which writes to AI_FILE (4-5/7)
            string_save(user_file, "") #USER_FILE is blanked out. AI_FILE still has the content from the previous step (6/7)
            wait_modified(ai_file) #Your integration script does what it needs to do with AI_FILE. Then you blank out AI_FILE. (7/7)

def loop(doll, bridge_active=False):
    """Infinite loop to emulate conversations."""
    while True:
        if bridge_active:
            string_save(ai_file, "") #USER_FILE and AI_FILE are blanked out (1/7)
            string_save(user_file, "")
            user_input = wait_modified(user_file) #USER_FILE is written to (2/7)
        else:
            user_input = input("User: ")
        doll.api_request(user_input, bridge_active) #passes contents of USER_FILE to the LLM API (3/7)
    return

def start(model, bridge_active=False):
    """Start script."""
    if os.path.isfile(ncb): #make sure that the ncb is created
        print('> Neural Cloud backup file found. Loading contents...')
        ncb_content=pickle_read(ncb)
        memory=ncb_content[0] #memory set!
        ai_name=list(memory.keys())[0] #set ai_name
        system_prompt=ncb_content[1] #second item in list
        doll=NeuralCloud(ai_name, model, system_prompt) #initiate the NeuralCloud class with this info
        print(f'> Neural Cloud for {ai_name} loaded succesfully.')
    else: #if ncb not found, make and populate
        print('> Neural Cloud Backup not found. Creating...')
        ai_name=input('> What name would you like to assign to the AI? (This is what you will call the AI)\n> ')
        system_prompt=input('> Provide a system prompt for the AI. (This is akin to the personality or baseline traits for the AI)\n> ')
        doll=NeuralCloud(ai_name, model, system_prompt) #initiate the NeuralCloud class with this info
        #now save the system prompt
        pickle_write(ncb, [{}, system_prompt], 'wb') #now save this new ncb. its a list with entry 0 being memory dict, and entry 1 the system_prompt string
        print(f'> Neural Cloud for {ai_name} created.')
        doll.api_request(f"Hello, {ai_name}.") #make sure we actually get something to write to ncb
    if bridge_active:
        print(f'> Bridge service is active. AI responses will be written to {ai_file}, and User inputs should be placed in {user_file}.')
    loop(doll, bridge_active) #ignition!

ncb, ai_file, user_file = "neuralcloud_backup.ncb", 'neuralcloud_ai.file', 'neuralcloud_user.file' #you MUST define these variables
start("qwen:0.5b", bridge_active=True)