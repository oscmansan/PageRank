#!/usr/bin/python

from collections import namedtuple
import time
import sys

class Edge:
    def __init__ (self, origin=None):

        self.origin = origin
        self.weight = 0


    def __repr__(self):
        return "edge: {0} {1}".format(self.origin, self.weight)

    ## write rest of code that you need for this class

class Airport:
    def __init__ (self, iden=None, name=None):
        self.code = iden
        self.name = name
        self.routes = []
        self.routeHash = dict()
        self.outweight = 0

    def __repr__(self):
        return "{0}\t{2}\t{1}".format(self.code, self.name, self.pageIndex)

edgeList = [] # list of Edge
edgeHash = dict() # hash of edge to ease the match
airportList = [] # list of Airport
airportHash = dict() # hash key IATA code -> ID (AKA OpenFlights Identifier)
P = []

def readAirports(fd):
    print "Reading Airport file from {0}".format(fd)
    airportsTxt = open(fd, "r");
    cont = 0
    for line in airportsTxt.readlines():
        a = Airport()
        try:
            temp = line.split(',')
            if len(temp[4]) != 5 :
                raise Exception('not an IATA code')
            a.name=temp[1][1:-1] + ", " + temp[3][1:-1]
            a.code=temp[4][1:-1]
        except Exception as inst:
            pass
        else:
            cont += 1
            airportList.append(a)
            airportHash[a.code] = len(airportList)-1
    airportsTxt.close()
    print "There were {0} Airports with IATA code".format(cont)


def readRoutes(fd):
    print "Reading Routes file from {0}".format(fd)
    routesTxt = open(fd, "r")
    cont = 0
    for line in routesTxt.readlines():
        try:
            temp = line.split(',')
            #print temp
            if len(temp[2]) != 3 :
                raise Exception('not an IATA code')
            if len(temp[4]) != 3 :
                raise Exception('not an IATA code')
            #Obtenir aeroport origen amb codi IATA

            o_code=temp[2]
            if o_code in airportHash:
                pass
            else:
                raise Exception('not airport found')

            id_o=airportHash[o_code]
            o_airport = airportList[id_o]
            #Obtenir aeroport final amb codi IATA

            d_code=temp[4]
            if d_code in airportHash:
                pass
            else:
                raise Exception('not airport found')
            id_d=airportHash[d_code]
            d_airport=airportList[id_d]

            #Comprobar si existeix Edge
            edge = None
            if o_code in d_airport.routesHash:
                #Si existeix,
                edge = d_airport.routesHash[o_code]
                d_airport.routesHash[o_code].weight += 1
            else:
                #Si no, afegim eix i inicialitzem
                edge = Edge(id_o)
            #En aquest punt, tenim segur un Edge
            #Afegim la ruta a la llista de aeroport final
            d_airport.routes.append(edge)
            d_airport.routeHash[o_code] = edge
            #Afegim eix a llista global
            edgeList.append(edge)
            edgeHash[o_code+","+d_code] = edge
            #Augmentar outweight (rutes sortints) de aeroport origen
            o_airport.outweight += 1
        except Exception as inst:
            pass
        else:
            #Incrementem comptador
            cont += 1
            print "Imma here"
    routesTxt.close()
    print "There were {0} Routes with IATA code".format(cont)

def checkStoppingCondition(A, B):
    th = 0.0001
    diff = map(lambda (a,b): abs(a-b), zip(A,B))
    return all(map(lambda x: x < th, diff))

def computePageRanks():
    n = len(airportList)
    P = [1./n]*n
    L = 0.85
    stopping_condition = False

    iterations = 0;
    while not stopping_condition:
        Q = [0.]*n
        for i in range(n):
            a = airportList[i]
            sum = 0
            for r in a.routes:
                w = r.weight
                j = r.origin
                out = airportList[j].outweight
                sum += P[j] * w / out
            Q[i] = L*sum + (1-L)/n

        stopping_condition = checkStoppingCondition(P,Q)
        P = Q
        iterations += 1

    return iterations


def outputPageRanks():
    l = []
    for i,p in enumerate(P):
        l.append((p,airportList[i].name))
    print l

def main(argv=None):
    readAirports("airports.txt")
    readRoutes("routes.txt")
    time1 = time.time()
    iterations = computePageRanks()
    time2 = time.time()
    outputPageRanks()
    print "#Iterations:", iterations
    print "Time of computePageRanks():", time2-time1


if __name__ == "__main__":
    sys.exit(main())
