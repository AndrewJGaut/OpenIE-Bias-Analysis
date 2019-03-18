'''
Creates a new dataset file containing only sentences with gendered words in them.
This helps us speed up obtaining the openIE extractions
'''

import re
import inflect

#file = open("NOW_genderswapped_randomswapnames.txt", "r")
#file = open("spaces_preprocessed_NOW_news_corpus.txt", "r")
#out_file = open("NOW_genderswapped_randomnames_genderedsentencesonly3.txt", "w")

'''
What it does:
    Creates and returns a hashset of all gendered words and names
    This way, we can check if words are in the hashset or not and, if a sentence has words in the hashset, then it's a gendered sentence
'''
def createGenderedSet():
    genderedSet = set()
    infl = inflect.engine()

    with open("../../NamesAndSwapLists/male_first_names.txt") as file:
        for line in file.readlines():
            genderedSet.add(clean(line.strip().lower(), infl))
    with open("../../NamesAndSwapLists/female_first_names.txt") as file:
        for line in file.readlines():
            genderedSet.add(clean(line.strip().lower(), infl))
    with open("../../NamesAndSwapLists/swap_list_norepeats.txt", "r") as file:
        for line in file.readlines():
            word1, word2 = line.split()

            #put both pairs in so search is faster
            #space still won't be too big
            genderedSet.add(word1)
            genderedSet.add(word2)

    return genderedSet

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

'''
Parameters:
    out_file - the file that the function will write to
What it does:
    For every sentence in the dataset file, it finds if that sentence has a gendered word or name in it
    If the sentence has a gendered word or name, then it writes the sentence to the gendered_dataset file
    Gendered_dataset file will have one gendered sentence per line
'''
def getGenderedDataset(dataset_file_name, out_file_name):
    dataset_file = open(dataset_file_name, "r")
    out_file = open(out_file_name, "w")

    genderedSet = createGenderedSet()
    infl = inflect.engine()

    for line in dataset_file.readlines():
        #punctuation = re.compile('[.|]')
        punctuation_regex = re.compile("(\.|!|\?)")
        punctuation = punctuation_regex.findall(line)
        sentences = re.split('[\.|!|\?]', line)
        for i in range(len(sentences)):
            sentence = sentences[i]
            for word in sentence.split():
                word = clean(word, infl)
                if word in genderedSet:
                    out_file.write(sentence + punctuation[i] + "\n")
                    break

    out_file.close()
    dataset_file.close()

'''
For testing; this reads from and returns strings, which is easier to test with
Other than those differences, this function is the same as the regular function
'''
def getGenderedDatasetTesting(in_str):
    genderedSet = createGenderedSet()
    infl = inflect.engine()
    out_str = ""

    for line in in_str.split('\n'):
        #punctuation = re.compile('[.|]')
        punctuation_regex = re.compile("(\.|!|\?)")
        punctuation = punctuation_regex.findall(line)
        sentences = re.split('[\.|!|\?]', line)
        for i in range(len(sentences)):
            sentence = sentences[i]
            for word in sentence.split():
                word = clean(word, infl)
                if word in genderedSet:
                    out_str += sentence + punctuation[i] + "\n"
                    break

    return out_str

if __name__ == '__main__':
    getGenderedDataset(file, out_file)