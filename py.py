import openai
import os
openai.api_key = ""

#This is a simple script to converse with OpenAI's GPT models. It tries to keep persistence between chats by creating a file to store logs of the past conversations, here known as neuralcloud.ncb. 
#Model responses are also written to a log.log for further reference.

#################
### Variables ###

#model is the used OpenAI model. Check their website for different model names.
#https://platform.openai.com/docs/models/overview
model="text-davinci-003" 

#temperature controls the randomness of the response. The higher the temperature, the more random the response.
#its range is a number between 0 and 1. Decimals up to two places after the point are accepted.
temperature=0.6

#max_toxens is the maximum number of tokens to be generated. Each toxen is around 4 characters of text.
#its range is a whole number between 1 and 2048
max_tokens=150

#top_p controls diversity via nucleus sampling. A value of 0.5 means half of all likelihood-weighted options are considered.
#its range is a number between 0 and 1. Decimals up to two places after the point are accepted.
top_p=1

#frequency_penalty controls how much to penalize the likelihood to repeat the same phrases. The higher the number the more varied responses.
#its range is a number between 0 and 1. Decimals up to two places after the point are accepted.
frequency_penalty=0.5

#presence_penalty controls how much to penalize whether tokens have already appeared. Higher numbers mean that the model will talk about new topics.
#its range is a number between 0 and 1. Decimals up to two places after the point are accepted.
presence_penalty=0.6

#best_of controls how many times to generate a response to pick the best one from. OpenAI cautions you against setting this too high.
#its range is a whole number between 1 and 20
best_of=1

#the prompt is what the model will read for to create the response.
#Do not include the initial human prompt, just the description of what the model's pesonality should be like.
base_prompt="""The following is a conversation with an AI assistant. The assistant is helpful, creative, clever, and very friendly."""

#################
#################

#Initialize my custom memory file. Basically, a text file to log everything we've written and then reuse it as the prompt for future prompts. 
#First we check if there already exists a neural cloud file. If not, then we create the ncb file and wrtie the prompt to it.
#Its Like waking up their neural cloud for the first time. Otherwise, its just restoring their neural clouds.
ncb = './neuralcloud.ncb'
check = os.path.isfile(ncb)
if check:
  pass
else:
  append = open("neuralcloud.ncb", "a")
  append.write(base_prompt + "\nHuman: Hello.") #So the model's first words are a greeting to the user.
  append.close()

#################
### Functions ###

#Function for the api request so that I don't have to copy paste this over and over again.
def api_request(prompt):
  response = openai.Completion.create(
    model=model,
    prompt=prompt,
    temperature=temperature,
    max_tokens=max_tokens,
    top_p=top_p,
    frequency_penalty=frequency_penalty,
    presence_penalty=presence_penalty,
    best_of=best_of,
    stop=[" Human:", " AI:"]
  )
  api_request.response = response['choices'][0]['text'].strip()
  append = open("log.log", "a")
  append.write("\n" + response['choices'][0]['text'].strip()) #Write to log
  append.close()

#Function for the reading of the ncb.
def read_ncb():
  read = open("neuralcloud.ncb", "r")
  read_ncb.output = read.read()

#Function for the writing and appending to the ncb.
def append_ncb(append_input):
  append = open("neuralcloud.ncb", "a")
  append.write(append_input)
  append.close()

#Main function to regulate a question-answer type interaction between user and the model. First load in the past prompts, then move on.
def main():
  while True:
    read_ncb()
    api_request(read_ncb.output)
    append_ncb("\n" + api_request.response)
    print(api_request.response)

    #Then have the user interact with the model.
    #Function to ask user for input
    userInput = input("[Enter your input:] ")
    append_ncb("\nHuman: " + userInput)

#################
#################

if __name__ == "__main__":
    main()


