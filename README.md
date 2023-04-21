# gptChat

---

### Intro:

Simple scripts to mimic a chat function using OpenAI's api and other fun things. Note that you will need an OpenAI API to run this.

I don't know how to code. These are scripts that I've put together with hopefully enough comments that someone who doesn't know what they are doing (me in a few months), will be able to get the gist of what each piece of line does. It's been fun I guess working with the APIs and learning what a list is.

### General Setup:

I recommend running these scripts in a virtual environment. I'll assume you know how to set one up and activate it. If not, refer to the docs: https://docs.python.org/3/library/venv.html

For all scripts, first use pip to install the ```requirements.txt```, then you can open a script in a text editor to tweak the variable values to your liking. Usually, that ends up being the api key, as well as temperature, prompt, delimiters, etc.

Then you can put your API key into the top of the script, where ```openai.api_key = ""``` is. Run the script with cli or gui, whichever you know how. To stop, just kill the script with ^C.

Refer to the individual folder READMEs for more specific instructions.

### Types of scripts:

- ```cli```: The most basic scripts in that they were created first. These scripts allow the user to talk to the api through cli. It is the most simple without any fun features, so do note that they **do not limit how large the model's ncb is**.The longer it is, the **more expensive your api requests get**, and the model might not give back responses if it hits the maximum token limit. Use at your discretion. There is a script for the GPT3 api, and another that uses the gpt3.5 api. Refer to their readmes in the folder.

-```enhancedMemory```: The second generation of scripts and also the base for all the other later scripts. The scripts in this folder go a bit beyond, allowing the user to talk to the api but now does in fact **limit how large the model's ncb** is, trying to solve the problem with the scripts in ```cli```. Bascially, the ncb is compressed every certain number of dialog exchanges. Refer to the README in that folder for more information.

-```discord```: The scripts in this folder use the scripts from ```cli``` and ```enhancedMemory``` to create a discord bot. Information and setup instructions are in the README in that folder.

-```renpy```: This folder is a renpy project. It can be run from the renpy sdk. If you just want to run this, it is probably easier for you to instead go to the Releases page of this repo and just use those. Please please please read the instructions there. **run ```backend.py``` first before the renpy launcher```

### Logic behind my scripts:

The basic logic is that the scripts is that they query the api for a response based off os some sort of input. To retain "memory", these scripts will create two files to store previous conversations. This include a ```neuralcloud.ncb``` (ncb for **n**eural **c**loud **b**ackup) and ```log.log```. The ncb file is what serves as the memory for the model, and basically logs the prompt, model output, and user input altogether. The log file logs the model and user responses in a readeable format. **To reset the model "personality", remove the ncb file and the log file.** This applies to all models.

Again, refer to each individual README.md for more information.

Note the neural cloud backup files are generally not cross-compatible between the scripts.

---

Let's show an example of the cli scripts in action. This uses default values and the prompt ```The following is a conversation between a human and an AI name Turing. Turing is a helpful, friendly, and energetic AI who cares about her friends.```. The tracebacks and errors are due to me stopping the script with ^C.

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
---

Now, let's show an example of the renpy application:

![alt text](/screenshots/rpy1.png)

![alt text](/screenshots/rpy2.png)
