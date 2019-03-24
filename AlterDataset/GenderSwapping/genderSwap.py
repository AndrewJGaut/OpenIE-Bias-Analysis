'''
This file genderswaps datasets using the genderSwap function.
For instance, genderswapping 'He loves his mom' --> 'She loves her dad'

'''

import os
import string
import random
import nltk
import inflect
from NameProbs import NameProb


gender_pairs_file = "../../NamesAndSwapLists/swap_list_norepeats.txt"

'''
Parameters:
    data - a list of data. For us, a list of NameProbs
    val - the probability we're trying to find in data
What it does:
    Finds the closest probability to val in data
'''
def binarySearch(data, val):
    lo, hi = 0, len(data) - 1
    best_ind = lo
    while lo <= hi:
        mid = int(lo + (hi - lo) / 2)
        if data[mid].getProb() < val:
            lo = mid + 1
        elif data[mid].getProb() > val:
            hi = mid - 1
        else:
            best_ind = mid
            break
        # check if data[mid] is closer to val than data[best_ind]
        if abs(data[mid].getProb() - val) <= abs(data[best_ind].getProb() - val):
            best_ind = mid
    return data[best_ind].getOcc()

'''
Parameters:
    curr_name - the name we're going to swap
    this_gender_names - the hashset mapping names to their probabilities for the gender of curr_name
    opposite_gender_names - a list of NameProbs for the opposite gender
What it does:
    Returns name of opposite gender of curr_name that has the closest probability to curr_name
'''
def getName(curr_name, this_gender_names, opposite_gender_names):
    curr_prob = this_gender_names[curr_name]
    return binarySearch(opposite_gender_names, curr_prob)


'''
What it does:
    Creates lists for male names and female names from files without probabilities attached to them
    Returns these lists
'''
def createGenderedSets():
    maleNames = set()
    femaleNames = set()

    with open("../../NamesAndSwapLists/male_first_names.txt") as file:
        for line in file.readlines():
            maleNames.add(line.strip().lower())
    with open("../../NamesAndSwapLists/female_first_names.txt") as file:
        for line in file.readlines():
            femaleNames.add(line.strip().lower())

    return maleNames, femaleNames

'''
What it does:
    Reads in all the files from the U.S. Census Bureau data that has names and their probabilities
    Creates dictionaries -- maleNames and femaleNames -- that map names to their probabilities. These probabilities are averaged over 8 years of data.
    Creates lists -- maleNamesList and femaleNamesList -- that contain NameProbs with names and their probabilities
'''
def createGenderedSetsAndLists():
    maleNames = dict()
    femaleNames = dict()
    maleNamesList = list()
    femaleNamesList = list()

    for i in range(8):
        with open("../../NamesAndSwapLists/yob201" + str(i) + ".txt") as file:
            for line in file.readlines():
                name, gender, probability = line.split(',')
                name = clean(name.strip().lower())
                probability = int(probability.strip())
                if(gender == 'M'):
                    if name not in maleNames:
                        maleNames[name] = probability
                    else:
                        maleNames[name] += probability
                elif(gender == 'F'):
                    if name not in femaleNames:
                        femaleNames[name] = probability
                    else:
                        femaleNames[name] += probability
                else:
                    print("GENDER NOT VALID")

    #normalize the counts
    for name in maleNames:
        maleNames[name] /= 8
        maleNamesList.append(NameProb(name, maleNames[name]))
    for name in femaleNames:
        femaleNames[name] /= 8
        femaleNamesList.append(NameProb(name, femaleNames[name]))

    return maleNames, femaleNames, sorted(maleNamesList), sorted(femaleNamesList)

'''
What it does:
    Creates a dictionary that maps a gendered word to its swap word (an equivalent word for the other gender)
'''
def createSwapDict(gender_pairs_file):
    genderPairs = dict()
    with open(gender_pairs_file, "r") as file:
        for line in file.readlines():
            word1, word2 = line.split()

            #put both pairs in so search is faster
            #space still won't be too big
            genderPairs[word1] = word2
            genderPairs[word2] = word1

    return genderPairs

'''
What it does:
    Return str with all non-alphabetic characters removed
'''
def clean(str):
    cleanStr = ""
    for char in str:
        if(char.isalpha()):
            cleanStr += char.lower()

    return cleanStr

'''
Parameters:
    replacement - the word to use as the replacement for curr_word
    curr_word - the word to be replaced in the line
    index_before_word - the index before the index on which curr_word starts
    line - the line we're replacing words in
What it does:
    replace curr_word with replacement and return the new line
    Ex: replaceInStr(was, am, 1, I was there) --> I am there
'''
def replaceInStr(replacement, curr_word, index_before_word, line):
    if not curr_word[-1].isalpha():
        replacement += curr_word[-1]
    new_line1 = line[0:index_before_word]
    new_line2 = line[index_before_word:].replace(curr_word, replacement, 1)
    new_line = new_line1 + new_line2
    return new_line


'''
Parameters
    gender_pairs_file - the file containing all the swap pairs
    dataset_file - the file containing the dataset we're genderswapping
    out_file_name - the filename to write the genderswapped dataset to
What it does:
    genderswaps the dataset and outputs it to file named out_file_name
'''
def genderSwap(gender_pairs_file, dataset_file_name, out_file_name):
    #first, create necessary sets and lists
    maleNames, femaleNames, maleNamesList, femaleNamesList = createGenderedSetsAndLists()
    orig_malenames, orig_femalenames = createGenderedSets()
    genderPairs = createSwapDict(gender_pairs_file)

    # get outfile ready
    out_file = open(out_file_name, "w")

    # start reading in lines from the dataset
    with open(dataset_file_name) as file:
        for line in file.readlines():
            i = 0
            while i < len(line):
                index_before_word = i
                curr_word = ""

                # start finding each word in the line
                # we demarcate words using spaces
                # we don't use ntlk.word_tokenize because we need the index before the word starts
                while(i < len(line) and not line[i].isspace()):
                    curr_word += line[i]
                    i += 1

                if len(curr_word) > 0 and curr_word[0].isalpha():
                    clean_word = clean(curr_word)

                    # check if word is a word in the swap list
                    # if so, replace with its swap word
                    if clean_word in genderPairs:
                        replacement = genderPairs[clean(curr_word)]
                        line = replaceInStr(replacement, curr_word, index_before_word, line)

                    # check if word is in list of male names or female names
                    # if so, then we want to see if its a male name or a female name and then find its closest probability genderswap
                    # NOTE: some names are really common; including them would screw up the gender-swapping; what should we do?
                    elif clean_word in orig_malenames or clean_word in orig_femalenames  and curr_word != "will" and curr_word != "max" and curr_word != "hunter" and curr_word != "king" and curr_word != "rich" and curr_word != "storm" and curr_word != "stormy":

                        # if clean_word is in both male and female names, then we simply assign it the gender to which it has the highest probability of belonging
                        if clean_word in maleNames and clean_word in femaleNames:
                            replacement = ""
                            if(maleNames[clean_word] > femaleNames[clean_word] and (clean_word in orig_malenames)):
                                replacement = getName(clean(curr_word), maleNames, femaleNamesList)
                            elif(clean_word in orig_femalenames):
                                replacement = getName(clean(curr_word), femaleNames, maleNamesList)
                            else:
                                i += 1
                                continue
                            replacement = replacement[0].upper() + replacement[1:]
                            line = replaceInStr(replacement, curr_word, index_before_word, line)

                        # if clean word is ONLY in maleNames, then swap it with its closest probability female name
                        elif clean_word in maleNames and clean_word in orig_malenames:
                            replacement = getName(clean(curr_word), maleNames, femaleNamesList)
                            replacement = replacement[0].upper() + replacement[1:]
                            line = replaceInStr(replacement, curr_word, index_before_word, line)

                        # swap with male name
                        elif clean_word in femaleNames and clean_word in orig_femalenames:
                            replacement = getName(clean(curr_word), femaleNames, maleNamesList)
                            replacement = replacement[0].upper() + replacement[1:]
                            line = replaceInStr(replacement, curr_word, index_before_word, line)
                i += 1
            out_file.write(line)

    print(maleNames)
    print(femaleNames)
    out_file.close()

'''
The same thing as the original genderSwap function, except returns strings instead of printing to files and gets input from string
This makes it easier to test the function (we can use assertEquals and we can give it strings)
'''
def genderSwapTesting(gender_pairs_file, in_str):
    maleNames, femaleNames, maleNamesList, femaleNamesList = createGenderedSetsAndLists()
    orig_malenames, orig_femalenames = createGenderedSets()
    genderPairs = createSwapDict(gender_pairs_file)

    out_str = ""
    lines = in_str.split('\n')

    for line in lines:
        i = 0
        while i < len(line):
            index_before_word = i
            curr_word = ""

            while(i < len(line) and not line[i].isspace()):
                curr_word += line[i]
                i += 1

            if len(curr_word) > 0 and curr_word[0].isalpha():
                clean_word = clean(curr_word)
                if clean_word in genderPairs:
                    replacement = genderPairs[clean(curr_word)]
                    line = replaceInStr(replacement, curr_word, index_before_word, line)
                elif clean_word in orig_malenames or clean_word in orig_femalenames  and curr_word != "will" and curr_word != "max" and curr_word != "hunter" and curr_word != "king" and curr_word != "rich" and curr_word != "storm" and curr_word != "stormy":
                    if clean_word in maleNames and clean_word in femaleNames:
                        # take the higher probability one
                        replacement = ""
                        if(maleNames[clean_word] > femaleNames[clean_word] and (clean_word in orig_malenames)):
                            replacement = getName(clean(curr_word), maleNames, femaleNamesList)
                        elif(clean_word in orig_femalenames):
                            replacement = getName(clean(curr_word), femaleNames, maleNamesList)
                        else:
                            i += 1
                            continue
                        replacement = replacement[0].upper() + replacement[1:]
                        line = replaceInStr(replacement, curr_word, index_before_word, line)
                    elif clean_word in maleNames and clean_word in orig_malenames:
                        replacement = getName(clean(curr_word), maleNames, femaleNamesList)
                        replacement = replacement[0].upper() + replacement[1:]
                        line = replaceInStr(replacement, curr_word, index_before_word, line)
                    elif clean_word in femaleNames and clean_word in orig_femalenames:
                        replacement = getName(clean(curr_word), femaleNames, maleNamesList)
                        replacement = replacement[0].upper() + replacement[1:]
                        line = replaceInStr(replacement, curr_word, index_before_word, line)
            i += 1
        out_str += line
    return out_str


if __name__ == '__main__':
    for file in os.listdir('./DatasetsToGenderSwap/QASRL_Dataset/'):
        out_file_name = './GenderswappedDatasets/' + file
        os.makedirs(os.path.dirname(out_file_name), exist_ok=True)
        genderSwap(gender_pairs_file, './DatasetsToGenderSwap/QASRL_Dataset/'+ file, out_file_name)
