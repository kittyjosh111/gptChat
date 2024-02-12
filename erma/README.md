# Q1A-MX (Erma)

*???: Have you really lost your memories, Erma?*

*Erma: Sorry...*

*???: Do you remember those ships that sailed the stormy seas for treasure?*

*???: In order to fix their position with the wind and waves tossing them, those huge ships would throw anchors out into the sea...*

*???: I left the first anchor point in your neural cloud—your name.*

*Erma: ...So as long as I say the name "Erma" in my neural cloud, I'll be able to unlock this area.*

*???: Correct.*

### Intro
Yet another chatbot implementation using OpenAI APIs. Alternatively, you can use LocalAI provided you have a strong enough computer and modify the ```erma.py``` script.

This chatbot was an attempt to write a script using better programming practices, such as using higher order functions instead of just a list of commands. It serves a similar purpose to the older scripts in this repository, but has a cleaner interface and should be more modular. It has a memory that stores user-api exchanges just like anything in the ```cli``` folder, and has the summarization features found in ```enhancedMemory```, but now introduces the concept of the 'Summer Garden'.

This concept of the summer garden was featured in the Longitudinal Strain event of the mobile game Girl's Frontline. In short, it is a way to store memories in a key, value relationship similar to your average dictionaries. Even if the chatbot's memory is altered due to resetting the log of past conversations (ex. summarizer function), it can still reinvoke memories that were tied to some key by having either the user or itself say that word.

For example, say the chatbot and user had a conversation about favorite foods that was saved to the Summer Garden under the key 'foodie'. Even if the conversation is led away from this topic and excluded from subsequent summarizations, as long as the chatbot or the user ever mentions the word 'foodie', then the summary of their conversation of favorite foods will be put back into the chatbot's memory. In a way, this works a bit like how humans might remember an event more specifically if reminded of certain attributes of said event.

### Setup
```erma.py``` is the main script. You are advised to run it in a virtual environment. Remember to ```pip install -r requirements.txt```

The script is currently meant to be run in an interactive mode. You can look at the last two lines for a hint on how to start up the chatbot.

First, you should copy ```.env.example``` to ```.env``` and edit ```OPENAI_API_KEY``` to include your OpenAI api key in the string. If you want to use the discord integration (more on that later), then fill out ```DISCORD_API_KEY``` as well.

Then, you must define ```ncb```, ```ai_file```, and ```user_file```. These should all be strings. The example given in the script is:

```ncb, ai_file, user_file = "neuralcloud_backup.ncb", 'neuralcloud_ai.file', 'neuralcloud_user.file'```

Failing to do this step means you will get an error when running the ```start()``` function. You can change the filenames in the strings to your liking.

 Then there are two ways to run ```erma.py```:

- ```bridge_active=True```. This tells ```erma.py``` to write AI responses to ```ai_file```, and look at ```user_file``` for user input. This means you cannot write to the chatbot in the console, and is meant to work as a "headless server" for integration with other services, such as ```discord-erma.py```. More on that later. 

	- To run with ```bridge_active``` activated, run ```start(model, bridge_active=True)``` in the console, where ```model``` is a string of the openai model (ex. 'gpt-3.5-turbo-0125')

- ```bridge_active=False```. This is the default value if you do not pass in a second argument to ```start()```. In this case, you write directly to the chatbot in the console, and ```ai_file```, ```user_file``` are not accessed at all.

	- To run with ```bridge_active``` not active, just run ```start(model)``` in the console, where ```model``` is a string of the openai model (ex. 'gpt-3.5-turbo-0125')

Again, refer to the last two lines of ```erma.py``` as an example way to start the script.

### Integrations

I am planning to write more integrations for ```erma.py```. You can too. Since you can run ```erma.py``` with ```bridge_active=True``` and have the chatbot wait for ```user_file``` to be populated, as well as write the API response to ```ai_file```, then you can write your own script to watch for changes to said files and send their contents off to some other service. I have an example ```discord-erma.py``` in this repository that does exactly that. Two functions from ```erma.py``` that could be useful for this are as follows:

```
def  wait_modified(filename):
	"""Function that looks at the time at which a FILENAME (string) was last edited.
	If that time changes, it means FILENAME was edited, and we return its new contents."""
	last_modified=os.path.getmtime(filename)
	while last_modified == os.path.getmtime(filename):
		time.sleep(2.0) #adjust as necessary as to not burn out your processor
	else:
		with  open(filename, "r") as read:
			return read.read().rstrip() #rstrip removes the extra newline at the end

def  string_save(filename, input):
	"""Function to save a string to a file.
	Takes in an INPUT (string), and overwrites to FILENAME (string)"""
	with  open(filename, "w") as  file:
		file.write(input)
```

You can import these from ```erma``` when writing your own script.

---

*The Summer Garden is closed.*

*No matter how many years pass...*

*No matter how time flies...*

*No matter what destiny has in store for me...*

*I will find this place again.*

*I will remember you all again.*
