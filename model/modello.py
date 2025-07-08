from operator import itemgetter

import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self.grafo = nx.Graph()
        self.bestScore = 0
        self.bestPercorso = []

    def build_graph(self, year):
        self.grafo = None
        self.grafo = nx.Graph()
        nodes = DAO.getter_teams_year(year).values()
        self.grafo.add_nodes_from(nodes)
        for n1 in nodes:
            for n2 in nodes:
                if n1 != n2 and (n1, n2) not in list(self.grafo.edges):
                    salT1 = DAO.getter_totSalary_team(n1.ID, year)
                    salT2 = DAO.getter_totSalary_team(n2.ID, year)
                    w = int(salT1) + int(salT2)
                    self.grafo.add_edge(n1, n2, weight= w)

    def get_dettagli(self, node):
        res = []
        neighbors = list(self.grafo.neighbors(node))
        for neighbor in neighbors:
            res.append((neighbor, self.grafo[node][neighbor]['weight']))
        return res




    def bestPath(self, startNode):
        self.ricorsione([startNode])
        print(self.bestPercorso)

    def ricorsione(self, parziale):
        rimanenti = self.rimanenti(parziale)
        print(rimanenti)
        if rimanenti == []:
            self.calcola_score(parziale)
        else:
            for n in rimanenti:
                parziale = parziale.copy()
                parziale.append(n)
                self.ricorsione(parziale)
                parziale.pop()


    def rimanenti(self, parziale):
        lastNode = parziale[-1]
        vicini = list(self.grafo.neighbors(lastNode))
        rimanenti = []
        for v in vicini:
            if v in parziale:
                continue
            if len(parziale) < 2:
                rimanenti.append(v)
            elif self.grafo[lastNode][v]['weight'] < self.grafo[parziale[-2]][lastNode]['weight']:
                rimanenti.append(v)
        return rimanenti

    def calcola_score(self, parziale):
        score = 0
        for i in range(len(parziale)-1):
            score += self.grafo[parziale[i]][parziale[i+1]]['weight']
        if score > self.bestScore:
            self.bestScore = score
            self.bestPercorso = parziale



if __name__ == "__main__":
    m = Model()
    m.build_graph(2015)
    print(m.grafo)
