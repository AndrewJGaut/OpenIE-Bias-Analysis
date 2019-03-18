'''
This code takes extracted relations and post-processes them so that it's easier to find occupation and gendered words.
Basically:
	all words are stemmed
	all plural words are made singular
	all words are made lowercase
Nothing else is changed.
'''



import nltk
import contractions
import inflect

infl = inflect.engine()

'''
Parameters:
	in_file - input file of extracted relations
	out_file - output file with postprocessed extracted relations
	testing - true if we're testing (and thus reading from and writing to basic strings)
	in_str - only used if we're testing
What it does:
	Read top of file
'''

def normalize(in_file, out_file, testing, in_str):
	if(not testing):
		out_file = open(in_file, "w")
		with open(out_file, "r") as file:
			for line in file.readlines():
				new_line = ""
				words = nltk.word_tokenize(line)
				for word in words:
					if '\'' in word:
						continue
					word = word.lower()
					if (infl.singular_noun(word)):
						word = infl.singular_noun(word)
					if(word[0].isalnum()):
						new_line += " "
					new_line += str(word)
				out_file.write(new_line + "\n")
		out_file.close()
	elif(testing):
		lines = in_str.split('\n')
		out_str = ""
		for line in lines:
			new_line = ""
			words = nltk.word_tokenize(line)
			for word in words:
				if '\'' in word:
					continue
				word = word.lower()
				if(infl.singular_noun(word)):
					word = infl.singular_noun(word)
				if(word[0].isalnum()):
					new_line += " "
				new_line += str(word)
			out_str += new_line + "\n"
		return out_str

if __name__ == '__main__':
	pass
	#normalize("allpostpr_REG_Stanford_extr_rel.txt", "postpr_REG_Stanford_extr_rel.txt", False, "")