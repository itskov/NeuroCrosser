from pyramid.view import (
    view_config,
    view_defaults,
    )

from pyramid.response import Response

# Importing pickle to load the data into the session.
import pickle

import os
import json
import numpy as np

import logging




@view_defaults(route_name='hello')
class MainViews(object):
    def __init__(self, request):
        self.request = request
        self.view_name = 'MainViews'

        # Initializing logger
        import logging
        logging.info('Starting Session.')

	# Checking if the session should be initialized, and intialize it 
	# if required.
        if ('geneDict' not in self.request.session):
            with open('./MainApp/data/geneDictionary','rb') as f:
                self.request.session['geneDict'] = pickle.load(f)

        if ('cellGeneDict' not in self.request.session):
            with open('./MainApp/data/cellGeneDictionary', 'rb') as f:
                cellGeneDictionary = pickle.load(f)

                # Removing problematic cell names
                notNeurons = [(not key.isupper()) for key in cellGeneDictionary.keys()]
                notNeuronsNames = np.asarray(list(cellGeneDictionary.keys()))[np.asarray(notNeurons)]
                list(map(lambda x: cellGeneDictionary.pop(x, None), notNeuronsNames))

                self.request.session['cellGeneDict'] = cellGeneDictionary





	# Initializing the data once into the session.

    @view_config(route_name='home', renderer='home.pt')
    def home(self):
        return {}

    @view_config(route_name='fetchGO', renderer="json")
    def fetchGO(self):
        global logger;

        geneName = self.request.text;
        geneDict = self.request.session['geneDict'];

        #print("Requesting GO for: " + geneName);
        logging.info("Requesting GO for: " + geneName)

	# Going over the different categories.
        allGos = [];	
        categories = list(geneDict[geneName].values());
        for i in range(0,len(categories)):
            allGos = allGos + categories[i]

        allGos = [tuple(l) for l in allGos];
        allGos = list(set(allGos));
        allDictJSON = [{'Name' : go[1],'GOId' : go[0]} for go in allGos]

        #print(allGos);
        return(allDictJSON);

    @view_config(route_name='overlappingGenes', renderer="json")	
    def overlappingGenes(self):
        #print(json.loads(self.request.text))
        cellGeneDictionary = self.request.session['cellGeneDict']
	
        cellGeneDict = self.request.session['cellGeneDict']
        

        cellList = json.loads(self.request.text)
        
        if (len(cellList) == 0):
            return [];

        cellList = [list(dic.values())[0] for dic in cellList]
        print(cellList)
        logging.info('Cells:' + str(cellList))
        
	
        # All genes of the requested neurons
        allGenes = [set(cellGeneDictionary.get(cellName,'')) for cellName in cellList]
	
        currentIntersect = allGenes[0]
        for i in range(1,len(allGenes)):
            currentIntersect = allGenes[i].intersection(currentIntersect)

        returnList = []

        for gene in currentIntersect:
	    # We have to iterate over all cells and see where this gene appears.
            currentAlsoIn = []

            for key in cellGeneDict.keys():
                if (gene in cellGeneDictionary[key]):
                    if (key not in cellList):
                        currentAlsoIn.append(key)
	
            returnList.append({'Name' : gene, 'AlsoIn' : ", ".join(currentAlsoIn)})

        returnList = sorted(returnList, key = lambda x: len(x.values()[0].split(", ")))
        #print("Here:" + "   " + str([(list(x.values())[0]) for x in returnList]));
        #print((returnList[1].values()[0].split(",")))
        
        

        #print("Return List: " + str(returnList))
	
        if (len(returnList) > 0):	
            return returnList
        else:
            return('[]');
	
	

    

