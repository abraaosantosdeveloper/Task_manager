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
                db_config = Config.get_db_config()
                
                # Check if password is the default placeholder
                if not db_config['password'] or db_config['password'] == 'your_password_here':
                    raise ValueError(
                        "⚠️  Database password not configured!\n"
                        "Please edit the .env file and set DB_PASSWORD with your MySQL password"
                    )
                
                cls._pool = pooling.MySQLConnectionPool(
                    pool_name="task_manager_pool",
                    pool_size=5,
                    **db_config
                )
                print("✅ Database connection pool created successfully")
            except ValueError as err:
                print(f"\n{err}\n")
                raise
            except mysql.connector.Error as err:
                if err.errno == 1045:  # Access denied
                    print(f"\n❌ MySQL Access Denied!")
                    print(f"   User: {db_config.get('user', 'unknown')}")
                    print(f"   Host: {db_config.get('host', 'unknown')}")
                    print(f"   Database: {db_config.get('database', 'unknown')}")
                    print(f"\n💡 Solutions:")
                    print(f"   1. Check your MySQL password in the .env file")
                    print(f"   2. Verify MySQL user exists: mysql -u {db_config.get('user', 'root')} -p")
                    print(f"   3. Grant permissions: GRANT ALL ON {db_config.get('database', 'task_manager')}.* TO '{db_config.get('user', 'root')}'@'localhost';\n")
                else:
                    print(f"❌ Error creating connection pool: {err}")
                raise
        return cls._pool
    
    @classmethod
    def get_connection(cls):
        """Get a connection from the pool"""
        try:
            pool = cls.get_pool()
            return pool.get_connection()
        except ValueError as err:
            # Password not configured - already printed detailed message
            raise
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
