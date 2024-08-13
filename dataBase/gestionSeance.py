


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

    