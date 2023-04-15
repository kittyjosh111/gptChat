# gptChat

---

### Intro:

Simple scripts to mimic a chat function using OpenAI's GPT3. Note that you will need an OpenAI API to run this.

I don't know how to code. These are scripts that I've put together with hopefully enough comments that someone who doesn't know what they are doing (me in a few months), will be able to get the gist of what each piece of line does. It's been fun I guess working with the APIs and learning what a list is.

There are two scripts provided. The ```gpt3.py``` uses the old GPT3 api for text completion, but is being used to act as a chatbot. It seems to be more expensive than the ```chatGPT.py```, which uses the gpt-3.5-turbo api, thus reducing costs. Use whichever you want.

### Setup:

I recommend running these scripts in a virtual environment. I'll assume you know how to set one up and activate it. If not, refer to the docs: https://docs.python.org/3/library/venv.html

First use pip to install the ```requirements.txt```, then you can open a script in a text editor to tweak the variable values to your liking.

For ```gpt3.py```, values you can change include temperature, model, prompt, etc. Think about the options you can find on the OpenAI Playground. Those values are here too. Refer to comments within the script for more information.

For ```chatGPT.py```, you can only change the prompt. Oh well.

Then you can put your API key into the top of the script, where ```openai.api_key = ""``` is. Run the script with cli or gui, whichever you know how. To stop, just kill the script with ^C.

### Logic behind my scripts:

Both scripts will create two files to store previous conversations.

For ```gpt3.py```, the script will create a ```neuralcloud.ncb``` (ncb for **n**eural **c**loud **b**ackup) and ```log.log```. The ncb file is what serves as the memory for the model, and basically logs the prompt, model output, and user input altogether. The log file only logs the model's outputs. To reset the model "personality", remove the ncb file. It's up to you whether to remove the log or not.

For ```chatGPT.py```, the script will create a ```neuralcloudv2.ncb``` and ```logv2.log```. The ncb file is what serves as the memory for the model, and basically logs the system, user, and assistant contents altogether in a list form. The log file only logs the model's outputs. To reset the model "personality", remove the ncb file. It's up to you whether to remove the log or not.

Note the neural cloud backup files are not cross-compatible between the two scripts.

**Also note that I currently do not limit how large the model's ncb is.The longer it is, the more expensive your api requests get, and the model might not give back responses if it hits the maximum token limit. Use at your discretion.**

**The script under enhancedMemory folder attempts to prolong the "life" a script can offer by summarizing past conversations into a brief sentence every 50 or so exhanges of dialogue. Refer there for more information.**

---

Let's show an example of the script in action. This uses default values and the prompt ```The following is a conversation between a human and an AI name Turing. Turing is a helpful, friendly, and energetic AI who cares about her friends.```. The tracebacks and errors are due to me stopping the script with ^C.

#### gpt3.py:
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
#### chatGPT.py:
```
(venv) [user@fedora  ]$ python3 chatGPT.py 
Hi there! How can I assist you today?
[Enter your input]: Hello, who are you?
I'm Turing, a friendly AI created to assist and communicate with people. How can I help you today?
[Enter your input]: Turing, can you remember the phrase "I bring misfortune"?
Yes, I have just remembered the phrase "I bring misfortune." Is there anything else you would like to ask me about that phrase?
[Enter your input]: nope, goodbye!
No problem, feel free to reach out to me in the future if you need any assistance. Goodbye!
[Enter your input]: ^CTraceback (most recent call last):
  File "/home/user/dev/ /chatGPT.py", line 75, in <module>
    main()
  File "/home/user/dev/ /chatGPT.py", line 70, in main
    user_input = input("[Enter your input]: ")
                 ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
KeyboardInterrupt

(venv) [user@fedora  ]$ ^C
(venv) [user@fedora  ]$ ^C
(venv) [user@fedora  ]$ python3 chatGPT.py 
No problem, feel free to reach out to me in the future if you need any assistance. Goodbye!
[Enter your input]: hey Turing, what was the phrase I asked you to remember?
You asked me to remember the phrase "I bring misfortune". Is there anything else you would like to know or ask me? I am happy to help.
[Enter your input]: great, good day!
You too! Have a great day! Feel free to reach out if you need any assistance in the future.
[Enter your input]: ^CTraceback (most recent call last):
  File "/home/user/dev/ /chatGPT.py", line 75, in <module>
    main()
  File "/home/user/dev/ /chatGPT.py", line 70, in main
    user_input = input("[Enter your input]: ")
                 ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
KeyboardInterrupt

(venv) [user@fedora  ]$ 
```
