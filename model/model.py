import copy
import itertools
import random
import warnings

from database.DAO import DAO
import networkx as nx


class Model:
    def __init__(self):
        self._grafo = nx.Graph()
        self._idMapTeams = {}
        self._allTeams = []
        self._bestPath = []
        self._bestScore = 0


    def getBestPath(self, start):
        self._bestPath = []
        self._bestScore = 0

        parziale = [start]
        vicini = self._grafo.neighbors(start)
        for v in vicini:
            parziale.append(v)
            self._ricorsione(parziale)
            parziale.pop()
        return self._bestPath, self._bestScore


    def getBestPathV2(self, start):
        self._bestPath = []
        self._bestScore = 0

        parziale = [start]
        vicini = self._grafo.neighbors(start)
        viciniTuples = [(v, self._grafo[start][v]["weight"]) for v in vicini]
        viciniTuples.sort(key=lambda x: x[1], reverse=True)

        #for v in vicini:
        parziale.append(viciniTuples[0][0]) #arco piu granfe di cui prendo il nodo
        self._ricorsioneV2(parziale)
        parziale.pop()
        return self._bestPath, self._bestScore


    def _ricorsione(self, parziale):

        # 1. verifico che parzial sia UNA SOLUZIONE e verifico se migliore della best

        if self.score(parziale)>self._bestScore:
            self._bestScore = parziale
            self._bestPath = copy.deepcopy(parziale)



        # 2. verifico se posso aggiungere un nuovo nodo

        # 3. aggiungo nodo e faccio ricorsione

        for v in self._grafo.neighbors(parziale - 1):
            if v not in parziale and self._grafo[parziale[-2]][parziale[-1]]["weight"] > self._grafo[parziale[-1]][v]["weight"]:
                parziale.append(v)
                self._ricorsione(parziale)
                parziale.pop()


    def _ricorsioneV2(self, parziale):


        if self.score(parziale)>self._bestScore:
            self._bestScore = parziale
            self._bestPath = copy.deepcopy(parziale)

        vicini = self._grafo.neighbors(parziale[-1])
        viciniTuples = [(v, self._grafo[parziale[-1]][v]["weight"]) for v in vicini]
        viciniTuples.sort(key=lambda x: x[1], reverse=True)


        for t in viciniTuples:
            if t[0] not in parziale and self._grafo[parziale[-2]][parziale[-1]]["weight"] > t[1]:
                parziale.append(t[0])
                self._ricorsione(parziale)
                parziale.pop()
                return # perchè non ha senso controllare gli archi che pesano meno --> ammazzo l'esplorazione dopo aver aggiunto
                                                                                    # l'arco di cui sono sicuro sia il migliore


    def score(self, listOfNodes):
        if len(listOfNodes)<2:
            warnings.warn("errore ibn score, attesa lista lunga almeno 2. ")

        totPeso = 0
        for i in range(len(listOfNodes)-1):
            totPeso += self._grafo[listOfNodes[i-1][i]["weight"]]

        return totPeso














    def getYears(self):
        return DAO.getAllYears()

    def getTeamsofYear(self, year):
        self._allTeams = DAO.getTeamsOfYear(year)
        for t in self._allTeams:
            self._idMapTeams[t.ID] = t
        return self._allTeams


    def buildGraph(self, year):
        self._grafo.clear()
        if len (self._allTeams) == 0:
            print ("lista squadre vuota")
            return
        self._grafo.add_nodes_from(self._allTeams)

        # for n1 in self._grafo.nodes:
        #     for n2 in self._grafo.nodes:
        #         if n1!=n2:
        #             self._grafo.add_edge(n1, n2)


        # oppure

        myEdges = list(itertools.combinations(self._allTeams, 2))
        self._grafo.add_edges_from(myEdges)
        salariesofTeams = DAO.getSalaryofTeams(year, self._idMapTeams)
        for e in self._grafo.edges():
            self._grafo[e[0]][e[1]]["weight"] = salariesofTeams[e[0]]+salariesofTeams[e[1]]
        # return len(self._grafo.nodes), len(self._grafo.edges)





    def printGraphDetails(self):
        print (f"grafo creato con {len(self._grafo.nodes)} nodi e {len(self._grafo.edges)} archi")


    def getGraphDetails(self):
        return self._grafo.number_of_nodes(), self._grafo.number_of_edges()

    def getNeighborsSorted(self, source):
        vicini = nx.neighbors(self._grafo, source)

        # oppure
        # viciniV1 = self._grafo.neighbors(source)

        viciniTuple = []
        for v in vicini:
            viciniTuple.append((v, self._grafo[source][v]["weight"]))

        viciniTuple.sort(key = lambda x: x[1], reverse = True)
        return viciniTuple


    def getRandomNode(self):
        index = random.randint(0, self._grafo.number_of_nodes()-1)
        return list(self._grafo.nodes[index])

    def getWeightOfPath(self, path):
        pathTuple = [(path[0], 0)]
        for i in range(1, len(path)):
            pathTuple.append((path[i], self._grafo[[path[i]path[i-1]["weight"]]]))









