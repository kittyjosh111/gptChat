## Installation

1. Install Ollama and download an AI model.

2. Download the Renpy SDK from the internet. Make sure it is the one for your OS.

3. Using the SDK, create a new project/game. Customize the options to your liking, it won't affect my scripts.

4. Download the ```erma``` folder from this repository.

5. Move ```erma.py``` and ```requirements.txt``` from the ```erma``` folder into the game/ folder of you RenPy project. You can use your SDK to open this folder.

6. Move ```script.rpy``` and ```sentiment.rpy``` in this folder (integrations/renpy) into the game/ folder of your RenPy project. Your OS should ask you whether to replace script.rpy. Choose to replace the already-existing script.rpy.

6. Make a python venv to do things in. For example, in the project folder, run ```python3 -m venv venv```. Then activate it. ```source venv/bin/activate```

7. Navigate to the game/ folder of your RenPy project. Install the requirements for ```erma.py``` with pip. For example, run ```pip install -r requirements.txt```.

8. Makes sure that transformers is installed. Run ```pip install transformers```.

9. Navigate to the images/ folder in the RenPy project.

10. Put in three images, one for positive, neutral, and negative emotions. Title them ```positive.png```, ```neutral.png```, and ```negative.png```, respectively.

11. If you want, place a background image in the same folder and title it ```bg.jpg```.

## Running without sentiment analysis

1. Open ```erma.py``` with an editor. Uncomment the line ```ncb, ai_file, user_file = "neuralcloud_backup.ncb", 'neuralcloud_ai.file', 'neuralcloud_user.file'```. This should be near fourth to last line.

2. Then write the start function. MAKE SURE YOU SET BRIDGE_ACTIVE TO TRUE. As an example, you paste this function call into the last line of ```erma.py```: ```start('qwen:0.5b', bridge_active=True, local_summary="philschmid/flan-t5-base-samsum")```. Replace qwen:0.5b with your model name. If you don't want to use the local_summary feature, remove that argument from inside the function call.

3. Save your edits to ```erma.py```. Now activate the venv from earlier and run ```erma.py```.

4. Follow the instructions from ```erma.py``` if they appear.

5. Once ```erma.py``` reports that it is "Starting conversaton", you can open the RenPy SDK and launch your project.

6. Now you should be able to converse with the AI model through RenPy.
