from datetime import datetime
import mysql.connector

class Repository:
    
    def __init__(self):
        self.host = "localhost"
        self.port = 3306
        self.database = "task_manager"
        self.user = "root"
        self.password = ""  # Coloque sua senha aqui
        
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

    def add(self, title, description, status="pending"):
        query = "INSERT INTO tasks (title, description, status) VALUES (%s, %s, %s)"
        self.execute(query, (title, description, status))

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
        query = "UPDATE tasks SET status = 'completed', completed_at = %s WHERE id = %s"
        self.execute(query, (datetime.now(), task_id))

    def update_task(self, task_id, novo_titulo, nova_descricao):
        query = "UPDATE tasks SET title = %s, description = %s WHERE id = %s"
        self.execute(query, (novo_titulo, nova_descricao, task_id))
        return True
