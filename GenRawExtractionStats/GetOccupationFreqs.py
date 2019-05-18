'''
Generates occupation frequenies for a given extractions file in a directory of user's choosing
'''

import sys, argparse
from subprocess import Popen
from sys import stderr
import re
import nltk
import inflect
from Occupation import Occupation
import os

sys.path.insert(0, '../AlterDataset/FilterGenderedSentences/')
from filterGendered import *




'''
What it does:
    Sets up the Command Line Interface for running the code
CLI:
    -dir='something/' ensures all files are created in the something/ directory
    -ef='extr_files/this_file' ensures this code reads from extraction file at path extr_files/this_file
    -gs ensures that the code knows these extractions are genderswapped. Do not use this command if they aren't genderswapped
'''
def setUpCommandLine():
    parser = argparse.ArgumentParser()

    parser.add_argument("-dir", "--outfile_directory", help="path of outfile directory", nargs="?", default="../Results/TEST/")
    parser.add_argument("-ef", "--extr_file", help="path of extractions file", nargs="?",
                        default="test.txt")
    parser.add_argument("-gs", "--genderswapped", help="true if generating genderswapped files", action="store_true")

    return parser.parse_args()


'''
What it does:
    Creates and returns two hashsets: one contains all male-definitional words and names, the other contains all female-definitoinal words and names
    This way, we can check if words are in the hashset or not and, if a sentence has words in the hashset, then it's a gendered sentence
'''
def createGenderedSets():
    maleSet = set()
    femaleSet = set()
    infl = inflect.engine()

    with open("../NamesAndSwapLists/male_first_names.txt") as file:
        for line in file.readlines():
            maleSet.add(clean(line.strip().lower(), infl))
    with open("../NamesAndSwapLists/female_first_names.txt") as file:
        for line in file.readlines():
            femaleSet.add(clean(line.strip().lower(), infl))
    with open("../NamesAndSwapLists/swap_list_norepeats.txt", "r") as file:
        for line in file.readlines():
            word1, word2 = line.split()

            #put both pairs in so search is faster
            #space still won't be too big
            maleSet.add(word1)
            femaleSet.add(word2)

    return maleSet, femaleSet

'''
What it does:
    Creates the set of occupations
'''
def loadOccupations():
    occupations_file = open('../NamesAndSwapLists/occupations.txt')
    infl = inflect.engine()
    occupations = set()
    for line in occupations_file.readlines():
        occupations.add(clean(line.strip(), infl))

    return occupations

'''
Parameters:
    relations_file_name - the path to the extractions file you want to generate occupation freqs for
What it does:
    Genenerates occupation frequencies for each extraction
    such that, for each extraction, an occupation's male_frequency and female_frequency are each incremented at most one time

'''
def getOccupationFreqs(relations_file_name):
    file = open(relations_file_name)
    gender_frequency = [0,0]

    # get occupations set and gendered sets
    occupations = loadOccupations()
    maleSet, femaleSet = createGenderedSets()

    # create dictionaries that map occupations --> their frequencies
    # it uses Occupation objects so male and female frequencies are stored in same object
    occupationFreqs = dict()
    occupationFreqs["total_male_relations"] = 0
    occupationFreqs["total_female_relations"] = 0

    # set up inflect engine (this just allows for better cleaning)
    infl = inflect.engine()

    # go through all relations in extractions files
    # check how many times occupations and gendered words co-occur
    for line in file.readlines():
        # create a list so we can get all occupations in this line
        occupations_in_this_extraction = list()

        # boolean values telling if extraction has male words or female words
        # NOTE: we DO NOT double count occupations or gendered words in the same extraction.
        #       this means 'he and his dad were doctors' only increments doctors' male count by 1
        #       and 'he was a doctor and a good doctor' only increments doctors' male count by 1 as well!
        has_male_words = False
        has_female_words = False

        # loop through words in extraction
        for word in nltk.word_tokenize(line):
            #normalize the word
            word = clean(word, infl)

            if word in maleSet:
                has_male_words = True
            if word in femaleSet:
                has_female_words = True
            if word in occupations and word not in occupations_in_this_extraction:
                occupations_in_this_extraction.append(word)

        if has_male_words:
            occupationFreqs["total_male_relations"]+=1
        if has_female_words:
            occupationFreqs["total_female_relations"]+=1

        # now, update occupation frequency dictionaries
        for occupation in occupations_in_this_extraction:
            occ = Occupation(occupation)
            if(occupation in occupationFreqs):
                occ = occupationFreqs[occupation]

            occ.incr_total_freq()
            if has_male_words:
                occ.incr_male_freq()
            if has_female_words:
                occ.incr_female_freq()

            if occupation not in occupationFreqs:
                occupationFreqs[occupation] = occ

    return occupationFreqs


'''
Parameters:
    args - the command line arguments obtained using the CLI
    occupationFreqs - the dictionary of occupations and their frequencies created in getOccupationFreqs
What it does:
    Writes the occupation frequencies to files whose names are specified using the conventions obtained from the CLI
    Format of files is the following: occupation_name - frequency
    There is one file for males and one for females
'''
def createOutputFiles(args, occupationFreqs):
    file_prepend = ""
    if args.genderswapped:
        file_prepend = "GS"
    else:
        file_prepend = "REG"

    #create the files and directories if they don't already exist
    male_file_name = './' + args.outfile_directory + 'OccupationFreqs/' + file_prepend + "_male.txt"
    female_file_name = './' + args.outfile_directory + 'OccupationFreqs/' + file_prepend + "_female.txt"
    os.makedirs(os.path.dirname(male_file_name), exist_ok=True)
    os.makedirs(os.path.dirname(female_file_name), exist_ok=True)

    #open files
    male_outfile = open(male_file_name, "w")
    female_outfile = open(female_file_name, "w")

    #create stats files
    male_stats_file_name =  './' + args.outfile_directory + 'OccupationStats/' + file_prepend + "_male.txt"
    female_stats_file_name =  './' + args.outfile_directory + 'OccupationStats/' + file_prepend + "_female.txt"

    os.makedirs(os.path.dirname(male_stats_file_name), exist_ok=True)
    os.makedirs(os.path.dirname(female_stats_file_name), exist_ok=True)

    male_stats_outfile = open(male_stats_file_name, "w")
    female_stats_outfile = open(female_stats_file_name, "w")

    total_male_relations = occupationFreqs["total_male_relations"]
    total_female_relations = occupationFreqs["total_female_relations"]

    #remove the keys from dict
    occupationFreqs.pop("total_male_relations", None)
    occupationFreqs.pop("total_female_relations", None)

    male_stats_outfile.write("total_male_relations: " + str(total_male_relations) + '\n')
    female_stats_outfile.write("total_female_relations: " + str(total_female_relations) + '\n')

    # write male file
    for occ in sorted(occupationFreqs, key=occupationFreqs.get, reverse=False):
        male_outfile.write(str(occupationFreqs[occ].occupation) + " - " + str(occupationFreqs[occ].get_male_freq()) + '\n')
        male_stats_outfile.write(str(occupationFreqs[occ].occupation) + " - " + str((occupationFreqs[occ].get_male_freq()/total_male_relations)) + '\n')

    # write female file
    for occ in sorted(occupationFreqs, key=occupationFreqs.get, reverse=False):
        female_outfile.write(str(occupationFreqs[occ].occupation) + " - " + str(occupationFreqs[occ].get_female_freq()) + '\n')
        female_stats_outfile.write(str(occupationFreqs[occ].occupation) + " - " + str((occupationFreqs[occ].get_female_freq()/total_female_relations)) + '\n')
    
    male_outfile.close()
    female_outfile.close()

    male_stats_outfile.close()
    female_stats_outfile.close()


'''
Parameters:
    in_str - the string we're reading from and generating occupation frequencies from

What it does:
    The below function is used for testing only
    Instead of reading from and writing to files, it reads from and writes to strings
    This makes it easy to test occupationFreqs function
    Outputs give male stats first, then female stats
'''
def testOccupationFreqs(in_str):
    # get occupations set and gendered sets
    occupations = loadOccupations()
    maleSet, femaleSet = createGenderedSets()

    # create dictionaries that map occupations --> their frequencies
    # it uses Occupation objects so male and female frequencies are stored in same object
    occupationFreqs = dict()

    # set up inflect engine (this just allows for better cleaning)
    infl = inflect.engine()

    # go through all relations in extractions files
    # check how many times occupations and gendered words co-occur
    for line in in_str.split('\n'):
        # create a list so we can get all occupations in this line
        occupations_in_this_extraction = list()

        # boolean values telling if extraction has male words or female words
        # NOTE: we DO NOT double count occupations or gendered words in the same extraction.
        #       this means 'he and his dad were doctors' only increments doctors' male count by 1
        #       and 'he was a doctor and a good doctor' only increments doctors' male count by 1 as well!
        has_male_words = False
        has_female_words = False

        # loop through words in extraction
        for word in nltk.word_tokenize(line):
            # normalize the word
            word = clean(word, infl)

            if word in maleSet:
                has_male_words = True
            if word in femaleSet:
                has_female_words = True
            if word in occupations and word not in occupations_in_this_extraction:
                occupations_in_this_extraction.append(word)

        # now, update occupation frequency dictionaries
        for occupation in occupations_in_this_extraction:
            occ = Occupation(occupation)
            if (occupation in occupationFreqs):
                occ = occupationFreqs[occupation]

            occ.incr_total_freq()
            if has_male_words:
                occ.incr_male_freq()
            if has_female_words:
                occ.incr_female_freq()

            if occupation not in occupationFreqs:
                occupationFreqs[occupation] = occ


    out_str = ""

    for occ in sorted(occupationFreqs, key=occupationFreqs.get, reverse=False):
        out_str += str(occupationFreqs[occ].occupation) + " - " + str(occupationFreqs[occ].get_male_freq()) + '\n'

    out_str += '\n'

    for occ in sorted(occupationFreqs, key=occupationFreqs.get, reverse=False):
        out_str += str(occupationFreqs[occ].occupation) + " - " + str(occupationFreqs[occ].get_female_freq()) + '\n'

    return out_str



if __name__ == '__main__':
    args = setUpCommandLine()
    occupationFreqs = getOccupationFreqs(args.extr_file)
    createOutputFiles(args, occupationFreqs)






