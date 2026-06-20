import copy
import networkx as nx
from database.DAO import DAO

class Model:
    def __init__(self):
        self._grafo = nx.Graph()
        self._classification = []
        self._idMapClassifications = None


    def get_all_locations_desc(self):
        return DAO.get_all_locations_desc()


    def creaGrafo(self, localization):

        self._grafo.clear()
        self._classification = DAO.getAllNodes(localization)
        self._idMapClassifications = {a.GeneID: a for a in self._classification}
        self._grafo.add_nodes_from(self._classification)


        coppie = DAO.getEdges(localization)

        for c in coppie:
            idA, idB = c["idA"], c["idB"]
            a = self._idMapClassifications[idA]
            b = self._idMapClassifications[idB]
            pesoA= DAO.getPeso(idA).get(idA, 0)
            pesoB = DAO.getPeso(idB).get(idB, 0)
            if pesoA != pesoB:
                peso=pesoA+pesoB
            else:
                peso=pesoB
            self._grafo.add_edge(a, b, weight=peso)



    def getGraphDetails(self):
        return len(self._grafo.nodes), len(self._grafo.edges)

    def getTopArchi(self):
        archi = list(self._grafo.edges(data=True))

        archi_ordinati = sorted(
            archi,
            key=lambda x: x[2]["weight"],
            reverse=False
        )

        return archi_ordinati[:]

    def get_connected_components(self):
        # lista di set di nodi, una per ogni componente connessa
        components = list(nx.connected_components(self._grafo))
        # tieni solo quelle con più di un nodo
        components = [c for c in components if len(c) > 1]
        # ordina per dimensione decrescente
        components.sort(key=len, reverse=True)
        return components
