#merge this and mack once we decide we want to use this or not

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import re
import datetime

from kivy.app import App
from kivy.uix.scrollview import ScrollView
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty
from kivy.lang import Builder
from kivy.core.window import Window
# import pandas
import nltk
from pandas import DataFrame, Series, read_csv, read_pickle
from re import sub
from nltk.stem import wordnet
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk import pos_tag
from sklearn.metrics import pairwise_distances
from nltk import word_tokenize
from nltk.corpus import stopwords

from clean_master_data import DataCleaner

# This is for the autocorrect functionality
from textblob import TextBlob

# This is for the Named Entity Recognition functionality
import spacy
import en_core_web_sm
from random import randint


print("Starting Laur...")
#import laur_ai as LaurAI



def time_now():
    return "[" + datetime.datetime.now().strftime("%H:%M:%S") + "]"

#set specifics for the stuff in the gui
root_widget = Builder.load_string('''
<ScrollableLabel>:
    #Specifics of Scrollable Label
    text: app.text
    Label:
        text: root.text
        font_size: 14
        text_size: self.width, None
        color: [0,0,0,1]
        markup: True
        size_hint_y: None
        pos_hint: {"left":1, "top":1}
        height: self.texture_size[1]
        valign: 'top'
        halign: 'left'
        scroll_y: None
        padding_x: 7
        padding_y: 7
<BoxLayout>
<RootWidget>:
    #Background Set
    BoxLayout:
        size: root.size
        pos: 0,0
        canvas.before:
            Rectangle:
                pos: self.pos
                size: self.size
                source: '../mackenzie.jpg'

        #Conversation Box
        BoxLayout:
            orientation: 'vertical'
            padding: 20
            spacing: 10
            BoxLayout:
                size_hint: None, None
                size: root.width * 0.35, root.height - 100
                canvas.before:
                    Color:
                        rgba: 0,0,0,.75
                    BorderImage:
                        source: 'zelda.png'
                        pos: self.x - 1, self.y - 1
                        size: (root.width * 0.35)+2, root.height - 98
                    Color:
                        rgba: .95,.95,.95,.9
                    Rectangle:
                        pos: self.pos
                        size: root.width * 0.35,root.height - 100
                ScrollableLabel:
                    id: laur_output
                    markup: True

            #Bottom Bar
            BoxLayout:
                orientation: 'horizontal'
                spacing: 10
                size_hint_y: .1
                TextInput:
                    id: txt_input
                    background_color: [1,1,1,.95]
                    foreground_color: [0,0,0,1]
                    cursor_color: [0,0,0,1]
                    size_hint_x: .8
                    #multiline: False
                    write_tab: False
                    hint_text: "Insert Text Here"
                Button:
                    id: btn
                    text: 'Send'
                    font_size: 20
                    bold: True
                    size_hint_x: .2
                    background_color: [.8, .8, .8, 1]
                    color: [1, 1, 1, 1]
                    on_press: app.runStuff(txt_input.text)
                    on_release: app.read()
                    on_release: txt_input.text=""
''')


print("Laur Started")


class RootWidget(BoxLayout):
    pass


class ScrollableLabel(ScrollView):
    pass


class Laur_AI(App):
    text = StringProperty('')

    #Initiate the file to write and read from / Start conversation
    def __init__(self, data, use_cleaned_data=True, **kwargs):
        super().__init__(**kwargs)
        Window.bind(on_key_down=self._on_keyboard_down)
        Window.bind(on_key_up=self._on_keyboard_up)
        with open('Conversation.txt', 'w') as f:
            f.write('[b]' + time_now() + ' Laur:[/b] HI! My name is Laur and I am a chatbot!' + '\n')
            f.close()
        with open('Conversation.txt', 'r') as f:
            contents = f.read()
            self.text = contents
        self.data = data[["comment", "response"]]
        self.data_cleaner = DataCleaner()
        self.cleaned_data = DataFrame(columns=["Question", "Answer"])
        # use data if provided
        if use_cleaned_data:
            self.cleaned_data = read_pickle("../data/master_data_cleaned.pkl")
            if len(self.cleaned_data) != len(self.data):
                # if the data does not match, retrain
                self.cleaned_data = self.data_cleaner.clean_data(self.data)
                # to improve speed, save to master cleaned
                self.cleaned_data.to_pickle("../data/master_data_cleaned.pkl", protocol=4)

        self.finalText = DataFrame(columns=["Lemmas"])
        self.c = CountVectorizer()
        self.bag = None

    #Make it so on keyboard enter it runs and clears text of text box
    def _on_keyboard_down(self, instance, keyboard, keycode, text, modifiers):
        if keycode == 40:  # enter
            app.runStuff(self.root.ids.txt_input.text)
    def _on_keyboard_up(self,instance, keyboard, keycode):
        if keycode == 40:  # enter
            app.read()
            self.root.ids.txt_input.text=""

    #Handles user input and prints to screen
    def runStuff(self, input):
        try:
                #split sentences up into parts
                #userInput = re.split('[\.!?]', input.lower().rstrip('.!?'))
                full_reply = ' '
                #print("got here")
                if input == "bye":
                    app.get_running_app().stop()
                #makes call to tree to get response
                #print("stuck getting response")
                response = app.askQuestion(input.lower())
                full_reply += response + ' '
                #print("got a response")
                with open('Conversation.txt', 'a') as f:
                    f.write('[b]' + time_now() + ' User:[/b] ' + input + '\n')
                    f.write('[b]' + time_now() + ' Laur:[/b]' + str(full_reply) + '\n')
                    f.close()
        except:
                pass

    #Reads text from Conversation.txt to screen
    def read(self):
        with open('Conversation.txt', 'r') as f:
            contents = f.read()
            self.text = contents

    def build(self):
        return RootWidget()


    def clean_line(self, line):
        '''
        Clean the line
        This line makes all lowercase, and removes anything that isn't a number
        '''
        return sub(r'[^a-z ]', '', str(line).lower())

    def tokenize_and_tag_line(self, line):
        ''' Tokenizes the words then tags the tokenized words '''
        return pos_tag(word_tokenize(line), None)

    def create_lemma_line(self, input_line):
        ''' We create the lemmatizer object '''
        lemma = wordnet.WordNetLemmatizer()
        # This is an array for the current line that we will append values to
        line = []
        for token, ttype in input_line:
            checks = ["a", "v", "r", "n"]
            if(ttype[0].lower() not in checks):
                ttype = "n"
            line.append(lemma.lemmatize(token, ttype[0].lower()))
        return {"Lemmas": " ".join(line)}

    def create_lemma(self):
        ''' Creates lemmas for the cleaned data (lemma is the lower )'''
        lemmas = []
        for j in self.cleaned_data.iterrows():
            lemmas.append(self.create_lemma_line(j[1][0]))
        self.finalText = self.finalText.append(lemmas)

    def create_bag_of_words(self):
        '''
        create a bag of words and save in a dataframe with the same indicies as
        the master data
        '''
        self.bag = DataFrame(self.c.fit_transform(self.finalText["Lemmas"]).toarray(),
                             columns=self.c.get_feature_names(), index=self.data.index)

    def askQuestion(self, context):
        '''
        @param question: a string context given by the user
        output a string response to context
        ---
        Compute most similar context to the input using semisupervised learning
        and return approproate response to the determined most similar context
        '''
        # correct the given input
        context = self.autocorrect(context)

        # Removes all "stop words"
        valid_words = []
        for i in context.split():
            if i not in stopwords.words("english"):
                valid_words.append(i)

        # Clean the data and get tokenized and tagged data
        valid_sentence = self.tokenize_and_tag_line(self.clean_line(" ".join(valid_words)))
        lemma_line = self.create_lemma_line(valid_sentence)

        try:
            index = self.determine_most_similar_context(lemma_line)
            if index != -1:
                # respond with response to most similar context
                answer = self.data.loc[index, "response"]
                return answer

            # Else we are going to respond with one of the nouns with the following context
            nlp = en_core_web_sm.load()
            nouns = nlp(context)
            # Get a random noun from the generated list of nouns, and select the first element
            # which is the noun (second is what kind of noun)
            noun = nouns[randint(0, len(nouns)-1)]

            return "Sorry :,( I don't know what " + str(noun) + " is!"


        except KeyError:
            # an unknown word was passed
            return "I am miss pwesident uwu"

    def autocorrect(self, input):
        # Creates the NLP named entity recognition
        nlp = en_core_web_sm.load()
        # Finds all of the nouns in the input string
        nouns = nlp(input)

        finalText = ""
        # For all of the values in the input
        for i in input.split(" "):
            # If the values are not nouns (autocorrect breaks on nouns)
            if i not in str(nouns):
                # Run autocorrect on the nouns and add it to the final string
                finalText += str(TextBlob(i).correct()) + " "
            # Else just add the noun
            else:
                finalText += i + " "

        return finalText



    def determine_most_similar_context(self, lemma_line, similarity_threshold=0.05):
        '''
        @param lemma_line: a dictionary of words from the input
        ----
        returne index of datapoint with most similar context to one given
        '''
        # create dataframe of one row initialized to zeros
        # this will represent the lemma
        valid_sentence = DataFrame(0, columns=self.bag.columns, index=[0])

        # set column of 1's for words in lemma line
        for i in lemma_line["Lemmas"].split(' '):
            if i in valid_sentence.columns:
                    # if the column exists, laur.ai recognizes the word
                    # if laur.ai recognizes the word, it will on it
                    # otherwise, do not
                    valid_sentence.loc[:, i] = 1
            else:
                try:
                    for syn in wordnet.synsets(i):
                        if syn in valid_sentence.columns:
                            # if the column exists, laur.ai recognizes the word
                            # if laur.ai recognizes the word, it will on it
                            # otherwise, do not
                            valid_sentence.loc[:, i] = 0.1
                            break
                except AttributeError:
                    # Module has no attribute synsets
                    # (you have entered something that doesn't exist)
                    break

        # find cosine similarity
        cosine = 1 - pairwise_distances(self.bag, valid_sentence, metric="cosine")
        # prepare data to be used in series with data's index
        cosine = Series(cosine.reshape(1,-1)[0], index=self.data.index)

        # determine index of element with highest similarity
        # the answer is the response at this index
        # if it does not find any datapoints similar then it recognizes nothing
        # in the input and the index returned is -1

        # We can solve the 0 problem by simply saying that if the cosine.max() is
        # less than 0.01 similarity we are going to respond with a predefined message

        if cosine.max() < similarity_threshold:
            return -1

        # return cosine.idxmax()
        # if multiple indicies share the maximum value, pick a random
        # create list of indicies of all maximum values
        max_index = cosine[cosine.values == cosine.max()].index
        # return a random index from the list
        i = randint(0,len(max_index)-1)
        return max_index[i]

print("Please wait as Laur.AI loads")

data_master = read_csv("../data/master_data.csv")


# First we need to clean the data, so it is all lower case and without special
# characters or numbers
# We can then tokenize the data, which means splitting it up into words instead
# of a phrase. We also need to know the type of word


if __name__ == '__main__':
    app = Laur_AI(data_master)
    app.create_lemma()

    # Now we can start to create the bag of words
    app.create_bag_of_words()
    app.run()
