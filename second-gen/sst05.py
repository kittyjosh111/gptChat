# SST-05 (Second-Gen Doll)
#
# Yet another attempt at overcomplicating the ollama APIs.
# This script relies on embeddings to allow the model to determine which lines of dialogue are important
# for its memory. As a result, the summarizer and summer garden features on the first generation and erma
# scripts have been obsoleted.
#
# To start this script, refer to the last two lines invoking the agent_intialize function.
# Like erma, this supports a bridge mode, where responses are read and written to external files.
# However, due to usage of Tables (courtesy Data 8's datascience package), "neural cloud" management
# should be cleaner and easier to track than the previous two implementations.
# Additionally, a debug mode can be turned on to print the similarity table and memory for debugging purposes.

import os
import ollama
import numpy as np
import time
from numpy.linalg import norm
from datascience import *

######################
### Base functions ###
######################

def embed_generate(text, embed_model):
  """Function to generate an embedding for a TEXT"""
  """ EMBED_MODEL is meant to be defined as a Global Variable"""
  return client.embeddings(model=embed_model, prompt=text)

def generate_embed_table(table, embed_model, debug=False):
  """Embeddings generation. Takes in a TABLE and generates embeddings for each row, then
  appends those values in a new table with column Embeddings"""
  embeddings_array = make_array()
  for i in np.arange(table.num_rows):
    if debug:
      print(f"Generating embeds for row {i+1} out of {table.num_rows} rows of dialogue...")
    embedding = embed_generate(table.column("Contents").item(i), embed_model)
    embeddings_array = np.append(embeddings_array, embedding) #this saves us errors with nested arrays, but as a consequence, we cannot save embeddings to a file
  if debug:
    print("Embed table generated.")
  return table.with_columns("Embeddings", embeddings_array)

def update_embed_table(table, speaker, text, embed_model):
  """Function to update a TABLE with the TEXT appended to Contents col, and its embeddings
  appended to the Embeddings col"""
  table_speaker = table.column("Speaker")
  table_contents = table.column("Contents")
  table_embeddings = table.column("Embeddings")
  new_embedding = embed_generate(text, embed_model)
  table_speaker = np.append(table_speaker, speaker)
  table_contents = np.append(table_contents, text)
  table_embeddings = np.append(table_embeddings, new_embedding)
  return Table().with_columns("Speaker", table_speaker, "Contents", table_contents, "Embeddings", table_embeddings)

def save_table(table, filename):
  """Function to save a TABLE (preferably the embed table)'s Spaker and Contents columns. Due to
  issues with nested arrays and types, the embeds cannot be saved and thus won't be saved."""
  return table.select("Speaker", "Contents").to_csv(filename)

def load_table(filename):
  """Function to load a TABLE from a CSV. Automatically extracts only the 'Contents' col, or complains otherwise"""
  loaded = Table.read_table(filename)
  if "Contents" not in loaded.labels and "Speaker" not in loaded.labels:
    return "[ERROR] Required columns not found."
  else:
    return loaded.select("Speaker", "Contents")

def get_sims(target, library):
  """Returns an array of similarity scores given a TARGET string and a LIBRARY array
  of embeddings. The returned array is in order of items in LIBRARY and contains similarity scores"""
  #(x, y) = x . y / ||x|| * ||y|| (from gopenai's medium post, RAG for Everyone)
  similarity_scores = make_array()
  for i in library:
    x = target
    y = i["embedding"]
    cosine = np.dot(x,y)/(norm(x)*norm(y))
    similarity_scores = np.append(similarity_scores, cosine)
  return similarity_scores

def generate_sim_table(embed_table, prompt, embed_model):
  """Take in a EMBED_TABLE table with embeddings and a PROMPT string. Then calculates
  the embeddings of PROMPT and attaches a new column with similarity scores to the original table.
  Returns EMBED_TABLE sorted by similarities in the column Similarities."""
  prompt_embedding = embed_generate(prompt, embed_model)
  similarity_scores = get_sims(prompt_embedding["embedding"], embed_table.column("Embeddings"))
  return embed_table.with_columns("Similarities", similarity_scores).sort("Similarities", descending=True)

#######################
### Agent functions ###
#######################

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

def agent_creation():
  """Function to ask for agent specifics from the user. Returns that in a table"""
  ai_name=input('> What name would you like to assign to the AI? (This is what you will call the AI)\n> ')
  system_prompt=input('> Provide a system prompt for the AI. (This is akin to the personality or baseline traits for the AI)\n> ')
  speaker_array = make_array("Name", "System")
  content_array = make_array(f'{ai_name}', f'{system_prompt} Your name is {ai_name}.')
  print(f'> Neural Cloud for {ai_name} created.')
  return Table().with_columns("Speaker", speaker_array, "Contents", content_array)

def agent_wakeup(neuralcloud):
  """Function that checks the NEURALCLOUD (filename) to see if it exists.
  In this case, the neuralcloud will be a csv file that contains a datascience
  table, consisting of a "Speaker" and "Contents" column. Then, when the agent
  formulates a response, we can used table operations (take most resent K rows,
  or do a similarity classification) to present related information to the model.
  
  Returns a Table of 2 columns (no embeds)"""
  if os.path.isfile(neuralcloud):
    print("> Pre-existing neural cloud found. Loading...")
    loaded_table = load_table(neuralcloud)
    ai_name = loaded_table.where("Speaker", "Name").column("Contents").item(0)
    print(f"> Neural cloud for {ai_name} loaded.")
    return loaded_table
  else:
    print("> No existing neural cloud found. Creating...")
    new_table = agent_creation()
    save_table(new_table, neuralcloud) #and save it
    return new_table

def classify_speaker(tbl_take):
  """Takes in a row (table) of the embed_table, then outputs the dictionary
  that ollama requires in its messages list"""
  if "User" in tbl_take.column("Speaker").item(0):
    this_role = "user"
  elif "Assistant" in tbl_take.column("Speaker").item(0):
    this_role = "assistant"
  tbl_content = tbl_take.column("Contents").item(0)
  return {'role': this_role, 'content': f'{tbl_content}'}

def agent_load_memory(embed_table, user_input, n, k, embed_model, debug):
  filter_table = embed_table.take(np.arange(embed_table.num_rows - 1)) #ok, so first we remove the most recent line
  filter_table = filter_table.take(np.arange(2, filter_table.num_rows)) #then we remove the system prompt and name (first two lines)
  if filter_table.num_rows - n <= 0: #then we get the N most recent dialogues, if theres enough entries
    recent_range = np.arange(filter_table.num_rows) #otherwise just take everything
  else:
    recent_range = np.arange(filter_table.num_rows - n, filter_table.num_rows)
  recent_mem = filter_table.take(recent_range) #and remove them from the filtered
  filter_table = filter_table.take(np.arange(filter_table.num_rows)) #now run the similarity test on whats left
  sim_table = generate_sim_table(filter_table, user_input, embed_model) #and select the k most similar
  if sim_table.num_rows >= k: #similarly, check to see if we can even take K items
    k_nn_mem = sim_table.sort("Similarities", descending=True).take(np.arange(k))
  else:
    k_nn_mem = False
  system_prompted = embed_table.where("Speaker", "System").column(1).item(0) #we're going to stick K items into the system prompt
  named = embed_table.where("Speaker", "Name").column(1).item(0) #extract this
  memory_list = [] #now add k and n together
  if k_nn_mem:
    id_table = embed_table.with_columns("ID", np.arange(0, embed_table.num_rows)) # we need this for later
    k_nn_mem = k_nn_mem.join("Contents", id_table).sort("ID") #and sort by time
    for k_index in np.arange(k_nn_mem.num_rows):
      k_table_hold = k_nn_mem.take(k_index)
      first_add = k_table_hold.column("Contents").item(0) #its either a User or Assistant dialogue
      if first_add not in system_prompted:
        if "User" in k_table_hold.column("Speaker").item(0): #if we pulled a user dialogue, we get the AI's next dialouge
          next_dialogue = 1 #id of the ai response to user
        elif "Assistant" in k_table_hold.column("Speaker").item(0): #otherwise we pull the AI and the user dialogue before it
          next_dialogue = -1 #id of the user dialogue the AI was responding to
        second_id = id_table.where("Contents", first_add).column("ID").item(0) + next_dialogue
        second_add = id_table.where("ID", second_id).column("Contents").item(0)
        if next_dialogue == 1:
          system_prompted += f" User: {first_add}\n{named}: {second_add}"
        elif next_dialogue == -1:
          system_prompted += f" User: {second_add}\n{named}: {first_add}"
    memory_list.append({'role': "system", 'content': f'{system_prompted}'})
  for n_index in np.arange(recent_mem.num_rows):
    memory_list.append(classify_speaker(recent_mem.take(n_index)))
  if debug:
    print(f"\n---\n[DEBUG]: Similarities Table\n{sim_table}")
  return memory_list

def agent_get_embeds(table, embed_model, debug=False):
  """Function to generate the embed table for the passed in
  TABLE from load_memory or other"""
  return generate_embed_table(table, embed_model, debug)

def user_turn(table, filename, embed_model, bridge_active, user_file):
  """Function to add user input to the embed table, then save"""
  if bridge_active and user_file:
    user_input = wait_modified(user_file)
  else:
    user_input = input("User: ")
  new_table = update_embed_table(table, "User", user_input, embed_model)
  save_table(new_table, filename)
  return new_table, user_input

def agent_turn(table, messages_list, filename, model, embed_model, bridge_active, ai_file, user_file):
  """Function to add agent input to the embed table, then save"""
  output = client.chat(
    model=model,
    messages=messages_list
  )
  ai_input = output['message']['content']
  print(f"Assistant: {ai_input}")
  new_table = update_embed_table(table, "Assistant:", ai_input, embed_model)
  save_table(new_table, filename)
  if bridge_active and user_file and ai_file:
    string_save(ai_file, ai_input)
    string_save(user_file, "")
  return new_table

def user_agent_loop(table, filename, chat_model, n, k, embed_model, bridge_active, ai_file, user_file, debug):
  """Loops the user and agent turns while ensuring they receive and return
  the correct and necessary stuff"""
  system_prompt = table.where("Speaker", "System").column("Contents").item(0)
  while True:
    user_table, user_input = user_turn(table, filename, embed_model, bridge_active, user_file)
    #memory_list = [{'role': 'system', 'content': f'{system_prompt}'}] #system prompt...
    memory_list = []
    for each in agent_load_memory(user_table, user_input, n, k, embed_model, debug): #...memory...
      memory_list.append(each)
    memory_list.append({'role': 'user', 'content': f'{user_input}'}) #...and user inoput.
    if debug:
      print(f"\n[DEBUG]: Memory (length {len(memory_list)})\n{memory_list}\n---\n")
    table = agent_turn(user_table, memory_list, filename, chat_model, embed_model, bridge_active, ai_file, user_file) #resets the table

def agent_initialize(filename, chat_model, n, k, embed_model, bridge_active=False, ai_file=False, user_file=False, debug=False):
  """Starts the conversation. Requires FILENAME to save the neural cloud to,
  CHAT_MODEL for the llm model used to generate text, N, for the number of recent
  messages to load into memory, K for the number of most similar messages to load into
  memory (does not include the k recent messages), and EMBED_MODEL for generation of
  embeddings."""
  if bridge_active:
    print(f'> Bridge service is active. AI responses will be written to {ai_file}, and User inputs should be placed in {user_file}.')
    string_save(ai_file, "") #creates an empty file at AI_FILE
    string_save(user_file, "") #and the same for USER_FILE
  embed_table = agent_get_embeds(agent_wakeup(filename), embed_model, debug)
  user_agent_loop(embed_table, filename, chat_model, n, k, embed_model, bridge_active, ai_file, user_file, debug)

############
### Main ###
############

# The first required arg is the name of the neural cloud (filename to save the csv for later re-use)
# The second required arg is the name of the ollama model for TEXT GENERATION.
# The third required arg is for the number of recent lines of dialogue to add into memory.
# The fourth required arg is for the number of most related lines of dialogue EXCLUDING the above conditions to add into memory.
# The fifth required arg is for the name of the ollama model for EMBEDDING GENERATION.

#agent_initialize("neuralcloud", "mistral", 5, 3, "nomic-embed-text")
agent_initialize("neuralcloud", "llama3.2:1b", 10, 5, "nomic-embed-text", bridge_active=False, ai_file="ai_file", user_file="user_file", debug=True)
