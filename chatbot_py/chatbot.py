from pandas import read_csv
from laur_ai import LaurAI

class ChatBot:
    '''
    Executes Laur.AI
    '''
    def __init__(self):
        self.output_text("Please wait as Laur.AI loads")
        data_master = read_csv("data/master_data.csv")
        self.laurBot = LaurAI(data_master)

    def setup_laurai(self):
        '''
        cleans data, lematizes the data and creates a bag of words from
        lematized data
        '''
        # convert the data into it's base form
        self.laurBot.create_lemma()
        # represent data in bag
        self.laurBot.create_bag_of_words()

    def run(self):
        '''
        Run the program, output greeting and instructions, then 
        '''
        text = "Ask me anything :)\nControl C or Type \"Bye\" to quit"
        self.output_text(text)

        # loop that controls program
        stop = False
        while not stop:
            context = self.input_context()
            if context == "bye":
                # exit condition
                self.output_text("bye :))")
                stop = True
            else:
                response = self.laurBot.askQuestion(context)
                self.output_text(response)

        # farewellgi message
        self.output_text("Thank you for talking to Laur.AI")

    def input_context(self):
        '''
        recieve context from user
        '''
        context = input("> ")
        return context.lower()

    def output_text(self, text):
        '''
        @param - string to be displayed to user
        outputs the text
        ''' 
        print(text)
