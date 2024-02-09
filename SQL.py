import sqlite3 as sl

con = sl.connect("users.db")


class SQL:
    def __init__(self):
        self
    
    def create_table(self):
        with con:
            data = con.execute("select count(*) from sqlite_master where type='table' and name='users'")
            for row in data:
                if row[0] == 0:
                    with con:
                        con.execute("""
                            CREATE TABLE users (
                            username TEXT,
                            id INTEGER,
                            total INTEGER DEFAULT 0,
                            total_correct INTEGER DEFAULT 0, 
                            total_human INTEGER DEFAULT 0,
                            total_human_correct INTEGER DEFAULT 0,
                            total_economy INTEGER DEFAULT 0,
                            total_economy_correct INTEGER DEFAULT 0,
                            total_policy INTEGER DEFAULT 0,
                            total_policy_correct INTEGER DEFAULT 0,
                            total_law INTEGER DEFAULT 0,
                            total_law_correct INTEGER DEFAULT 0,
                            total_sociology INTEGER DEFAULT 0,
                            total_sociology_correct INTEGER DEFAULT 0,
                            mode INTEGER DEFAULT 0,
                            is_answering INTEGER DEFAULT 0,
                            date DATE DEFAULT (datetime('now','localtime'))
                    );
                """)    
                        
    def add_in_table(self, con, data):
        cursor_obj = con.cursor()
        cursor_obj.execute('SELECT * FROM users WHERE (id=?)', (data[1], ))
        entry = cursor_obj.fetchone()
        if entry is None:
            cursor_obj.execute('INSERT INTO users (username, id) VALUES(?, ?)', data)
            con.commit()
            return True
        else:
            return False
        
    def search_in_table(self, id):
        cursor_obj = con.cursor()
        result = cursor_obj.execute("SELECT * FROM users WHERE id = '%s'" % id).fetchall()
        return result
    
    def change_is_anwering(self, id, a):
        cursor_obj = con.cursor()
        cursor_obj.execute(f"UPDATE users SET is_answering = {a} WHERE id = {id}")
        con.commit()

    
    def update_all_total_in_table(self, id):
        cursor_obj = con.cursor()
        cursor_obj.execute("UPDATE users SET total = total + 1 WHERE id = '%s'" % id)
        con.commit()

    def update_true_data_in_table(self, id):
        cursor_obj = con.cursor()
        cursor_obj.execute("UPDATE users SET total_correct = total_correct + 1 WHERE id = '%s'" % id)
        con.commit()

    def set_mode(self, id, a):
        cursor_obj = con.cursor()
        cursor_obj.execute(f"UPDATE users SET mode = {a} WHERE id = {id}")
        con.commit()

    def get_id(self):
        cursor_obj = con.cursor()
        a = cursor_obj.execute("SELECT id from users").fetchall()
        return a


    def change_totals(self, id, mode):
        cursor_obj = con.cursor()
        if mode == 1:
            cursor_obj.execute(f"UPDATE users SET total_human = total_human + 1 WHERE id = {id}")
            con.commit()
        if mode == 2:
            cursor_obj.execute(f"UPDATE users SET total_economy = total_economy + 1 WHERE id = {id}")
            con.commit()
        if mode == 3:
            cursor_obj.execute(f"UPDATE users SET total_policy = total_policy + 1 WHERE id = {id}")
            con.commit()
        if mode == 4:
            cursor_obj.execute(f"UPDATE users SET total_law = total_law + 1 WHERE id = {id}")
            con.commit()
        if mode == 5:
            cursor_obj.execute(f"UPDATE users SET total_sociology = total_sociology + 1 WHERE id = {id}")
            con.commit()

    def change_totals_correct(self, id, mode):
        cursor_obj = con.cursor()
        if mode == 1:
            cursor_obj.execute(f"UPDATE users SET total_human_correct = total_human_correct + 1 WHERE id = {id}")
            con.commit()
        if mode == 2:
            cursor_obj.execute(f"UPDATE users SET total_economy_correct = total_economy_correct + 1 WHERE id = {id}")
            con.commit()
        if mode == 3:
            cursor_obj.execute(f"UPDATE users SET total_policy_correct = total_policy_correct + 1 WHERE id = {id}")
            con.commit()
        if mode == 4:
            cursor_obj.execute(f"UPDATE users SET total_law_correct = total_law_correct + 1 WHERE id = {id}")
            con.commit()
        if mode == 5:
            cursor_obj.execute(f"UPDATE users SET total_sociology_correct = total_sociology_correct + 1 WHERE id = {id}")
            con.commit()