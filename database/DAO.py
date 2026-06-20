from database.DB_connect import DBConnect
from model.classification import Classification
from model.gene import Gene
from model.interaction import Interaction


class DAO():

    @staticmethod
    def get_all_genes():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """SELECT * 
                        FROM genes"""
            cursor.execute(query)

            for row in cursor:
                result.append(Gene(**row))

            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def get_all_interactions():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """SELECT * 
                           FROM interactions"""
            cursor.execute(query)

            for row in cursor:
                result.append(Interaction(**row))

            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def get_all_classifications():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """SELECT * 
                        FROM classification"""
            cursor.execute(query)

            for row in cursor:
                result.append(Classification(**row))

            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def get_all_locations_desc():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select distinct localization
from classification c
order by localization desc
"""
            cursor.execute(query)

            for row in cursor:
                result.append(row["localization"])

            cursor.close()
            cnx.close()
        return result


    @staticmethod
    def getAllNodes(localization):
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select distinct *
from classification c 
where c.Localization =%s
"""
            cursor.execute(query,(localization,))

            for row in cursor:
                result.append(Classification(**row))

            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def getEdges(localization):
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """select distinct c1.GeneID as idA, c2.GeneID as idB
from classification c1, classification c2, interactions i
where c1.Localization =  %s and c2.Localization = %s
  and c1.GeneID < c2.GeneID
  and (
        (i.GeneID1 = c1.GeneID and i.GeneID2 = c2.GeneID)
     or (i.GeneID1 = c2.GeneID and i.GeneID2 = c1.GeneID))
    """

        cursor.execute(query, (localization, localization))

        for row in cursor:
            results.append(row)

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getPeso(geneID):
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)
        query = """
            select distinct g.GeneID as geneID, g.Chromosome as peso
from  genes g 
where  g.GeneID =%s
        """
        cursor.execute(query, (geneID,))
        res = {row["geneID"]: row["peso"] for row in cursor}
        cursor.close()
        cnx.close()
        return res