# SST-05

### Intro
After taking the Data 8 class at UC Berkeley, I was introduced to their ```datascience``` package, which is essentially a modified wrapper for Pandas meant to introduce the basics of programming in data science at an introductory level. However, being a published package on pypi means that ```datascience``` is also relatively simple to use outside of the class jupyter notebooks and can be applied to various other python projects.

SST-05 is meant to improve on the ideals behind Erma while removing redundant steps, thus creating an overall more streamlined approach at maintaining / loading in "memory" for an llm chatbot. While tools like LangChain, chroma, or other vector databases would provide more robust memory systems, I would prefer to use as little dependencies as needed, if only as a programming exercise.

While Erma needed to run a summarization step after reaching the token limit (due to storing all past dialogues in the system prompt), SST-05 instead stores all dialogue in a ```datascience``` Table() and calculates embeddings for each line for use in cosine similarity comparisons. This way, SST-05 can choose the most recent N dialogue exchanges along with the K most relevant lines from the full conversation history in order to reduce the api token count and remove the need for a summarizer. Erma's "Summer Garden" concept is also obsoleted using this method, as there is no longer a need to tie certain lines of dialogue to keys, rather SST-05 can figure out what is relevant from embeddings and some math.

In a sense, this "algorithm" is somewhat similar to the Nearest Neighbors section from Data 8 (it's inspired by that lab), and you can see the Table() of embeddings sorted by similarity in SST-05's debug outputs.

Also to note, SST-05 is compatible with the integration scripts meant for Erma. You'll need to still set ```bridge_active```, ```ai_file```, and ```user_file``` to enter bridge mode and interface with the other scripts, but the order of operations from Erma's bridge mode also applies to SST-05. [Find the steps here.](https://github.com/kittyjosh111/gptChat/tree/main/erma/integrations)

### Setup
```sst05.py``` is the main script. You are advised to run it in a virtual environment. Remember to ```pip install -r requirements.txt```

Scroll down to the last few lines of the script to see how to run ```agent_initialize()```. But as a TLDR:

1) The first argument is a **required** STRING filename for which to save the CSV of dialogue to. SST-05 will use this while in operation, as well as to load in "memory" if you ever stop and restart the script.

2) The second argument is a **required** STRING name for the *text-generation* model you want to use. SST-05 is currently meant for usage with Ollama, but a programmer should be able to convert it to OpenAI calls or wherever your llm is hosted.

3) The third argument is a **required** INTEGER for the *K* number of most *recent* lines of dialogue to include in the llm's system memory.

3) The fourth argument is a **required** INTEGER for the *N* number of most *relevant* lines of dialogue to include in the llm's system memory.

5) The fifth argument is a **required** STRING name for the *embeddings* model you want to use. SST-05 is currently meant for usage with Ollama, but a programmer should be able to convert it to OpenAI calls or wherever your llm is hosted.

6) The sixth argument (bridge_active) is an optional BOOLEAN for whether to use bridge mode. If it is set to ```True```, the following two arguments must also be defined.

7) The seventh argument (ai_file) is an optional STRING filename for where the llm should write its responses to. This file should then be picked up by an integration script.

8) The eighth argument (user_file) is an optional STRING filename for where the llm should read for responses by the user. This file should be written to by an integration script.

9) The ninth argument (debug) is an optional BOOLEAN for whether to print out debug messages. These messages will show what the llm is doing, as well as the above K and N lines of past dialogue being passed into it.