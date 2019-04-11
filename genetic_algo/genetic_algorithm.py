from math import *
import sys
import random
import operator

"""
#TODO
take a snake (amplitude, offset), processes it and gives it's score

The score function must also write the performance of the snake in a file
"""

def evaluate(snake):
	#score = random.randint(0,100)
	#fonction(amplitude, offset) min in (300,512)

	score = sqrt(snake[0]^2 + 300) + sqrt(snake[1]^2 + 512)
	return(score)



"""
Generate a random amplitude and offset that compose a snake 

@returns amplitude, offset
"""
def generateSnake():
	amplitude = random.randint(1,600)
	offset = random.randint(0,1023)

	return(amplitude, offset)

"""
Generates a population of size sizePopulation and returns it in a list
"""
def generatePopulation(sizePopulation):
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

def computePerfGeneration(population):
	populationPerf = {}
	for snake in population:
		populationPerf[snake] = evaluate(snake)

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
		nextGeneration.append(random.choice(populationSorted)[0])
	random.shuffle(nextGeneration)
	
	return nextGeneration


"""
Hybrids the two snake parents in order to create a child
"""

def createChild(individual1, individual2):
	#TODO

	"""
	Possible solution : 
		Amplitude = mean of their amplitude 
		Offset = mean of their offset 

	Should we ponderate by their score ?
	How to add some randomness ? => Ponderated randomly thanks to a gaussian ?
		gaussian with varian = score ?
	"""
	pond_amplitude = random.random()
	pond_offset = random.random()
	amplitude = pond_amplitude * individual1[0] + (1-pond_amplitude) * individual2[0]
	offset = pond_offset * individual1[1] + (1 - pond_offset) * individual2[1]
	child = (amplitude, offset)
	
	return child


"""
Create number_of_child children from the breeders generation
"""
def createChildren(breeders, number_of_child):
	nextPopulation = []
	for i in range(len(breeders)/2):
		for j in range(number_of_child):
			nextPopulation.append(createCild(breeders[i], breeders[len(breeders) -1 -i]))
	
	return nextPopulation

"""
Randomly mutates the values of a snake
"""
def mutateSnake(snake):
	modification_variance = [200,100]

	item_modified = random.randint(0,1) #Either modify amplitude or offset
	# Modify it randomly AROUND it's value following a gaussian
	snake[item_modified] = random.gaussian(snake[item_modified], modification_variance)

	return snake
	
"""
Randomly mutates the population given with a probability chance_of_mutation
"""
def mutatePopulation(population, chance_of_mutatsion):
	for i in range(len(population)):
		if random.random() < chance_of_mutation:
			population[i] = mutateSnake(population[i])

	return population

"""
Saves a generation in the file file_name
"""

def saveGeneration(sorted_population, generation_index, file_name):
	file = open(file_name, "w+")
	file.write(strcat("generation ", str(generation_index+1)))
	for i in range(len(sorted_population)):
		f.write("%d, %d, %d\n", sorted_population[0], sorted_population[1], sorted_population[2])

## Main

def genetic_algorithm(populationSize, number_of_generations):

	pop = generatePopulation(populationSize)
	
	for generation in range(number_of_generations):
		print("Generation no : " + generation)
		perf = computePerfGeneration(pop)
		
		#TODO



print(perf)

