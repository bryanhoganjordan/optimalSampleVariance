import math
import sklearn
import numpy as np
from numpy import dot
from numpy.linalg import norm
import operator

class planetClassifier(object):

    '''
    to be used at the end to recursively determine optimal configuration of planets
    '''

    def planetCombination(self, ranks, length, result):

        #iteratively determine optimal ranking and then return the top-number of hits determined by LENGTH
        if len(set(result)) == length:
            return result
            
        else:
            #pull highest value
            if len(result) == 0:
                result.append(scoreRanks[0][0][0])
                result.append(scoreRanks[0][0][1])

            #find highest value from last item
            lastItem = result[-1]

            #retrieve highest value from last item that isn't in results
            for entry in scoreRanks:

                if entry[0][0] == lastItem and entry[0][1] not in result:
                    result.append(entry[0][1])
                    return self.planetCombination(scoreRanks, 3, result) 


#each key contains a list of values representative of planet's properties
planets = {}

'''
planet list => index_0 = radius-in-km, index_1 = weight-in-kg (strip exponent for example), 
                index_2 = human-population, index_3 = O2-concentration-in-atmosphere-percent, 
                index_4 = gravity-acceleration-in-m/s^2.
'''

planets["Mercury"] = [2440, 3.285, 0, 0.13, 3.59]
planets["Venus"] = [6052, 4.867, 0, 0, 8.87]
planets["Earth"] = [6371, 5.972, 7530000000, 20.95, 9.81]
planets["Mars"] = [3390, 6.39, 0, 0.146, 3.77]
planets["Jupiter"] = [69911, 1.898, 0, 0, 25.95]
planets["Saturn"] = [58232, 5.683, 0, 0, 11.08]
planets["Uranus"] = [25362, 8.681, 0, 0, 10.67]
planets["Neptune"] = [24622, 1.024, 0, 0, 14.07]

planetList = [*planets]

#determine cosineSimilarity for each planet
results = {}

for planet in planetList:

    cosineResults = {}

    for altPlanet in planetList:

        if altPlanet is not planet:

            #determine cosine similarity
            cosineResult = dot(planets[planet], planets[altPlanet])/(norm(planets[planet])*norm(planets[altPlanet]))

            #print(planet + " VS " + altPlanet + "===" + str(cosineResult))
            cosineResults[altPlanet] = cosineResult

    results[planet] = cosineResults

'''
distances between planets
if combination of planets eg. Saturn => Mars is not found in dictionary, flip to Mars => Saturn
'''

distances = {}

distances["Mercury"] = {"Venus": 50.29, "Mars": 170.03, "Earth": 91.69, "Jupiter": 720.42, "Saturn": 1366.69,"Uranus": 2815.64, "Neptune": 4443.09}
distances["Venus"] = {"Mars": 119.74, "Earth": 41.4, "Jupiter": 670.13, "Saturn": 1316.4, "Uranus": 2765.35, "Neptune": 4392.80}
distances["Earth"] = {"Mars": 78.34, "Jupiter": 628.73, "Saturn": 1.275, "Uranus": 2723.95, "Neptune": 4351.4}
distances["Mars"] = {"Jupiter": 550.39, "Saturn": 1196.66, "Uranus": 2645.61, "Neptune": 4273.0}
distances["Jupiter"] = { "Saturn": 646.270, "Uranus": 2095.22, "Neptune": 3722.67}
distances["Saturn"] = {"Uranus": 1448.95, "Neptune": 3076.40}
distances["Uranus"] = {"Neptune": 1627.45}

scoreRanks = []

#iterate throught planets, determine respective score
#score => cosine(Planet - (Planet + 1))/distance

for planet in planetList:

    #retrieve cosine score by iterating through key and value in results dictionary
    for altPlanet, cosineScore in results.items():

        if altPlanet != planet:
            
            if planet in distances:
                
                #retrieve distance
                if altPlanet in distances[planet]:
                    distance = distances[planet][altPlanet]
                
                else:
                    distance = distances[altPlanet][planet]

            if planet not in distances:

                #use altplanet and reverse configuration for distance
                distance = distances[altPlanet][planet]

            #retrieve cosine
            if altPlanet in cosineScore:
                cosine = cosineScore[altPlanet]
            else:
                cosine = results[altPlanet][planet]

            score = float(cosine)/float(distance)

            #print(planet + " VS " + altPlanet + " SCORE === "+ str(score))

            scoreRanks.append([[planet, altPlanet], score])

scoreRanks = sorted(scoreRanks, key=operator.itemgetter(1))

planetWorker = planetClassifier()

#returns recursively determined optimal combination of merchandIds
print(planetWorker.planetCombination(scoreRanks, 3, []))




