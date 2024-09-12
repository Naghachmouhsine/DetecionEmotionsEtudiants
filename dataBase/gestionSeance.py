import pandas as pd
class GestionSeance : 
    def __init__(self,cnx) : 
        self.conn=cnx
        self.cursor=cnx.cursor()
    def insertSeance(self,seance) : 
        insert_query="""
        INSERT INTO seances 
        (`dateSeance`, `module`, `prcAnger`, `prcDisgust`, `prcFear`, `prcHappiness`, `prcNeutral`, `prcSadness`, `prcSurprise`, `user_id`) 
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);
        """
        print(seance)
        try:
            data = (seance["dataSeance"],seance["module"],seance["emotion"]["anger"],seance["emotion"]["disgust"],seance["emotion"]["fear"],seance["emotion"]["happiness"],seance["emotion"]["neutral"],seance["emotion"]["sadness"],seance["emotion"]["surprise"],seance["user_id"])
            self.cursor.execute(insert_query, data)
            self.conn.commit()
            return True
        except mysql.connector.Error as err:
            print(f"Erreur lors de l'insertion : {err}")
            self.conn.rollback()
            return False
    def getStatistique(self) : 
        select_query=""" 
                    SELECT module,AVG(prcAnger),AVG(prcDisgust),AVG(prcFear),
                    AVG(prcHappiness),AVG(prcNeutral),AVG(prcSadness),AVG(prcSurprise)
                    FROM seances
                    GROUP BY module;
                    """
        self.cursor.execute(select_query)
        resultat=self.cursor.fetchall()
        return resultat
    def getStatistique2(self) : 
        select_query=""" 
        SELECT module,dateSeance,
        (((prcHappiness+prcNeutral)-(prcAnger+prcDisgust+prcFear+prcSadness+prcSurprise))/100) as indiceSatisfaction  
        FROM seances 
        ORDER BY module,dateSeance;
        """
        df=pd.read_sql(select_query,self.conn)
        df["numSeance"]=df.groupby("module").cumcount() +1
        resultat=df.groupby("module").apply(lambda x : x[["numSeance","indiceSatisfaction"]].to_dict(orient="list")).to_dict()
        return resultat



            

    