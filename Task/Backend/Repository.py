from datetime import datetime
import mysql.connector
import Repository

class Repository:
    
    def __init__(self):
        self.host = "localhost"
        self.port = 3307
        self.database = "task_manager"
        self.user = "root"
        self.password = ""
        
    def get_connection(self):
        return mysql.connector.connect(
            host=self.host,
            port=self.port,
            user=self.user,
            password=self.password,
            database=self.database
        )

    def execute(self, query, params=None):
        conn = self.get_connection()
        cursor = conn.cursor()
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        conn.commit()
        cursor.close()
        conn.close()

    def add(self, title, description):
        query = "INSERT INTO tasks (title, description) VALUES (%s, %s)"
        self.execute(query, (title, description))

    def get_all(self):
        query = "SELECT * FROM tasks ORDER BY id DESC"
        conn = self.get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(query)
        results = cursor.fetchall()
        cursor.close()
        conn.close()
        return results


    def delete(self, task_id):
        query = "DELETE FROM tasks WHERE id = %s"
        self.execute(query, (task_id,))

    def update_status(self, task_id, status):
        query = "UPDATE tasks SET status = %s WHERE id = %s"
        self.execute(query, (status, task_id))

    def complete(self, task_id):
        query = """
            UPDATE tasks 
            SET status = 'completed', completed_at = %s
            WHERE id = %s
        """
        self.execute(query, (datetime.now(), task_id))