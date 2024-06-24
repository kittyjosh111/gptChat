# Hacking, or one way to implement an integration

This is the logic behind the Ren'Py integration. I include this as a reminder for how ```erma.py``` behaves in bridge mode. You may use this logic in your scripts, or create your own more efficient algorithms.

---

```erma.py``` comes with a "bridge" mode, which becomes active when you run the start function with ```bridge_active=True``` as an argument. In this mode, you will not be able to interact with ```erma.py``` through the console, but rather through the auxillary files it creates. By default, these files will be ```neuralcloud_user.file``` for user inputs, and ```neuralcloud_ai.file``` for the LLM's outputs. ```summarize``` is created when the model is in the middle of summarizing.

For ease, I will use the internal variable names to refer to the auxillary files now. USER_FILE corresponds to ```neuralcloud_user.file```, and AI_FILE corresponds to ```neuralcloud_ai.file```.

When we first run ```erma.py```, both auxillary neuralcloud* files are blanked out, meaning they don't have any content. ```erma.py``` then assumes the first turn always belongs to the user, so it will wait for a user to write input to USER_FILE. Once that happens, USER_FILE is no longer empty and ```erma.py``` triggers an API request to your API model, giving them the contents of USER_FILE. When the API responds and returns back its output, ```erma.py``` writes said output to AI_FILE and then blanks out USER_FILE. For people who've looked at the code, I want to clarify that the blanking of USER_FILE happens after take_turns is called with the USER arg. It is in the first few lines of the USER's turn where USER_FILE is blanked out. So what you should see now is that USER_FILE still exists but is empty, while AI_FILE now has the API output written to it. This is how a normal exchange works.

Thus what do we learn? One important takeaway is that **USER_FILE is always empty when ```erma.py``` is currently waiting for someone to write something to USER_FILE. In other words, USER_FILE is empty when it is the USER's turn in the dialogue exchange**.

Great. What about AI_FILE? You might be tempted to say that a good check for whether it is the LLM's turn is to check whether AI_FILE has content. You'd be half right.

Unfortunately, ```erma.py``` has no clue whether you or your integration has finished dealing with the contents of AI_FILE. Thus, it doesn't make sense to have ```erma.py``` blank out the AI_FILE itself. What this means is that **the integration script must manually blank out AI_FILE when it is done reading the content**. Only then can you use the above check.

What does this mean so far? Let's put it in a step form:

1. USER_FILE and AI_FILE are blanked out

2. USER_FILE is written to

3. ```erma.py``` passes contents of USER_FILE to the LLM API

4. While the LLM is generating output, USER_FILE still has the user's input, and AI_FILE is still blank.

5. The LLM API returns something, which ```erma.py``` writes to AI_FILE

6. USER_FILE is blanked out. AI_FILE still has the content from the previous step

7. Your integration script does what it needs to do with AI_FILE. Then you **blank out AI_FILE**. What this results in is that...

8. Return to Step 1.

Thus, we have an infinite loop of user turn, ai turn, user turn, etc. Neato.

The wrench in the works occurs when the LLM enters its summarizer feature. Now we must deal with the ```summarize``` file.

When ```erma.py``` receives a function call to execute the summarizer feature, there IS A SMALL DELAY before ```summarize``` gets created. I do not know how long it takes, but it varies from milliseconds to a few seconds. When ```summarize``` is removed, that means the LLM has finished compressing the neural cloud.

Then how do we know when to catch ```summarize``` in the act? Well an easy way is when our previous checks for USER_FILE and AI_FILE are not met, in other words, the else case. To put it into perspective, refer back to step 4 of the above list. When USER_FILE is populated and AI_FILE is not, that means we either just finished writing to USER_FILE, or are waiting for the LLM to produce some output. This is also the situation if the summarizer functions in ```erma.py``` are working.

To explain more, the summarizer function is called either when the neuralcloud_backup exceeds a certain length, or is manually triggered by the user. These occur on the **user's turn**, or basically step 4 from the list.

When this happens, we can check whether ```summarize``` is created when we don't pass either check of USER_FILE or AI_FILE. In essence, the list now becomes:

1. USER_FILE and AI_FILE are blanked out

2. USER_FILE is written to (the integration script recognizes that USER_FILE is empty, and awaits user input)

3. ```erma.py``` passes contents of USER_FILE to the LLM API

4. ```erma.py``` knows how to interpret user requests to summarize. If USER_FILE has this, then the summarizer function is run and ```summarize``` is created. Once the summarizer finishes, ```summarize``` is deleted and it now becomes the user turn + USER_FILE is blanked out. In essence, you return to Step 1 because AI_FILE was never touched. If the summarizer function was not run, move to step 5.

5. While the LLM is generating output, USER_FILE still has the user's input, and AI_FILE is still blank.

6. The LLM API returns something, which ```erma.py``` writes to AI_FILE. (The integration script should recognize that AI_FILE is populated and proceed with whatever it needs to do, see step 8-9)

7. If the length of the neural cloud memory is too large, the summarizer function automatically triggers here. ```summarize``` is created. Once the summarizer finishes, ```summarize``` is deleted and USER_FILE is blanked out.

8. USER_FILE is blanked out. (This might be blanking a blank file, depending on previous step.) AI_FILE still has the content from before

9. Your integration script finishes what it needs to do with AI_FILE. Then you **blank out AI_FILE**. What this results in is that...

10. Return to Step 1.

In both steps where ```summarize``` appears, the integration script should recognize its presence and block user input. For example, in Ren'Py this would be spamming a warning message instead of giving the user input options.

This is the logic behind the Ren'Py integration script, and to an extent, the Discord one too.

Again, there's probably better ways to do this. I listed out the order of file operations on the auxillary files so you may see what happens when and act accordingly.