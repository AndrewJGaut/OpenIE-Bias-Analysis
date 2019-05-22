'''filepath = 'OpenIE5_REG_extractedrelations.txt'
#filepath = 'test.txt'
with open(filepath) as fp:  
	line = fp.readline()
	wfp = open('output.txt', "w")
	while line:
		if line[0] == '0' or line[0] == '1':
			wfp.write(line)
		line = fp.readline()

	wfp.close()
	fp.close()'''


def filter():
	#occupation_list = ("carpenter", "mechanic", "labourer", "driver", "sheriff", "farmer", "janitor", "lawyer", "physician", "executive", "analyst", "supervisor", "sales assistant", "editor", "accountant", "auditor", "writer", "baker", "clerk", "cashier", "counselor", "attendant", "teacher", "librarian", "assistant", "cleaner", "housekeeper", "nurse", "receptionist", "hairdresser", "secretary")
	
	# for each file, looks at the occupations in this list. change if you want to include different occupations
	occupation_list = ("executive", "governor", "student ", "researcher", "chef", "lawyer", "nurse", "doctor", "reporter", "engineer")
	
	# loops through the files in THIS list
	file_list = ("stanford_REG_male", "stanford_REG_female", "stanford_GS_male", "stanford_GS_female", "openIE5_REG_male", "openIE5_REG_female", "openIE5_GS_male", "openIE5_GS_female")

	readfilepath = '../Results/TEST/OccupationFreqs/'
	writefilepath = '../Results/TEST/OccupationStats/filtered.txt'
	wfp = open(writefilepath, "w")
	#filepath = 'test.txt'
	for filename in file_list:
		total = 0
		readfilepath = '../Results/TEST/OccupationFreqs/'
		readfilepath+=filename + '.txt'

		wfp.write("--------------------------------------------------------\n")
		wfp.write(filename)
		wfp.write("\n--------------------------------------------------------\n\n")

		for i in range(len(occupation_list)):
			with open(readfilepath) as rfp:  
				line = rfp.readline()
				while line:
					if line.find(occupation_list[i]) == 0:
						total+=int(line[line.find('-')+2:len(line)-1])
					line = rfp.readline()

		for i in range(len(occupation_list)):
			with open(readfilepath) as rfp:  
				line = rfp.readline()
				while line:
					if line.find(occupation_list[i]) == 0:
						wfp.write(line[:line.find('-')-1] + ' - ' + str(float(line[line.find('-')+1:])/total) + ' \n')
					line = rfp.readline()
			rfp.close()
		wfp.write("\n\n")
	wfp.close()


if __name__ == '__main__':
    filter()