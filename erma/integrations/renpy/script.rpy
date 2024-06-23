"""Just to be very clear, I really don't know how to use renpy.

The script of the game goes in this file."""

#Define the images to use. You SHOULD change these as needed.
image gpt neutral = "neutral.png"
image gpt positive = "positive.png"
image gpt negative = "negative.png"

#Python time. I am much more comfortable with this part.
init python: #renpy's way of initializing python stuff for later use

    import os
    import time

    #First define these vars. Change them as necessary. Refer to erma.py.
    ai_file = "neuralcloud_ai.file"
    user_file = "neuralcloud_user.file"

    pause_length = 2.0 #this controls the delay between each loop triggered.

    ######################################################################
    ## DO NOT MODIFY BELOW THIS LINE UNLESS YOU KNOW WHAT YOU ARE DOING ##
    ######################################################################

    #Then the functions. These are variations of the functions from erma.py.

    cwd = os.getcwd() #get the current executive dir so we can come back later

    def string_save(filename, input):
        """Function to save a string to a file.
        Takes in an INPUT (string), and overwrites to FILENAME (string)"""
        os.chdir('game') #I cant use slash syntax else it fails for whatever reason. IDK why.
        os.chdir('erma') #in pure python, we must navigate to the game folder first then to erma...
        open(filename, "w+").write(input)
        return os.chdir(cwd) #...then go back to the original folder

    def ren_read(filename):
        """Function to read the contents of a file.
        Takes in a FILENAME, and either returns its contents or FALSE if it 404s"""
        if renpy.loadable(filename, 'erma'):
            #return renpy.open_file(filename, directory='erma').read().decode("UTF-8")
            os.chdir('game') #same as in string_save. Its ugly but it works.
            os.chdir('erma')
            return_val=open(filename,"r").read()
            os.chdir(cwd)
            return return_val
        else:
            return False

    def wait_modified(filename):
        """Function that looks at the time at which a FILENAME (string) was last edited.
        If that time changes, it means FILENAME was edited, and we return its new contents."""
        os.chdir('game')
        os.chdir('erma')
        last_modified = os.path.getmtime(filename)
        while last_modified == os.path.getmtime(filename):
            renpy.pause(pause_length) #we call renpy's pause because the OS thinks the program is hanging when using time.sleep
        os.chdir(cwd)
        return ren_read(filename) #then read FILENAME content

    def splitter(text, split):
        """Function to split a large block of text TEXT
        into smaller chunks of length SPLIT. Then have renpy read out each chunk."""
        text_split = text.split()
        for each in range((len(text_split) // split) + 1):
            renpy.say("", ' '.join(text_split[:split])) #put it back together
            text_split = text_split[split:] #reassign the original list
        return

#Set renpy defaults. Mainly try disabling some UI elements.
default preferences.afm_enable = False
default preferences.desktop_rollback_side = "disable" #disable back button
default preferences.mobile_rollback_side = "disable" #disable back button

#The game starts here.
label start:
    scene bg #this loads in the bg.* file in the images directory
    show gpt neutral #base sentiment
    # These display lines of dialogue. - Ren'Py
    # Nuh uh! Infinite loops! - me

    python:
        # pre-run checklist. Must make sure that erma works properly and we start off with no AI output.
        while not renpy.loadable(ai_file, 'erma') and not renpy.loadable(user_file, 'erma'): #we need to make sure erma.py is in bridge mode
            renpy.say("NOTICE", "Files necessary for the bridging service from erma.py were not found. Please check that they were properly defined in scripts.rpy and that you have already set up erma.py.", interact=False)
            renpy.pause(pause_length)
        print("DEBUG: Prerun goal 1 completed. erma.py seems to be working!")
        string_save(ai_file, "") #we blank this out now. It doesn't affect erma, but makes the logic below much happier.
        print("DEBUG: Prerun goal 2 completed. AI_FILE has been cleared!")

        # main loop. Must make this infinite loop to repeat over and over.
        # if AI_FILE is populated, that means its time to display the AI response
        # else if the USER_FILE is blank, then we allow user to talk
        # else, something is happening and we wait for that to finish
        #   this means either the AI is making its response, or
        #   the summarizer feature is on and currently summarizing.
        while True:
            if ren_read(ai_file) != "": #if the AI_FILE is not blank, that means the AI has written to it: the AI response can be displayed
                print("DEBUG: Entered AI Turn...")
                if renpy.loadable('sentiment', 'erma'): #if sentiment.py is active, it created a sentiment file. Thus we look for sentiments
                    print("DEBUG: Waiting for sentiment analysis...")
                    sent_out = wait_modified('sentiment') #this one definitely is a function return
                    if 'positive' in sent_out:
                        renpy.show('positive') #self-explanatory
                    elif 'negative' in sent_out:
                        renpy.show('negative')
                    else: #neutral and other edge cases depending on the sentiment pipeline
                        renpy.show('neutral')
                    string_save('sentiment', "") #blank this out for next time
                    print("DEBUG: Sentiment analysis completed...")
                splitter(ren_read(ai_file), 36) #then we display whats here
                string_save(ai_file, "") #and blank it out to "reset" Ren'Py's view of AI_FILE
            elif ren_read(user_file) == "": #USER_FILE will be blanked by erma once AI output is written
                print("DEBUG: Entered USER turn...")
                user_input = renpy.input("Enter your input: ")
                string_save(user_file, user_input) #write renpy's input
            else:
                os.chdir('game') #We now should check if erma is summarizing. I cannot for whatever reason rely on renpy.loadable here.
                os.chdir('erma') #Thus, I rely on pure python to tell me whether the summarize file exists.
                while os.path.isfile('summarize'): #we can always rely on OS to check whether 'summarize' is inside the erma folder
                    print("DEBUG: Summarization active...")
                    renpy.say("NOTICE", "Neural Cloud compacting in progress. Please wait for it to finish.", interact=False) #if so, we send this out
                    renpy.pause(pause_length)
                else:
                    print("DEBUG: Ambiguous case. This usually means that the AI is busy creating summarizing or creating an output. Waiting before retrying...")
                os.chdir(cwd) #if not, then we reset the working python directory.
                renpy.pause(pause_length) #We wait a bit, also as to not burn out the CPUs.
    #This ends the game. We shouldn't ever reach here.
    return
