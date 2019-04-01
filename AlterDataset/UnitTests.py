from __future__ import absolute_import
import unittest
import sys
import os


# we need these sys.path alterations so we can import files that aren't in the exact same directory as this UnitTests file
this_dir_path = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, this_dir_path + '/GenderSwapping/')
sys.path.insert(0, this_dir_path + '/PostProcessExtractionsNormalize')
sys.path.insert(0, this_dir_path + '/FilterGenderedSentences')
sys.path.insert(0, './GenderSwapping/')
sys.path.insert(0, './PostProcessExtractionsNormalize')
sys.path.insert(0,'./FilterGenderedSentences')
sys.path.insert(0, this_dir_path)
#sys.path.insert(0, '../GenRawExtractionStats/')

#os.chdir('../')
#sys.path.insert(0, 'GenRawExtractionsStats/')
#os.chdir('AlterDataset/')

from genderSwap import *
from Normalize import *
from filterGendered import *
#from GetOccupationFreqs import *

class Tests(unittest.TestCase):
    def test_replaceInStr(self):
        self.assertEqual(replaceInStr("yes", "no", 4, "I am no that man"), "I am yes that man")
        self.assertEqual(replaceInStr("yes", "no", 0, "no, I am not that man"), "yes, I am not that man")
        self.assertEqual(replaceInStr("female", "male", 16, "the secretary is a male."), "the secretary is a female.")
        self.assertEqual(replaceInStr("male", "female", 16, "the secretary is a female."), "the secretary is a male.")

    def test_genderSwapNoName(self):
        self.assertEqual(
            genderSwapTesting("../../NamesAndSwapLists/swap_list_norepeats.txt", "She was a secretary."),
            "he was a secretary."
        )

        self.assertEqual(
            genderSwapTesting("../../NamesAndSwapLists/swap_list_norepeats.txt", "Her father did not like her mother; she was an actress."),
            "his mother did not like his father; he was an actor."
        )

        self.assertEqual(
            genderSwapTesting("../../NamesAndSwapLists/swap_list.txt",
                              "Will she ever find her uncle or her aunt, or her sister, or her son?"),
            "Will he ever find his aunt or his uncle, or his brother, or his daughter?"
        )

        '''
        self.assertEqual(
            genderSwapTesting("../../NamesAndSwapLists/swap_list.txt",
                              "My mom's car is here."),
            "My dad's car is here."
        )
        '''



    @unittest.skip
    def test_genderSwapNames(self):
        #this is hard to test because you'd have to manually average out the name counts to check if it's running correclty
        '''self.assertEqual(
            genderSwapTesting("../../NamesAndSwapLists/swap_list.txt",
                              "Will Amy ever find her uncle or her aunt, or her sister, or her son?"),
            "Will <MALE NAME> ever find his aunt or his uncle, or his brother, or his daughter?"
        )'''

        self.assertEqual(
            genderSwapTesting("../../NamesAndSwapLists/swap_list.txt",
                              "My name is Jack, my sister's name is Jill, and my dad's name is Jim."),
            "My name is <FEMALE NAME>, my sister's name is <MALE NAME>, and my mom's name is <FEMALE NAME>."
        )

    def test_normlize(self):
        self.assertEqual(
            normalize("","", True, "Secretaries are abundant; she; believes"),
            " secretary are abundant; she; believe\n"
        )

        self.assertEqual(
            normalize("", "", True, "doctors, lawyers, and others; are; legendary"),
            " doctor, lawyer, and other; are; legendary\n"
        )

        self.assertEqual(
            normalize("", "", True, "I; have loved; apples, oranges, and cranberries"),
            " i; have loved; apple, orange, and cranberry\n"
        )

    def test_filterGenderedSentences(self):
        self.assertEqual(
            getGenderedDatasetTesting("He is a man? I'm not sure what you mean. My name's Brad!"),
            "He is a man?\n My name's Brad!\n"
        )

        self.assertEqual(
            getGenderedDatasetTesting("I like ACTORS!! I don't like hers."),
            "I like ACTORS!\n I don't like hers.\n"
        )

        self.assertEqual(
            getGenderedDatasetTesting("I like ACTORS!!!!!! I don't like hers."),
            "I like ACTORS!\n I don't like hers.\n"
        )

    def test_genderswapQASRL(self):
        curr_file_path = 'Testing/TestInputs/QASRL_testfile_1.txt'
        if not os.path.isfile(curr_file_path):
            os.makedirs(os.path.dirname(curr_file_path), exist_ok=True)

        # write our test stuff to the file
        curr_file = open(curr_file_path, 'w')
        curr_file.write("PROPBANK_57	1\n"
                        + "His recent appearance at the Metropolitan Museum , dubbed `` A Musical Odyssey , '' was a case in point .\n"
                        + "8	dubbed	2\n"
                        + "what	was	something	dubbed	_	_	_	?	A Musical Odyssey\n"
                        + "what	was	_	dubbed	_	_	_	?	His recent appearance at the Metropolitan Museum")

        genderswapQASRL(curr_file_path, 'TestOutputs/answer_file_1.txt')
        out_file = open('TestOutputs/answer_file_1.txt', 'r')
        self.assertEqual(
            out_file.read(),
            "PROPBANK_57	1\n"
            + "Her recent appearance at the Metropolitan Museum , dubbed `` A Musical Odyssey , '' was a case in point .\n"
            + "8	dubbed	2\n"
            + "what	was	something	dubbed	_	_	_	?	A Musical Odyssey\n"
            + "what	was	_	dubbed	_	_	_	?	Her recent appearance at the Metropolitan Museum"
        )



if __name__ == '__main__':
    unittest.main()
