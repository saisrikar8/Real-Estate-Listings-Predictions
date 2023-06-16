from bs4 import BeautifulSoup
from Graph import SmartGraph2D
import urllib.request, urllib.parse, urllib.error
import re
import sys


class RealEstateListings:
    state = str()
    city = str()
    listings = dict()
    graph = None

    def __init__(self, city, stateAbbrv):
        self.state = stateAbbrv.lower()
        self.city = city.title()
        self.listings = {
            'x': list(),
            'y': list()
        }
        self.getListingsForCity()
        self.graph = SmartGraph2D(self.listings['x'], self.listings['y'], 'Real Estate Listings in ' + self.city[0].upper() + self.city[1:] + ', ' + self.state.upper(), 'Floor Plan Size (in hundreds of sqft)', 'Price in Hundreds of Thousands Of Dollars')
    def getListingsForCity(self):
        url = 'https://mls.foreclosure.com/listing/search.html?ci=' + self.city.lower().replace(' ', '%20') + '&st=' + self.state + '&utm_source=internal&utm_medium=link&utm_campaign=MLS_top_links'
        print(url)
        webpage = urllib.request.urlopen(url)
        soup = BeautifulSoup(webpage, 'html.parser')
        tag = soup('body')[0]
        data = re.findall('\$(.[0-9,]+) EMV.?|(.[0-9,]+) sqft\.', tag.text)
        i = 0
        while i < len(data):
            element = data[i]
            index = i%2
            if element[index] == '':
                data.pop(i)
            i += 1
        x = 0
        if len(data) % 2 != 0:
            data.pop(len(data) - 1)
        print(data)
        while x < len(data):
            price = data[x][0]
            floorPlanSize = data[x + 1][1]
            if floorPlanSize == '' or price == '':
                x += 2
                continue
            if 100000 > int(price.replace(',','')) > 5000000:
                data.pop(x)
                data.pop(x + 1)
                x+=2
                continue
            if int(floorPlanSize.replace(',', '')) > 10000:
                data.pop(x + 1)
                x+=2
                continue
            self.listings['x'].append(int(floorPlanSize.replace(',', ''))/100)
            self.listings['y'].append(int(price.replace(',', ''))/100000)
            x += 2
        print(self.listings)

    def graphListings(self):
        self.graph.scatterPlot('Current Listings')

    def getPricePrediction(self, floorPlanSize):
        wb = self.graph.linearRegression(showResultingLine= True)
        w = wb[0]
        b = wb[1]
        prediction = w*(floorPlanSize/100) + b
        print(wb)
        self.graph.plotPoint(floorPlanSize/100, prediction, 'Predicted Price for a ' + str(floorPlanSize) + ' sqft. house')
        return prediction*100000
    def showListingsGraph(self):
        self.graph.showGraph()



