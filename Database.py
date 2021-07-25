from sqlite3 import connect


class Database:
    @staticmethod
    def insert(name, national_code, birth_day):
        try:
            my_con = connect('users.db')
            my_cursor = my_con.cursor()
            my_cursor.execute(f"INSERT INTO user(NAME, BIRTH_DAY, NATIONAL_CODE)"
                              f"VALUES('{name}','{birth_day}','{national_code}')")
            my_con.commit()
            my_con.close()
            return True
        except Exception as e:
            print("error:", e)
            return False

    @staticmethod
    def select():
        print('in select func')
        try:
            my_con = connect('users.db')
            my_cursor = my_con.cursor()
            my_cursor.execute("SELECT * FROM user")
            result = my_cursor.fetchall()
            my_con.close()
            return result
        except Exception as e:
            print("error:", e)
            return []

    @staticmethod
    def delete(id):
        try:
            my_con = connect('users.db')
            my_cursor = my_con.cursor()
            my_cursor.execute(f"DELETE FROM user WHERE ID = {id}")
            my_con.commit()
            my_con.close()
            return True
            
        except Exception as e:
            print("error:", e)
            return False