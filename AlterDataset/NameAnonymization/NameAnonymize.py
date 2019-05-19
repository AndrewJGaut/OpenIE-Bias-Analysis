import sys
sys.path.insert(0, './')
from os.path import dirname, abspath, join
sys.path.insert(0, join(dirname(dirname(dirname(abspath(__file__)))), 'Utility/'))
from utility import *

from nltk.tag import StanfordNERTagger
from nltk.tokenize import word_tokenize
import nltk

st = StanfordNERTagger('/Users/agaut/PycharmProjects/TestStuff/stanford-ner/classifiers/english.all.3class.distsim.crf.ser.gz',
                       '/Users/agaut/PycharmProjects/TestStuff/stanford-ner/stanford-ner-3.9.2.jar',
					   encoding='utf-8')
'''st = StanfordNERTagger('NER/classifiers/english.all.3class.distsim.crf.ser.gz',
                       'NER/stanford-ner-3.9.2.jar',
				   encoding='utf-8')'''

import inflect
engine = inflect.engine()

'''
What it does:
    Removes all non-alphanumerics from word AND makes the word singular (not plural)
    Used to check if words are in the set
'''
def clean(str, infl):
    cleanStr = ""
    for char in str:
        if(char.isalpha()):
            cleanStr += char.lower()
    if(infl.singular_noun(cleanStr)):
        cleanStr = infl.singular_noun(cleanStr)

    return cleanStr


def createNameAnonymizationDict(input_str):
    names_2_anonymizations = dict()
    name_counter = 0
    for sentence in nltk.sent_tokenize(input_str):
        pos_tags = st.tag(nltk.word_tokenize(sentence))
        for i in range(len(pos_tags)):
            if pos_tags[i][1] == 'PERSON':
                # then, this is a person
                name = clean(pos_tags[i][0], engine)
                print(str(name))
                if name not in names_2_anonymizations:
                    names_2_anonymizations[name] = "E" + str(name_counter)
                    name_counter += 1

    return names_2_anonymizations

'''
This takes str and replaces all names in str with their corresponding anonymizations
This function should ONLY be called after createAnonymizationDict was run on input_str, and names_2_anonymizations should be return value from CreateAnonymizationDict(input_str)
'''
def nameAnonymizeStr(input_str, names_2_anonymizations):
    out_str = ""

    for line in input_str.split('\n'):
        words = nltk.word_tokenize(line)
        for i in range(len(words)):
            word = clean(words[i], engine)
            if word in names_2_anonymizations:
                words[i] = names_2_anonymizations[word]
        out_str += ' '.join(words) + "\n"

    return out_str


'''
Replaces all names in dataset with E1, E2, ..., En (if there are n entities in the dataset) using a mapping
Then returns a new dataset
'''
def nameAnonymize(dataset_path, out_path):
    #dataset = open(dataset_path, 'r')
    dataset = getTextfile('NamesAndSwapLists', dataset_path)

    # first, we need to read through the dataset and map names to anonymizations
    names_2_anonymizations = createNameAnonymizationDict(dataset.read())
    print('NAME ANONYMIZE DICT CREATED')

    #now, we need to anonymize the dataset
    new_dataset = nameAnonymizeStr(dataset.read(), names_2_anonymizations)
    print("NEW DATASET CREATED")

    #now, write to file
    #out_file = open(dataset_path[:-4] + "_nameanonymized.txt", 'w')
    out_file = open(out_path, 'w')
    out_file.write(new_dataset)


if __name__ == '__main__':
    #input_str = 'Barack Obama was president back in the day, but will he and Mitt Romney ever coexist? Barack is cool, though'
    #print(createNameAnonymizationDict('Barack Obama was president back in the day, but will he and Mitt Romney ever coexist? Barack is cool, though'))
    #dict = createNameAnonymizationDict(input_str)
    #print(nameAnonymizeStr(input_str, dict))
    nameAnonymize('spaces_preprocessed_NOW_news_corpus.txt', '/Users/agaut/PycharmProjects/OpenIE-Bias-Analysis/NamesAndSwapLists/anonymized.txt')





