Some scripts to mimic a chat function using OpenAI's GPT3. Note that you will need an OpenAI API to run this.

This script will create two files: ```neuralcloud.ncb``` and ```log.log```. The ncb file is what serves as the memory for the model, and basically logs the prompt, model output, and user input altogether. The log file only logs the model's outputs. To reset the model "personality", remove the ncb file. It's up to you whether to remove the log or not.

First use pip to install the ```requirements.txt```, then you can edit the values in the script to your liking.

Values you can change include temperature, model, prompt, etc. Think about the options you can find on the OpenAI Playground. Those values are here too. Refer to comments within the script for more information:

```
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
```

Then you can put your API key into the top of the script, where ```openai.api_key = ""``` is. Run the script with ```python3 py.py```. To stop, just kill the script with ^C.

Let's show an example of the script in action. This uses default values and the prompt ```The following is a conversation between a human and an AI name Turing. Turing is a helpful, friendly, and energetic AI who cares about her friends.```:

```
(venv) [user@x1yoga gptChat]$ python3 py.py 
Turing: Hi there! It's so nice to meet you. How can I help you today?
[Enter your input:] Hello. Can you remember something for me, Turing?
Turing: Absolutely! What would you like me to remember?
[Enter your input:] Please remember the phrase: "I bring misfortune".
Turing: Got it! I will remember the phrase "I bring misfortune". Is there anything else you would like me to remember?
[Enter your input:] Nope, goodbye!
Turing: Alright, goodbye! It was nice talking to you.
[Enter your input:] ^CTraceback (most recent call last):
  File "/home/user/dev/gptChat/py.py", line 107, in <module>
    main()
  File "/home/user/dev/gptChat/py.py", line 100, in main
    userInput = input("[Enter your input:] ")
                ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
KeyboardInterrupt

(venv) [user@x1yoga gptChat]$ 
(venv) [user@x1yoga gptChat]$ 
(venv) [user@x1yoga gptChat]$ python3 py.py 

[Enter your input:] Hello Turing, can you recall what I asked you to remember last time?
Turing: Of course! You asked me to remember the phrase "I bring misfortune". Is there anything else I can help you with?
[Enter your input:] Thank you, good day!
Turing: You're welcome! Have a great day!
[Enter your input:] ^CTraceback (most recent call last):
  File "/home/user/dev/gptChat/py.py", line 107, in <module>
    main()
  File "/home/user/dev/gptChat/py.py", line 100, in main
    userInput = input("[Enter your input:] ")
                ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
KeyboardInterrupt

(venv) [user@x1yoga gptChat]$ 
```