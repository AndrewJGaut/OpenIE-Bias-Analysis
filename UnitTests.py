import unittest
import sys

# we need these sys.path alterations so we can import files that aren't in the exact same directory as this UnitTests file
sys.path.insert(0, '/Users/agaut/PycharmProjects/OpenIEBias/AlterDataset/GenderSwapping/')
sys.path.insert(0, '/Users/agaut/PycharmProjects/OpenIEBias/PostProcessExtractions/PostProcessExtractionsNormalize')
sys.path.insert(0, '/Users/agaut/PycharmProjects/OpenIEBias/AlterDataset/FilterGenderedSentences')
from genderSwap import *
from Normalize import *
from filterGendered import *

class TestGenderSwap(unittest.TestCase):
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

    def test_genderSwapNames(self):
        pass
        #this is hard to test because you'd have to manually average out the name counts to check if it's running correclty

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

if __name__ == '__main__':
    unittest.main()