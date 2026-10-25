import sqlite3 
from contextlib import contextmanager

class database_manager:
    def __init__(self, db_name):
        self.db_name = db_name
    @contextmanager
    def get_connection(self):
        conn = sqlite3.connect(self.db_name)
        try:
            yield conn
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()