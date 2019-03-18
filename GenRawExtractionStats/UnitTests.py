import unittest
from GetOccupationFreqs import *

class Tests(unittest.TestCase):
    def test_occupationFreqs(self):
        self.assertEqual(
            testOccupationFreqs("he; is; nurse\nshe;is;doctor"),
            "doctor - 0\nnurse - 1\n\ndoctor - 1\nnurse - 0\n"
        )

        self.assertEqual(
            testOccupationFreqs("he; is; nurse\n"
                                + "she;is;doctor\n"
                                + "as a queen, she; likes; her secretary\n"
                                + "the king and queen both; like; their secretary"),
            "doctor - 0\n"
            + "nurse - 1\n"
            + "secretary - 1\n\n"
            + "doctor - 1\n"
            + "nurse - 0\n"
            + "secretary - 2\n"
        )

        self.assertEqual(
            testOccupationFreqs("he; is; a nurse, and he likes nurses\n"
                                + "she;is; doctor and doctors are very cool\n"
                                + "as a queen, she; likes; her secretary\n"
                                + "the king and queen both; like; their secretary"),
            "doctor - 0\n"
            + "nurse - 1\n"
            + "secretary - 1\n\n"
            + "doctor - 1\n"
            + "nurse - 0\n"
            + "secretary - 2\n"
        )




if __name__ == '__main__':
    unittest.main()