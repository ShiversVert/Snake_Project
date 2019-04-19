import numpy as np
import matplotlib.pyplot as plt
import re
import sys
from matplotlib.mlab import griddata

def load_gen(file_name, gen_index, make_tuple = False):

	text_file = open(file_name, "r")
	lines = text_file.read()
	lines = re.sub(r"\s+$", "", lines)
	lines = re.split('[; \n]',lines)
	print("Generation from "+file_name+" loaded to this world")
	text_file.close()
	loaded_perf = np.array(lines).reshape(len(lines)/3, 3).tolist()
	print(loaded_perf)
	print(loaded_perf[0][2])
	if make_tuple == True:		
		perf = np.zeros((len(lines)/3, 2)).tolist()

		for i in range(len(lines)/3):
			perf[i][0] = int(loaded_perf[i][0]), int(loaded_perf[i][1])
			perf[i][1] = int(float(loaded_perf[i][2]))

	else: 
		perf = np.zeros((len(lines)/3, 3)).tolist()		

		for i in range(len(lines)/3):
			perf[i][0] = int(loaded_perf[i][0])
			perf[i][1] = int(loaded_perf[i][1])
			print(loaded_perf[i][2])
			if (loaded_perf[i][2] == '9223372036854775807'):
				perf[i][2] = 5000
			else:
				perf[i][2] = int(float(loaded_perf[i][2]))

	print("Generation", gen_index, "loaded successfully")
	return perf

def load_all_gen(name, nb_of_gen, extension ='.txt'):
	generations = []
	for index in range(1,nb_of_gen+1):
		file_name = name + str(index) + extension
		generations.append(load_gen(file_name, index))

	return generations

def display_all(generations, nb_of_gen):
	mean =  []; var = []
	for i in range(nb_of_gen):
		current_gen = generations[i]
		print(current_gen)
		amplitude = np.array(current_gen)[:,0]#.tolist()
		offset = np.array(current_gen)[:,1]#.tolist()
		score = np.array(current_gen)[:,2]#.tolist()

		plt.figure(i)
		
		plt.subplot(2,1,1)
		plt.plot(offset, score, 'x')
		plt.subplot(2,1,2)
		plt.plot(amplitude, score, 'x')
		
	plt.show()
#######################################################
#######################MAIN############################
#######################################################

generations = load_all_gen('Generation_', 9)
display_all(generations,9)