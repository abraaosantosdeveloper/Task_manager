"""
Database connection utilities
"""
import mysql.connector
from mysql.connector import pooling
from api.utils.config import Config

class Database:
    """Database connection manager with connection pooling"""
    
    _pool = None
    
    @classmethod
    def get_pool(cls):
        """Get or create connection pool"""
        if cls._pool is None:
            try:
                cls._pool = pooling.MySQLConnectionPool(
                    pool_name="task_manager_pool",
                    pool_size=5,
                    **Config.get_db_config()
                )
                print("✅ Database connection pool created successfully")
            except mysql.connector.Error as err:
                print(f"❌ Error creating connection pool: {err}")
                raise
        return cls._pool
    
    @classmethod
    def get_connection(cls):
        """Get a connection from the pool"""
        try:
            pool = cls.get_pool()
            return pool.get_connection()
        except mysql.connector.Error as err:
            print(f"❌ Error getting connection: {err}")
            raise
    
    @classmethod
    def test_connection(cls):
        """Test database connection"""
        try:
            conn = cls.get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT 1")
            result = cursor.fetchone()
            cursor.close()
            conn.close()
            return result is not None
        except Exception as e:
            print(f"❌ Database connection test failed: {e}")
            return False
