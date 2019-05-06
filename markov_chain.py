import json

from random import randint

class MarkovChain():
    def __init__(self):
        self.mc = {}
        self.starting_words = []
        self.items = []
        self.cleaned_data = []
        self.stop_words = ['.', '?', '!']
        
    def read_text_file(self, file):
        text_file = open(file, 'r', encoding='utf-8')
        for item in text_file:
            self.items.append(item)
    
    def clean_data(self):
        item_length = len(self.items)
        full_length_data = []
        processed_data = []
        
        # Append blocks of tweets that were seperated by '.....'
        for i in range(item_length):
            if (i >= item_length - 1):
                break
            current_item = self.items[i]
            next_item = self.items[i + 1]
            if (current_item[:2] == ".." and next_item[len(next_item) - 3: -1] == ".."):
                new_item = next_item.strip('\n').strip('..') + ". " + current_item.strip('..')
                full_length_data.append(new_item.replace('&amp', 'and'))
                
            elif ('..' not in current_item and 'RT ' not in current_item and len(current_item) > 1):
                full_length_data.append(current_item.replace('&amp;', 'and'))
        
        # Remove new line characters and double quotes
        for data in full_length_data:
            if ('”' in data):
                clean_data = data.replace('”', '"').replace('“', '"')
                processed_data.append(clean_data.strip('\n').replace('\"', ''))
            else:
                processed_data.append(data.strip('\n').replace('\"', ''))
            
        
        # Add a stop word to the end of each item if it doesnt exist
        for data in processed_data:
            if (data[-1] not in self.stop_words):
                data += '.'
            self.cleaned_data.append(data)
                
        print("Data cleaned!")
        print("Length of uncleaned data: " + str(len(self.items)))
        print("Length of cleaned data: " + str(len(self.cleaned_data)))
        
    def build_markov_chain(self):
        for data in self.cleaned_data:
            tokenize = data.split(' ')
            tokenize_length = len(tokenize)
            # Get starting words
            if (len(tokenize) > 1 and tokenize[0] != ''):
                self.starting_words.append(tokenize[0])

            for i in range(tokenize_length):
                if (i >= tokenize_length - 1):
                    break
                current_word = tokenize[i]
                if (current_word not in self.mc):
                    self.mc[current_word] = []
                    
                self.mc[current_word].append(tokenize[i + 1])
        print(json.dumps(self.mc))
    def generate_text(self):
        generated_text = ''
        generating = True
        
        word = self.starting_words[randint(0, len(self.starting_words) - 1)]
        generated_text += word
        
        while (generating):
            rand_index = randint(0, len(self.mc[word]) - 1)
            next_word = self.mc[word][rand_index]
            
            generated_text += " " + next_word
            word = next_word
            
            if (next_word[-1] in self.stop_words or len(next_word) == 0):
                generating = False
                
        print("Trump Tweet: \n")
        return generated_text
        
    def export_markov_chain_in_json(self, filename):
        export_dict = {"starting_words": self.starting_words,
                       "body": self.mc,
                       "stop_words": self.stop_words}
        
        with open(filename + '.json', 'w', encoding='utf-8') as outfile:
            json.dump(export_dict, outfile)
            print("Exported " + filename + " as a json file!")
            
markov = MarkovChain()
markov.read_text_file('tweets_realDonaldTrump.txt')
markov.clean_data()
markov.build_markov_chain()
markov.export_markov_chain_in_json('markov_chain')

def run():
    return markov.generate_text()