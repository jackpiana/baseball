from database.DB_connect import DBConnect
from model.team import Team


class DAO():
    def __init__(self):
        pass

    @staticmethod
    def getter_anni():
        conn = DBConnect.get_connection()
        result = []
        if conn is None:
            print("Connection failed")
        else:
            cursor = conn.cursor()
            query = """select distinct year
                        from teams 
                        where year >= 1980
                        order by year desc"""
            cursor.execute(query)
            for row in cursor:
                result.append(row[0]) #row è una tupla contenente tutti gli attributi selezionati dalla query
            cursor.close()
            conn.close()
        return result

    @staticmethod
    def getter_teams_year(year):
        """
        usa unpacking di dizionari per creare oggetti di classe avente tutte le righe di data tabella
        return: mappa key= id, value= oggetto
        """
        conn = DBConnect.get_connection()
        result = {}
        if conn is None:
            print("Connection failed")
        else:
            cursor = conn.cursor(dictionary=True)
            query = """
            select distinct *
            from teams 
            where year = %s
                        """
            cursor.execute(query, (year,))
            for row in cursor:
                result[row["ID"]] = (Team(**row))  #**row è un operatore di unpacking (espansione) di un dizionario. nb: serve che tutti i nomi degli attributi combacino
            cursor.close()
            conn.close()
        return result

    @staticmethod
    def getter_totSalary_team(teamID, year):
        conn = DBConnect.get_connection()
        result = 0
        if conn is None:
            print("Connection failed")
        else:
            cursor = conn.cursor()
            query = """select s.teamCode, s.teamID, sum(salary)
                        from salaries s
                        where year = %s
                        and teamID = %s
                        group by teamID
"""
            cursor.execute(query, (year, teamID))
            for row in cursor:
                result += row[2]  # row è una tupla contenente tutti gli attributi selezionati dalla query
            cursor.close()
            conn.close()
        return result
