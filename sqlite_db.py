import sqlite3

class ElderDB:
    def __init__(self, db_name='elder_db.db'):
        self.db_name = db_name
        self.conn = None

    def connect_db(self):
        if self.conn is None:
            try:
                self.conn = sqlite3.connect(self.db_name)
                self.conn.execute('''CREATE TABLE IF NOT EXISTS Enhancement
                     (ID            INTEGER PRIMARY KEY AUTOINCREMENT,
                     ELDER_ID       TEXT    NOT NULL,
                     CREATED_AT     DATETIME DEFAULT CURRENT_TIMESTAMP,
                     ORIGINAL_TEXT  TEXT    NOT NULL,
                     LLM_OUTPUT     TEXT    NOT NULL,
                     FINAL_TEXT     TEXT
                     );''')
            except Exception as ex:
                raise ex

    def read_data(self, elder_id=None):
        self.connect_db()
        try:
            if elder_id is not None:
                query = "SELECT * FROM Enhancement WHERE ELDER_ID = ?"
                cursor = self.conn.execute(query, (elder_id,))
            else:
                query = "SELECT * FROM Enhancement"
                cursor = self.conn.execute(query)
            return cursor.fetchall()
        except Exception as ex:
            return str(ex)
        finally:
            if self.conn:
                self.conn.close()
                self.conn = None

    def update_data(self, id, date_time, elder_id, original_text, llm_output, final_text):
        self.connect_db()
        try:
            query = """
            UPDATE Enhancement 
            SET ELDER_ID = ?, CREATED_AT = ?, ORIGINAL_TEXT = ?, LLM_OUTPUT = ?, FINAL_TEXT = ? 
            WHERE ID = ?
            """
            self.conn.execute(query, (elder_id, date_time, original_text, llm_output, final_text, id))
            self.conn.commit()
            return "done"
        except Exception as ex:
            return str(ex)
        finally:
            if self.conn:
                self.conn.close()
                self.conn = None

    def delete_data(self, id, elder_id):
        self.connect_db()
        try:
            query = "DELETE FROM Enhancement WHERE ID = ? AND ELDER_ID = ?"
            self.conn.execute(query, (id, elder_id))
            self.conn.commit()
            return "done"
        except Exception as ex:
            return str(ex)
        finally:
            if self.conn:
                self.conn.close()
                self.conn = None



import sqlite3

class CarePlanDB:
    def __init__(self, db_name='care_plan.db'):
        self.db_name = db_name
        self.conn = None

    def connect_db(self):
        if self.conn is None:
            try:
                self.conn = sqlite3.connect(self.db_name)
                self.conn.execute('''CREATE TABLE IF NOT EXISTS CarePlan
                     (ID            INTEGER PRIMARY KEY AUTOINCREMENT,
                     ELDER_ID       TEXT    NOT NULL,
                     CREATED_AT     DATETIME DEFAULT CURRENT_TIMESTAMP,
                     CARE_PLAN      TEXT    NOT NULL);''')
            except Exception as ex:
                raise ex

    def read_data(self, elder_id=None):
        self.connect_db()
        try:
            if elder_id is not None:
                query = "SELECT * FROM CarePlan WHERE ELDER_ID = ?"
                cursor = self.conn.execute(query, (elder_id,))
            else:
                query = "SELECT * FROM CarePlan"
                cursor = self.conn.execute(query)
            return cursor.fetchall()
        except Exception as ex:
            return str(ex)
        finally:
            if self.conn:
                self.conn.close()
                self.conn = None

    def insert_data(self, elder_id, care_plan):
        self.connect_db()
        try:
            query = "INSERT INTO CarePlan (ELDER_ID, CARE_PLAN) VALUES (?, ?)"
            self.conn.execute(query, (elder_id, care_plan))
            self.conn.commit()
            return "done"
        except Exception as ex:
            return str(ex)
        finally:
            if self.conn:
                self.conn.close()
                self.conn = None

    def update_data(self, id, elder_id, care_plan):
        self.connect_db()
        try:
            query = """
            UPDATE CarePlan 
            SET ELDER_ID = ?, CARE_PLAN = ? 
            WHERE ID = ?
            """
            self.conn.execute(query, (elder_id, care_plan, id))
            self.conn.commit()
            return "done"
        except Exception as ex:
            return str(ex)
        finally:
            if self.conn:
                self.conn.close()
                self.conn = None

    def delete_data(self, id, elder_id):
        self.connect_db()
        try:
            query = "DELETE FROM CarePlan WHERE ID = ? AND ELDER_ID = ?"
            self.conn.execute(query, (id, elder_id))
            self.conn.commit()
            return "done"
        except Exception as ex:
            return str(ex)
        finally:
            if self.conn:
                self.conn.close()
                self.conn = None


import sqlite3

class CareNoteDB:
    def __init__(self, db_name='care_note.db'):
        self.db_name = db_name
        self.conn = None

    def connect_db(self):
        if self.conn is None:
            try:
                self.conn = sqlite3.connect(self.db_name)
                self.conn.execute('''CREATE TABLE IF NOT EXISTS CareNote
                     (ID            INTEGER PRIMARY KEY AUTOINCREMENT,
                     CREATED_AT     DATETIME DEFAULT CURRENT_TIMESTAMP,
                     CARE_NOTE      TEXT,
                     ORIGINAL_NOTE      TEXT );''')
            except Exception as ex:
                raise ex

    def read_data(self, id=None):
        self.connect_db()
        try:
            if id is not None:
                query = "SELECT * FROM CareNote WHERE ID = ?"
                cursor = self.conn.execute(query, (id,))
            else:
                query = "SELECT * FROM CareNote"
                cursor = self.conn.execute(query)
            return cursor.fetchall()
        except Exception as ex:
            return str(ex)
        finally:
            if self.conn:
                self.conn.close()
                self.conn = None

    def insert_data(self, care_note, original_note):
        self.connect_db()
        try:
            query = "INSERT INTO CareNote (CARE_NOTE,ORIGINAL_NOTE) VALUES (?,?)"
            self.conn.execute(query, (care_note,original_note))
            self.conn.commit()
            return "done"
        except Exception as ex:
            return str(ex)
        finally:
            if self.conn:
                self.conn.close()
                self.conn = None

    def update_data(self, id, care_note, original_note):
        self.connect_db()
        try:
            query = """
            UPDATE CareNote 
            SET CARE_NOTE = ? , ORIGINAL_NOTE = ?
            WHERE ID = ?
            """
            self.conn.execute(query, (care_note,original_note, id))
            self.conn.commit()
            return "done"
        except Exception as ex:
            return str(ex)
        finally:
            if self.conn:
                self.conn.close()
                self.conn = None

    def delete_data(self, id):
        self.connect_db()
        try:
            query = "DELETE FROM CareNote WHERE ID = ?"
            self.conn.execute(query, (id,))
            self.conn.commit()
            return "done"
        except Exception as ex:
            return str(ex)
        finally:
            if self.conn:
                self.conn.close()
                self.conn = None
