# -*- coding: utf-8 -*-

from math import *
import sys
import random
import operator
import numpy as np
import matplotlib.pyplot as plt
import re
from imageprocessing_functions import *
from move_function import *


################################################################
##############################INIT##############################
################################################################

DEBUG = True
white = 0xffffff; red = 0xff5f5f; green = 0x42ecec; blue = 0x0000ff; black = 0x000000

sensibility = (20, 20, 20)
exit = False;get_color = False
a = 0; b = 0;
target_pos = (0,0)

display_width = 1280; display_height = 720

#################################################################
############################FUNCTIONS############################
#################################################################
"""
take a snake (amplitude, offset), processes it and gives it's score

The score function must also write the performance of the snake in a file
"""

def evaluate(snake, display_window, cam, display_width, display_height, sensibility = (20,20,20), pixel_distance_to_go = 637):

	#score = sqrt(pow(snake[0]-300,2)) + sqrt(pow(snake[1] - 512, 2))
	#return(int(score))
	print("Evaluation de l'individu")
	print(snake)

	init_snake(id_bloque = 10, angle_bloque = 700, amplitude = snake[0], offset = snake[1])
	a, b, target = getTargetLocation(display_window, sensibility, cam, display_width, display_height, pixel_distance_to_go)

	move_snake(id_bloque = 10, amplitude = snake[0], offset  = snake[1])

	score = getScore(target, a, b, sensibility, display_window, cam, display_width, display_height)

	return(score)


"""
Generate a random amplitude and offset that compose a snake

@returns amplitude, offset
"""
def generateSnake():
	amplitude = randint(200,350)
	offset = randint(460,564)

	return(amplitude, offset)

"""
Generates a population of size sizePopulation and returns it in a list
"""
def generateFirstPopulation(sizePopulation):
	population = []
	i = 0
	while i < sizePopulation:
		population.append(generateSnake())
		i+=1

	return population

"""
Test every Snake of the population to give them a score and sort
the population by increasing order
"""

def computePerfGeneration(population, display_window, cam, display_width, display_height):
	populationPerf = {}
	compteur = 0;
	for snake in population:
		populationPerf[snake] = evaluate(snake, display_window, cam, display_width, display_height)
		compteur += 1;
		print('Individu :', compteur)
	return sorted(populationPerf.items(), key = operator.itemgetter(1))


"""
Select the (int) "best_sample" snakes from the sorted population and some few lucky snakes randomly
(lucky_few selected randomly)
"""
def selectFromPopulation(populationSorted, best_sample, lucky_few):
	nextGeneration = []
	for i in range(best_sample):
		nextGeneration.append(populationSorted[i][0])
	for i in range(lucky_few):
		nextGeneration.append(choice(populationSorted)[0])
	shuffle(nextGeneration)

	return nextGeneration


"""
Hybrids the two snake parents in order to create a child
"""
def createChild(individual1, individual2):
	"""
	Possible solution :
		Amplitude = mean of their amplitude
		Offset = mean of their offset

	Should we ponderate by their score ?
	How to add some randomness ? => Ponderated randomly thanks to a gaussian ?
		gaussian with varian = score ?
	"""
	pond_amplitude = random()
	pond_offset = random()
	amplitude = pond_amplitude * individual1[0] + (1-pond_amplitude) * individual2[0]
	offset = pond_offset * individual1[1] + (1 - pond_offset) * individual2[1]

	child = (int(amplitude), int(offset))

	return child


"""
Create number_of_child children from the breeders generation
number_of_child is the number of children for a given couple. len(breeders)/2 couples are created
"""
def createChildren(breeders, children_per_couple):
	nextPopulation = []
	for i in range(int(len(breeders)/2)):
		for j in range(children_per_couple):
			nextPopulation.append(createChild(breeders[i], breeders[len(breeders) -1 -i]))

	return nextPopulation

"""
Randomly mutates the values of a snake
"""
def mutateSnake(snake, modification_variance):

	item_modified = randint(0,1) #Either modify amplitude or offset
	# Modify it randomly AROUND it's value following a gaussian
	mutation = gauss(snake[item_modified], modification_variance[item_modified])
	if (item_modified == 0):
	 	return(int(mutation), snake[1])
	return (snake[0], int(mutation))

"""
Randomly mutates the population given with a probability chance_of_mutation
"""
def mutatePopulation(population, chance_of_mutation, modification_variance = [5,	5]):
	for i in range(len(population)):
		if random() < chance_of_mutation:
			population[i] = mutateSnake(population[i], modification_variance)

	return population

"""
Check individual for unexpected values
"""

def checkSnake(snake, MIN_AMPLITUDE = 200, MAX_AMPLITUDE = 500, MIN_OFFSET = 460, MAX_OFFSET = 564):
	amplitude, offset = snake
	if (amplitude < MIN_AMPLITUDE):
		amplitude = MIN_AMPLITUDE
	elif (amplitude > MAX_AMPLITUDE):
		amplitude = MAX_AMPLITUDE
	if (offset < MIN_OFFSET):
		offset = MIN_OFFSET
	elif (offset > MAX_OFFSET):
		offset = MAX_OFFSET

	return(amplitude, offset)
"""
Check population for unexpected values
"""
def checkPopulation(population, MIN_AMPLITUDE = 200, MAX_AMPLITUDE = 500, MIN_OFFSET = 460, MAX_OFFSET = 564):
	for i in range(len(population)) :
		population[i] = checkSnake(population[i])

	return population


"""
Saves a generation in the file file_name
"""
def saveGeneration(sorted_population, generation_index):
	gen = "Generation_" + str(generation_index+1) + ".txt"
	file = open(gen, "a+")
	for i in range(len(sorted_population)):
		snake = str(sorted_population[i][0][0]) + ';' + str(sorted_population[i][0][1]) + ';' + str(sorted_population[i][1]) + '\n'
		file.write(snake)
	file.close()

def meanVarScore(populationWithScore, mean, var):
	scores = [snake[1] for snake in populationWithScore]

	mean.append(np.mean(scores))
	var.append(np.var(scores)/2)

# Main

def genetic_algorithm(populationSize, number_of_generations, best_sample, lucky_few, children_per_couple, chance_of_mutation, display_window, cam, display_width, display_height):
	mean = []
	var = []

	pop = generateFirstPopulation(populationSize)

	for generation in range(number_of_generations):
		print("Generation no : " + str(generation+1))

		perf = computePerfGeneration(pop, display_window, cam, display_width, display_height)

		saveGeneration(perf, generation)
		meanVarScore(perf, mean, var)#Saving mean and var

		sample = selectFromPopulation(perf, best_sample, lucky_few)

		pop = createChildren(sample, children_per_couple)
		pop = mutatePopulation(pop, chance_of_mutation)
		pop = checkPopulation(pop)

	return mean,var

"""
Load the generation from the file "save" ad continue the genetic processing from there
"""
def genetic_algorithm_from_generation(save, loaded_gen_index, number_of_generations, best_sample, lucky_few, children_per_couple, chance_of_mutation, display_window, cam, display_width, display_height):
	mean = []; var = []

	#Loading generation nb loaded_gen_index from file save
	text_file = open(save, "r")
	lines = text_file.read()
	lines = re.sub(r"\s+$", "", lines)
	lines = re.split('[; \n]',lines)
	print("Generation from "+save+" loaded to this world")
	text_file.close()
	loaded_perf = np.array(lines).reshape(len(lines)/3, 3).tolist()
	perf = np.zeros((len(lines)/3, 2)).tolist()

	for i in range(len(lines)/3):
		perf[i][0] = int(loaded_perf[i][0]), int(loaded_perf[i][1])
		perf[i][1] = int(float(loaded_perf[i][2]))

	print(perf)
	print("Generation", loaded_gen_index, "loaded successfully")

	#meanVarScore(perf, mean, var)#Saving mean and var

	#Generate generation of index loaded_gen_index + 1 
	sample = selectFromPopulation(perf, best_sample, lucky_few)

	pop = createChildren(sample, children_per_couple)
	pop = mutatePopulation(pop, chance_of_mutation)
	pop = checkPopulation(pop)

	print("Generation", loaded_gen_index+1, "hybridised successfully")
	print(pop)
	print('\n')
	#COntinue genetic algorithm process	    

	for generation in range(loaded_gen_index+1, number_of_generations):
		print("Generation no : " + str(generation+1))

		perf = computePerfGeneration(pop, display_window, cam, display_width, display_height)

		saveGeneration(perf, generation)
		meanVarScore(perf, mean, var)#Saving mean and var

		sample = selectFromPopulation(perf, best_sample, lucky_few)

		pop = createChildren(sample, children_per_couple)
		pop = mutatePopulation(pop, chance_of_mutation)
		pop = checkPopulation(pop)

	return mean,var

################################################################
##############################MAIN##############################
################################################################
firstPopulationSize = 20; number_of_generations = 20; best_sample = 6;
lucky_few = 1; children_per_couple = 5;chance_of_mutation = 0.15;
display_window, display_width, display_height, cam = initImage()

#mean, var = genetic_algorithm(firstPopulationSize, number_of_generations, best_sample, lucky_few, children_per_couple, chance_of_mutation, display_window,cam, display_width, display_height)

mean, var = genetic_algorithm_from_generation("Generation_6.txt", 6, number_of_generations, best_sample, lucky_few, children_per_couple, chance_of_mutation, display_window, cam, display_width, display_height)

fig = plt.figure(1)
plt.errorbar(range(len(mean)), mean, var, ecolor = 'red')
plt.xlabel("Generation")
plt.ylabel("Score moyen")
plt.xlim(0,len(mean))
#plt.ylim(-20,30)
plt.grid()

plt.show()
