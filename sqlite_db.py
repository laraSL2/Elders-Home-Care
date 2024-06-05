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

    def select_data(self, elder_id=None):
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

    def insert_data(self, elder_id, original_text, llm_output, final_text):
        self.connect_db()
        try:
            query = "INSERT INTO Enhancement (ELDER_ID, ORIGINAL_TEXT, LLM_OUTPUT, FINAL_TEXT) VALUES (?, ?, ?, ?)"
            self.conn.execute(query, (elder_id, original_text, llm_output, final_text))
            self.conn.commit()
            return "done"
        except Exception as ex:
            return str(ex)
        finally:
            if self.conn:
                self.conn.close()
                self.conn = None

    def update_data(self, enhancement_id, original_text, llm_output, final_text):
        self.connect_db()
        try:
            query = "UPDATE Enhancement SET ORIGINAL_TEXT = ?, LLM_OUTPUT = ?, FINAL_TEXT = ? WHERE ID = ?"
            self.conn.execute(query, (original_text, llm_output, final_text, enhancement_id))
            self.conn.commit()
            return "done"
        except Exception as ex:
            return str(ex)
        finally:
            if self.conn:
                self.conn.close()
                self.conn = None

    def delete_data(self, enhancement_id):
        self.connect_db()
        try:
            query = "DELETE FROM Enhancement WHERE ID = ?"
            self.conn.execute(query, (enhancement_id,))
            self.conn.commit()
            return "done"
        except Exception as ex:
            return str(ex)
        finally:
            if self.conn:
                self.conn.close()
                self.conn = None

# Example usage
db = ElderDB('database/elder_db.db')
print(db.select_data('e0001'))
