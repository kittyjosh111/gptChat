"""Just to be very clear, I really don't know how to use renpy.

The script of the game goes in this file.

** erma.py should be started first and configured BEFORE running this renpy project. **
** sentiment.py should be started first and configured BEFORE running this renpy project. **
** if sentiment.py is not run, you WILL NOT see different emotions on the images **

The first check is whether 'summarize' exists. If it does, we wait for it to go away.
 Then we check whether user_file has any contents. If it doesn't, we know it is the user's turn,
   and thus we have renpy ask for the user's input.
 Else, we know it is the AI's turn and they might be busy generating input.
   thus, we wait until ai_file is next modified (erma writes the AI output to ai_file), then have 
   renpy read and display the contents of ai_file. During this process, user_file should have been
   blanked out, thus we are ready for the next cycle.
 Additionally, we check for the 'sentiment' file to be filled before displaying ai output. If it is
 non-existent, we don't change the image shown through Ren'Py"""

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

    ######################################################################
    ## DO NOT MODIFY BELOW THIS LINE UNLESS YOU KNOW WHAT YOU ARE DOING ##
    ######################################################################

    #Then the functions. These are variations of the functions from erma.py.
    def string_read(filename):
        """Function to read a string from a file.
        Takes in an FILENAME (string) and returns contents"""
        return open(filename,"r").read()

    def string_save(filename, input):
        """Function to save a string to a file.
        Takes in an INPUT (string), and overwrites to FILENAME (string)"""
        return open(filename, "w+").write(input)

    def exists(filename): #I realize that renpy has a builtin feature similar to this, but I couldn't get it to work.
        """Function that checks if the FILENAME is detected by Ren'Py.
        It is just a try except wrapper that returns either the FILENAME path or False."""
        try:
            return renpy.loader.transfn(filename) #should be renpy's view of FILENAME
        except:
            return False #renpy could not access FILENAME

    def wait_modified(filename):
        """Function that looks at the time at which a FILENAME (string) was last edited.
        If that time changes, it means FILENAME was edited, and we return its new contents."""
        last_modified = os.path.getmtime(filename)
        while last_modified == os.path.getmtime(filename):
            renpy.pause(1) #we call renpy's pause because the OS thinks the program is hanging when using time.sleep
        return string_read(filename) #then read FILENAME content

    def splitter(text, split):
        """Function to split a large block of text TEXT
        into smaller chunks length SPLIT. Then have renpy read out each chunk."""
        text_split = text.split()
        for each in range((len(text_split) // split) + 1):
            renpy.say("", ' '.join(text_split[:split])) #put it back together
            text_split = text_split[split:] #reassign the original list
        return

    #Now we make sure renpy can actually read/write these files...
    ai_file = exists(ai_file)
    user_file = exists(user_file)
    summarize_toggle = exists('summarize') #there are no user options to change this name
    sentiment = exists('sentiment') #same here

#Set renpy defaults. Mainly try disabling some UI elements.
default preferences.afm_enable = False
default preferences.desktop_rollback_side = "disable" #disable back button
default preferences.mobile_rollback_side = "disable" #disable back button

#The game starts here.
label start:
    scene bg #this loads in the bg.* file in the images directory
    show gpt neutral #base sentiment
    python:
        #and now, tell user some instructions.
        renpy.say("NOTICE", "Please make sure that 'erma.py' and 'sentiment.py' are not running. If they are, turn them off now. Once they have been turned off, you may click the text box to proceed.")
        string_save(ai_file, "") #blank them out so renpy doesnt crash later
        string_save(user_file, "")
        renpy.say("NOTICE", "You may now start 'erma.py' and 'sentiment.py'. Click the text box once they are running.")
    # These display lines of dialogue. - Ren'Py
    # Nuh uh! Infinite loops! - me
    while True:
        if exists('summarize'):
            $ renpy.say("NOTICE", "Neural Cloud compacting in progress. Please wait.")
            while exists('summarize'): #if we see the summarize file, that means the model is summarizing.
                pause 2 #just keep iterating through this loop
            $ renpy.say("NOTICE", "Neural Cloud compacting finished. You may click the text box to continue the conversation.")
        python: #start a python block
            if not string_read(user_file): #USER_FILE will be blanked by erma once it is passed to the AI
                user_input = renpy.input("Enter your input: ")
                string_save(user_file, user_input) #write renpy's input
            else: #must be AI turn then
                def wait_splitter(text, split):
                    """Function to call SPLITTER() on TEXT and SPLIT once
                    SENTIMENT has been modified"""
                    text_out = text #I expect TEXT to be a function. We should get its return val
                    sent_out = wait_modified(sentiment) #this one definitely is a function return
                    if 'positive' in sent_out:
                        renpy.show('positive') #self-explanatory
                    elif 'negative' in sent_out:
                        renpy.show('negative')
                    else: #neutral and other edge cases depending on the sentiment pipeline
                        renpy.show('neutral')
                    string_save(sentiment, "") #blank this out
                    return splitter(text_out, split) #run the actual splitting function
                if sentiment: #allows the user to choose whether to have the sentiment analysis features
                    wait_splitter(wait_modified(ai_file), 32) #run with sentiment wait
                else:
                    splitter(wait_modified(ai_file), 32) #run without sentiment wait
        pause 0.5 #necessary in order not to completely burn out the cpu
    #This ends the game. We shouldn't ever reach here.
    return
