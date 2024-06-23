#!/usr/bin/python3
""" Codename Q1A-MX (Erma)
Another implementation of the OpenAI API to create a simple chatbot.
- This chatbot can be assigned a name, AI_NAME.
- Upon creation, a system prompt is assigned to SYSTEM_PROMPT.
- Messages later passed to the api request usually are assigned to CONVO, which is a *list of dicts*.
    The first dict is the SYSTEM_PROMPT.
    Later entries are dicts of KEY assistant/user and VALUE message.
    An example is shown below:
      {
        "role": "user",
        "content": "hey gpt, can you tell me a joke?"
      },
      {
        "role": "assistant",
        "content": "Why did the scarecrow win an award? Because he was outstanding in his field."
      },
- The Q1A-MX is a special type of doll due to their usage of the Summer Garden, which is a place 
  where memories can be tied to certain words, or keys. An example of this concept is illustrated below:
      "Manager: Congratulations on your fine taste. This is the latest model of second-generation Doll, the Q1A-MX."
      "Q1A-MX: Who's the Q1A-MX? Me?"
      "Q1A-MX: Who am I...?"
      Just then, her sleeve slides down and the sunlight illuminates her arm, revealing a band of densely-packed 
      encrypted text that looks like jewelry. She selects the simplest characters and searches for them in her neural cloud. 
      "Q1A-MX: Erma?"
      "Q1A-MX: Erma? ...I am Erma."
      (Girl's Frontline: Longitudinal Strain [Event 13-3])
- In this script's implementation, GARDEN is a list of dicts, the dict keys being garden KEYS, 
  and their VALUES being a summarized memory string.
- Memories thus can be restored to the chatbot by invoking a key in the garden (just mention it in user/AI input), 
  then the VALUE is loaded into the CONVO under the assistant tag.
- All of this is saved to a file, which is NCB. It is referred to FILENAME later on in the script.
- Special commands can be inputted by the user, which are stored in COMMAND_CHECK()
- Users and the chatbot are able to compact the neural cloud with SUMMARIZE(), saving request tokens.
- To use, first define NCB (main neuralcloud file, responsible for holding past conversations and the summer garden),
  AI_FILE, a file to write AI responses to,
  and USER_FILE, a file where users can write their inputs to.
- To start the conversation, START() is called with the model name (ex. 'gpt3.5-turbo') and the BRIDGE_ACTIVE.
  BRIDGE_ACTIVE is either True or False, and determines whether the AI_FILE and USER_FILE should be used.
- If BRIDGE_ACTIVE is True, then the script waits for USER_FILE to be written to. This could be done manually,
  or through another script. Once USER_FILE is modified, this script reads the contents and uses it as the user's input.
  This input is then sent to the API, which returns a response that is thus written to AI_FILE. This cycle then repeats."""

import os
import time
import json
import re
import shutil
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

def wait_modified(filename):
  """Function that looks at the time at which a FILENAME (string) was last edited.
  If that time changes, it means FILENAME was edited, and we return its new contents."""
  last_modified=os.path.getmtime(filename)
  while last_modified == os.path.getmtime(filename):
    time.sleep(2.0) #adjust as necessary as to not burn out your processor
  else:
    with open(filename, "r") as read:
      return read.read().rstrip() #rstrip removes the extra newline at the end

def string_save(filename, input):
  """Function to save a string to a file.
  Takes in an INPUT (string), and overwrites to FILENAME (string)"""
  with open(filename, "w") as file:
    file.write(input)

def dict_write(filename, dictionary, mode):
  """Function to save DICTIONARY (dict) that is passed in to a FILENAME (string).
  If the file already exists, its content is overwritten. Returns DICTIONARY"""
  with open(filename, mode) as save: #for MODE: w is overwrite, a is append, etc
     save.write(json.dumps(dictionary))
  return dictionary #returns in case we want to reuse this somewhere

def dict_read(filename):
  """Function to read FILENAME and return the dictionary inside"""
  with open(filename) as read:
    return json.load(read) #return contents with their correct type

def save(value, key, filename):
  """Function to read FILENAME and look for the key KEY (string).
  Then overwrites FILENAME with new value VALUE for key KEY."""
  existing=dict_read(filename) #get content of FILENAME
  existing[key]=value #reassign old value to new VALUE
  return dict_write(filename, existing, 'w') #just overwrite, it's easier

def bridge(ai_file, user_file):
  """Higher order function responsible for bridging this script to AI_FILE and USER_FILE.
  Contains an INNER function that takes in AI_TEXT or USER_TEXT, both of which are optional
  If AI_TEXT is passed in, it writes that to AI_FILE
  Then, if USER_TEXT is passed in, it writes that to USER_FILE
  If nothing was passed in, it just returns AI_FILE and USER_FILE, respectively"""
  def inner(ai_text=None, user_text=None):
    if ai_text: #first check if we should write to AI_FILE
      string_save(ai_file, ai_text)
    if user_text: #then check if we should write to USER_FILE (unused for now)
      string_save(user_file, user_text)
    if not ai_text and not user_text: #else return AI_FILE and USER_FILE
      return ai_file, user_file
  return inner

def api_request(model, convo):
  """Function to send an API request to OpenAI. Returns the API output string"""
  request=client.chat.completions.create(
    model=model,
    messages=convo #messages is supposed to be a list of dicts
  )
  return request.choices[0].message.content #return only the text of content

def check_garden(input, filename, convo):
  """Function that checks if a key from the summer garden
  has appeared in the INPUT passed in. Then loads in the garden value to CONVO.
  Note that INPUT should remain unedited, and only CONVO has been modified"""
  memory=dict_read(filename) #load in the entire memory to look through garden
  for each in list(memory['garden'].keys()): #iterate through the dict inside the garden
    if each in input and str(memory['garden'][each]) not in str(convo): #if the key is in the INPUT passed in, AND not already in convo
      convo.append({'role': 'assistant', 'content': memory['garden'][each] + f' These memories are tied to the word {each}.'}, ) #update convo
  save(convo, 'convo', filename) #now save the convo
  return input, convo #return the INPUT and the CONVO

def summarize(model, ai_name, filename, convo, bridge_active, key=None, local_summary=False):
  """Function to summarize and compact the current Neural Cloud
  This saves token counts in the long run. Takes in AI_NAME, FILENAME, CONVO,
  and KEY (the key in the summer garden dict in a list"""
  print('> Neural Cloud compacting in progress. Please wait.')
  shutil.copy(ncb, 'backup.ncb.bk') #make a copy of the neural cloud in case we need to restore it
  if bridge_active:
    string_save('summarize', "") #if bridge activated, create a temp summarize file to tell the integration to wait for user input
  messages='' #first create a blanked string
  memory=dict_read(filename) #load in the entire memory to do stuff to
  system_prompt=memory['convo'][0]['content'] #get the old system prompt
  for each in memory['convo'][1:]: #then get the old convo values
    role, content = each['role'], each['content']
    if role == 'assistant': #convert all 'assistant' to AI_NAME
      role=ai_name #reassign ROLE so that it prints the AI_NAME later
    messages=messages + f'\n{role}: {content}' #next, we have to prefix MESSAGES with SYSTEM_PROMPT and make this the new system prompt to api_turn
  if not local_summary: #default is to use the api for summarization
    request=api_request(model, [{'role': 'system', 'content': 'You are a helpful AI that summarizes conversations.'}, {'role': 'user', 'content': f'You are {ai_name}. As {ai_name}, summarize the following from your point of view in less than 3 sentences. {messages}'}])
  else: #but we can run that locally
    from transformers import pipeline, logging #we use hugginface transformers locally
    logging.set_verbosity_error() #surpress messages from pipeline
    print('> Running summarizer locally.')
    pipe = pipeline("summarization", model=local_summary)
    request=pipe(messages, do_sample=False)[0]['summary_text'] #extract text after running
  convo=[{'role': 'system', 'content': f'{system_prompt}'}, {'role': 'assistant', 'content': f'{request}'}, ] #create a new convo prompt with everything
  save(convo, 'convo', filename) #now save the new convo
  if key: #now we do operations to update the summer garden
    print(f'> Saving to Summer Garden under the key: {key}.')
    garden=memory['garden'] #get the summer garden list
    garden[key]=request #update the summer garden dict
    save(garden, 'garden', filename) #now save it to FILENAME
  print('> Neural Cloud compacting finished. You may continue the conversation.\n')
  if bridge_active: #summarize file only exists if BRIDGE_ACTIVE was in fact active
    os.remove('summarize') #remove the temp file
    string_save(user_file, "") #and blank out user_file for the next round
  return take_turns(model, convo, ai_name, filename, bridge_active, local_summary)('user') #let AI do the summarization in background. That means user gets control next

def take_turns(model, convo, ai_name, filename, bridge_active=None, local_summary=False):
  """Higher order function that does things"""
  def inner(who, convo=convo, bridge_active=bridge_active):
    """Figure out whether to have the user or the AI given some result
    WHO should be the string 'api' or 'user' """
    if len(dict_read(filename)['convo']) >= 32: #change to a suitable number
      summarize(model, ai_name, filename, convo, bridge_active, local_summary=local_summary) #then summarize without saving to garden
    if who == "api":
      response, convo = check_garden(api_request(model, convo), filename, convo) #run a request, but first CHECK_GARDEN
      convo.append({'role': 'assistant', 'content': f'{response}'}, ) #append the return of API_REQUEST
      save(convo, 'convo', filename) #save for future use, also saves
      print(f'{ai_name}: ' + response + '\n') #print to console
      if bridge_active:
        bridge(ai_file, user_file)(ai_text=response)
        string_save(user_file, "") #finally, blank out the user_file again.
      return take_turns(model, convo, ai_name, filename, bridge_active, local_summary)('user') #returns control back to user for their turn
    elif who == "user":
      def get_user_input(user_file=None):
        """Function to get input from a user or an external file"""
        if user_file:
          return wait_modified(user_file)
        else:
          return input('User: ')
      def command_check(user_input):
        """Function that first checks the USER_INPUT to see if it matches one of the supported commands."""
        def action(input_command):
          """Takes in an INPUT function to run, then restarts take_turns with the user arg"""
          input_command #run the input command first
          return take_turns(model, convo, ai_name, filename, bridge_active, local_summary)('user') #then rerun with user in control
        def matcher(regex1, regex2):
          """Function that tries to match USER_INPUT against a provided REGEX1.
          If there is a match, run the second REGEX2.
          Returns False if REGEX1 fails, otherwise returns output from REGEX2"""
          matches = re.findall(regex1, user_input)
          if matches: #there were any returns, then take first one only
            contents = re.findall(regex2, matches[0]) #get the contents inside the parantheses
            return contents[0]
          else:
            return False
        if user_input == 'exit()':
          action(exit('> Program Terminated.')) #exits entire program with message
        elif user_input == 'clear()':
          action(os.system('cls' if os.name == 'nt' else 'clear')) #clear the console
        elif user_input == 'help()':
          action(print('> These are the available commands. Type them without the quotation marks.\n>  "exit()": Exits the session.\n>  "clear()": Clears the console.\n>  "summarize()": Manually compact the neural cloud by summarizing past conversations. To save to the summer garden, put the key which you want to save to inside the parantheses. For example, summarize(key).\n'))
        elif (match_expression := matcher(r'summarize\([^)]*\)', r'\((.*?)\)')) is not False: #regex1 is summarize(*), regex2 is (*)
          action(summarize(model, ai_name, filename, convo, bridge_active, match_expression, local_summary)) #input passed in, write to the summer garden
        else:
          return user_input #if no commands found, just return user_input for further processing
      if bridge_active: #then see whether to look for a user_file or have the input
        toggle=user_file
      else:
        toggle=False
      user_input, convo = check_garden(command_check(get_user_input(toggle)), filename, convo)
      convo.append({'role': 'user', 'content': f'{user_input}'}, )
      #we don't save to file here. For example, if the person you're talking to doesnt hear you, they wont remember what you said
      return take_turns(model, convo, ai_name, filename, bridge_active, local_summary)('api') #now return control back to the AI for their turn
    else:
      return '> Error. take_turns not called with correct inner function argument.'
  return inner

def start(model, bridge_active=False, local_summary=False):
  """Function to start the script. Takes in the openai MODEL (string), BRIDGE_ACTIVE (bool), and LOCAL_SUMMARY (string).
  NCB, AI_FILE, and USER_FILE should be defined in the Global Frame first.
  It then attempts to read the NCB and load in the past conversations + garden.
  If BRIDGE_ACTIVE is not False, then it creates the files AI_FILE and USER_FILE.
  If LOCAL_SUMMARY is not False, it should be the string of the summarizer model from Hugging Face to use.
  Otherwise, the summarizer feature is given to the MODEL to do."""
  if os.path.isfile(ncb): #make sure that the ncb is created
    print('> Neural Cloud backup file found. Loading contents...')
    memory=dict_read(ncb) #memory set!
    ai_name=memory.get('ai_name') #set ai_name
    convo=memory.get('convo') #set convo
    print(f'> Neural Cloud for {ai_name} loaded succesfully.')
  else: #if ncb not found, make and populate
    print('> Neural Cloud Backup not found. Creating...')
    ai_name=input('> What name would you like to assign to the AI? (This is what you will call the AI)\n> ')
    system_prompt=input('> Provide a system prompt for the AI. (This is akin to the personality or baseline traits for the AI)\n> ')
    convo=[{'role': 'system', 'content': f'{system_prompt} Your name is {ai_name}.'}, ]
    memory={'ai_name': ai_name, 'convo': convo, 'garden': {}} #memory set!
    dict_write(ncb, memory, 'w') #w indicates overwrite the file
    print(f'> Neural Cloud for {ai_name} created.')
  #now, we attempt to create files for the bridge functionality. If they exist, we just overwrite with a blank
  if bridge_active:
    print(f'> Bridge service is active. AI responses will be written to {ai_file}, and User inputs should be placed in {user_file}.')
    string_save(ai_file, "") #creates an empty file at AI_FILE
    string_save(user_file, "") #and the same for USER_FILE
  #now we attempt to display the most recent user-ai interaction if applicable
  print('> Starting conversaton. Type "help()" without the quotations to see available commands.\n')
  if len(memory['convo']) >= 4: #system_prompt, summary, user, api makes 4 total items in the list. Only if we have this count can we give a sensible past convo
    print('User: ' + memory['convo'][-2]['content']) #user
    print(f'{ai_name}: ' + memory['convo'][-1]['content'] + '\n') #api
  return take_turns(model=model, convo=convo, ai_name=ai_name, filename=ncb, bridge_active=bridge_active, local_summary=local_summary)('user') #ignition, starts a loop of user, api, user, api, etc...

## Initiate the script. Modify as needed. ##
#ncb, ai_file, user_file = "neuralcloud_backup.ncb", 'neuralcloud_ai.file', 'neuralcloud_user.file' #you MUST define these variables
#start('gpt-3.5-turbo-0125', bridge_active=True) #bridge is active for bridging to discord-erma
#start('gpt-3.5-turbo-0125') #bridge is not active, and only prints to local console
#start('gpt-3.5-turbo-0125', local_summary="philschmid/flan-t5-base-samsum") #bridge is not active, and summarization is done locally using the speicifed model.
