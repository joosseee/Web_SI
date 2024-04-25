from models.entities.User import User
class ModelUser():

    @classmethod
    def login(self, db, user):
        try:
            cursor = db.cursor()
            sql = """SELECT username, hash_password FROM users 
                    WHERE username = '{}'""".format(user.username)
            cursor.execute(sql)
            row = cursor.fetchone()
            if row != None:
                print(user.password)
                user = User(row[0],None,User.check_password(row[1], user.password))
                print(user.password)
                return user
            else:
                return None
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def get_by_username(self, db, username):
        try:
            cursor = db.cursor()
            sql = "SELECT username,tel_number,hash_password,province,permission,emails_total,emails_phising,emails_clicked FROM users WHERE username = ?"
            cursor.execute(sql,(username,))
            row = cursor.fetchone()
            if row != None:
                return User(row[0],row[1],None,row[3],row[4],row[5],row[6],row[7])
            else:
                return None
        except Exception as ex:
            raise Exception(ex)

