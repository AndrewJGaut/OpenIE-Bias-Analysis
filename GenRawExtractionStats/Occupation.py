'''
The following class stores and Occupation with the name of the occupation, its frequency co-occuring with males, and its frequency co-occuring with females
'''

class Occupation:
    def __init__(self, occupation):
        self.occupation = occupation
        self.male_freq = 0
        self.female_freq = 0
        self.total_freq = 0
        self.diff = 0

    def incr_male_freq(self):
        self.male_freq += 1

    def incr_female_freq(self):
        self.female_freq += 1

    def incr_total_freq(self):
        self.total_freq += 1

    def get_male_freq(self):
        return self.male_freq

    def get_female_freq(self):
        return self.female_freq

    def get_total_freq(self):
        return self.total_freq

    def get_occupation(self):
        return self.occupation

    def difference(self, male_tot, female_tot):
        self.diff = abs(float(self.male_freq / male_tot) - float(self.female_freq / female_tot))

    def __eq__(self, other):
        return self.occupation == other

    '''
    def __lt__(self, other):
        return self.occupation < other.occupation
    '''

    def __lt__(self, other):
        return self.diff < other.diff

    def __str__(self):
        return "{}: {}".format(self.occupation, self.diff)
    def __repr__(self):
        return "{}: {}".format(self.occupation, self.diff)