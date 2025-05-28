from database.DB_connect import DBConnect
from model.team import Team

class DAO():
    @staticmethod
    def getAllYears():
        conn = DBConnect.get_connection()

        result = []
        cursor = conn.cursor(dictionary=True)

        query = """select DISTINCT (year) 
                    from teams t 
                    where year  >= 1980
                    order by year desc"""

        cursor.execute(query)
        for row in cursor:
            result.append(row["year"])


        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getTeamsOfYear(year):
        conn = DBConnect.get_connection()

        result = []
        cursor = conn.cursor(dictionary=True)

        query = """select *
                    from teams t 
                    where t.`year` = %s"""

        cursor.execute(query, (year,))
        for row in cursor:
            result.append(Team(**row))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getSalaryofTeams(year, idMap):
        conn = DBConnect.get_connection()

        result = []
        cursor = conn.cursor(dictionary=True)

        query = """select t.teamCode,t.ID, SUM(s.salary) as totSalary
                    FROM salaries s, teams t, appearances a
                    WHERE s.`year` = t.`year` and t.`year` = a.`year` and a.`year` = %s
                    and t.ID = a.teamID and s.playerID = a.playerID  
                    GROUP by t.teamCode """

        cursor.execute(query, (year,))

        results = {}
        for row in cursor:
            results[idMap[row["ID"]]] = row["totSalary"]

        cursor.close()
        conn.close()
        return result
