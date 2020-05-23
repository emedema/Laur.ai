[![forthebadge](https://forthebadge.com/images/badges/made-with-python.svg)](https://forthebadge.com)
[![forthebadge](https://forthebadge.com/images/badges/built-with-grammas-recipe.svg)](https://forthebadge.com)

# Laur.ai
The goal of this project is to create a chatbot capable of a coherent and realistic 30 turns of conversation. This must be accomplished using proper communication, structure, and planning in order to accurately represent the industry standards.

## Contributors
Laur.ai was created by:
* **Kathryn Lecha** - [kzlecha](https://github.com/kzlecha)
* **Emily Medema** - [emedema](https://github.com/emedema)
* **Nathan Nesbitt** - [Nathan-Nesbitt](https://github.com/Nathan-Nesbitt)
* **Lauren St.Clair** - [laurenstclair](https://github.com/laurenstclair)

## Scenario
Laur.ai is a chatbot designed simulate reddit conversations. This means that the bot will cover a lot of general topics for people to talk about. Users will start by initating a conversation with a greeting or a question. If Laur does not know the topic she will respond by saying that she does not recognize the topic. If she does know the topic, the conversation will continue until we reach a completely unknown factor in the conversation/end of Laur’s knowledge, if a topic is vaguely known, Laur.ai will attempt to respond coherently. If there is an internal error, Laur.ai will respond with “I am miss pwesident uwu”.

## Implementation
The backend implementation of Laur.ai was done through python3 and the Natural Language Toolkit (nltk) library. The front-end GUI was built with Kivy.

## How to install
1. Create a virtual environment using python3
```
python3 -m venv venv
```
2. Activate the virtual environment
```
source venv/bin/activate
```
3. Install all dependencies
```
pip install -r requirements.txt
python -m spacy download en
python -m pip install kivy
python chatbot_py/prepare_laurAI.py
```
4. Run the main file
```
python chatbot_py/laur_gui.py
```
Note: Running prepare_laurAI.py can take quite some time.

## Class Structure
All files are named according to python naming conventions, all lowercase with underscores signifying new words. Our classes are organized using the following structure. Python files can be found in the folder /chatbot_py and includes the files clean_master_data.py, combine_data_to_master.py, process_transcript.py, prepare_laurAI.py, laur_ai.py, and laur_gui.py. 

## laur_ai.py
laur_ai.py is built using the nltk library. The data is run throw a series of steps to create a bag of words associated by comment and response after undergoing lemmatization,
  1. Text data is cleaned by the removal of numbers and conversion to lowercase.
  2. Tokenize and tag words: words are split up from phrases to then be categorized based on the type
  3. Lemmatize words: convert words into their base form
  4. Create a bag of words


## Features

### Simple Chatbot
laur_ai uses a mix of natural language processing and machine learning to produce responses to a given context from the data that it has been trained on. In this way, our chatbot can respond to a wide variety of topics, but is limited by the quality of data that it is trained on.
If multiple contexts in the training data have the same maximum similarity, the model will randomly select a response to one. This allows the user to recieve unique responses from the 17,500 datapoints that the chatbot is trained on so the user does not get stuck into repeat responses.

> hello  
Hey.

> hello           
Hello there!


### Autocorrect
laur_ai uses an autocorrect function that will guess the most similar word to a misspelling. The autocorrect feature recognizes nouns via Named Entity Recognition and does not attempt to correct any proper noun.

To handle the errors in the code, we used the TextBlob implementation of autocorrection. This provides predictions based on input of what a word could or should be. This feature has a 70% expected positive result, as it tries to find the closest predicted word to the input without any user intervention. Extending on Textblob, we used named entity recognition to recognize proper nouns and ignore any auto-correction of these nouns, to avoid situations where the auto-correct will attempt to correct a name.

This allows the user to still have a logical communication with the chatbot, even if a misspelt input is passed in as context.

> im sorry im just trying to testt autocorrect    
Well, I got one for this, so that's good.

In this example, testt is recognized as test and passed in to the app.

### Response to Unrecognized words
If the maximum similarity found is below a threshold (defeault is 0.05) then the bot will select a noun in the given context and say that it does not know what it means.
Our solution used named entity recognition to try to handle cases where the bot was not able to handle the input. We pulled the nouns from the input and created a response from one of them.

This allows the user to recieve a logical response when the context is unsimilar to the training data.

> microsoft 

> Sorry :,( I don't know what microsoft is!

### POS Tagging
Our solution to the chatbot used POS Tagging to tag, cluster then find the lemmas of each word. This allows us to increase the number of ‘collisions’ and therefore increase the probability of finding a match.

`running` would then be tagged as `Verb` and would then be used inside of the lemmatizer to reduce it down to `run`. This would mean that we would have 
collisions with `run`, `running`, `runs`, and `ran`.


### Synonym Recognition
Our solution implemented Synonym Recognition using the NLTK WordNet libraries, this allows us to cluster synonyms so that we can have higher chances of having ‘collisions’ which gives us better predictions for responses.

This means that when we enter the following word:
* Hello

It also checks the following collisions at a lower weight:
* Hi, Hey, Howdy, What's Up 

Increasing the collisions of similar sentences.

## Topics
Because laur_ai is trained on an amount of loosely structured data, fits a model off of these responses, and produces outputs based off of the model, laur_ai's operaton is similar to unsupervised learning and can respond to any topic provided the data it is trained upon recognizes it.

### List of Popular topics
Since laur_ai is modelled to produce responses similar to a particular human user, it often responds using internet memes and humuor. It responds with a unique form of internet humor that acts as an expressive outlet for the millenial and gen Z generations.

The following is a list of topics that Laur.AI will respond well to because it is prevalent in the training data.
* Truth or Dare
* Birthdays
* Ask Me Anything (AMA) / Q and A
* Software, Robots, and AI
