import mysql.connector as cnx
import bcrypt
class Authentification : 
    def __init__(self,cnx):
        self.cursor=cnx.cursor()
        self.conn=cnx
    def register(self, user):
        if not self.emailExist(user["email"]):
            insert_query = """ 
            INSERT INTO `users`(`nom`, `prenom`, `email`, `password`, `role`) 
            VALUES (%s, %s, %s, %s, %s)      
            """
            try:
                hashed_password =hash_password(user["password"])
                data = (user["nom"], user["prenom"], user["email"], hashed_password.decode('utf-8'), user["role"])
                self.cursor.execute(insert_query, data)
                self.conn.commit()
                return True
            except mysql.connector.Error as err:
                print(f"Erreur lors de l'insertion : {err}")
                self.conn.rollback()
                return False
        else:
            print("Email existe déjà")
            return "emailExiste"

    def auth(self,infoAuth) : 
        print("fkfkf")
        print(infoAuth)
        select_query="Select * from users where email=%s"
        self.cursor.execute(select_query,(infoAuth["email"],))
        user=self.cursor.fetchone()
        resultat={}
        if user is None : # L'utilisateur n'existe pas
            resultat["resultat"]=False
            return resultat
        if bcrypt.checkpw(infoAuth["password"].encode('utf-8'), user[4].encode('utf-8')):
            print("Authentification réussie")
            resultat["resultat"]=True
            resultat["user"]={"id" : user[0],"nom" : user[1],"prenom" : user[2],"email" : user[3],"role" : user[5]}
            return resultat
        else:
            print("Échec de l'authentification")
            resultat["resultat"]=False
            return resultat            
    def emailExist(self,email) : 
        select_query = "SELECT id FROM users WHERE email = %s"
        self.cursor.execute(select_query, (email,))  # Pass the parameter as a tuple
        resultat = self.cursor.fetchone()  # Fetch one result
        while self.cursor.fetchone() is not None: #lire resultat pour eviter erreur (Unread result found)
            pass
        return resultat is not None
def hash_password(password) : 
        salt=bcrypt.gensalt()
        return bcrypt.hashpw(password.encode('utf-8'),salt)
