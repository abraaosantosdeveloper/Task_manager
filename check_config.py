#!/usr/bin/env python3
"""
Script para validar a configuração do .env antes de iniciar a API
"""
import os
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from dotenv import load_dotenv
import mysql.connector

# Load .env
load_dotenv()

def check_env_file():
    """Check if .env file exists"""
    if not os.path.exists('.env'):
        print("❌ Arquivo .env não encontrado!")
        print("\n💡 Solução:")
        print("   cp .env.example .env")
        print("   nano .env  # Edite com suas credenciais\n")
        return False
    print("✅ Arquivo .env encontrado")
    return True

def check_database_config():
    """Check database configuration"""
    print("\n📋 Verificando configuração do banco de dados...")
    
    db_host = os.getenv('DB_HOST', 'localhost')
    db_port = int(os.getenv('DB_PORT', 3306))
    db_name = os.getenv('DB_NAME', 'task_manager')
    db_user = os.getenv('DB_USER', 'root')
    db_password = os.getenv('DB_PASSWORD', '')
    
    print(f"   Host: {db_host}")
    print(f"   Port: {db_port}")
    print(f"   Database: {db_name}")
    print(f"   User: {db_user}")
    print(f"   Password: {'*' * len(db_password) if db_password else '(vazio)'}")
    
    # Check if password is set
    if not db_password or db_password == 'your_password_here':
        print("\n❌ Senha do banco de dados não configurada!")
        print("\n💡 Solução:")
        print("   1. Abra o arquivo .env")
        print("   2. Altere DB_PASSWORD=your_password_here")
        print("   3. Coloque sua senha do MySQL\n")
        return False
    
    print("✅ Configuração do banco OK")
    return True

def test_database_connection():
    """Test database connection"""
    print("\n🔌 Testando conexão com o banco de dados...")
    
    try:
        conn = mysql.connector.connect(
            host=os.getenv('DB_HOST', 'localhost'),
            port=int(os.getenv('DB_PORT', 3306)),
            database=os.getenv('DB_NAME', 'task_manager'),
            user=os.getenv('DB_USER', 'root'),
            password=os.getenv('DB_PASSWORD', '')
        )
        
        cursor = conn.cursor()
        cursor.execute("SELECT VERSION()")
        version = cursor.fetchone()
        
        print(f"✅ Conexão bem-sucedida! MySQL {version[0]}")
        
        # Check if tables exist
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()
        table_names = [table[0] for table in tables]
        
        print(f"\n📊 Tabelas encontradas: {', '.join(table_names) if table_names else 'nenhuma'}")
        
        if 'users' not in table_names or 'tasks' not in table_names:
            print("\n⚠️  Tabelas necessárias não encontradas!")
            print("\n💡 Solução:")
            print("   mysql -u root -p < database.sql\n")
            return False
        
        print("✅ Todas as tabelas necessárias existem")
        
        cursor.close()
        conn.close()
        return True
        
    except mysql.connector.Error as err:
        if err.errno == 1045:  # Access denied
            print(f"\n❌ Acesso negado ao MySQL!")
            print(f"\n💡 Possíveis causas:")
            print(f"   1. Senha incorreta no .env")
            print(f"   2. Usuário '{os.getenv('DB_USER', 'root')}' não existe")
            print(f"   3. Usuário não tem permissões\n")
            print(f"🔧 Teste manual:")
            print(f"   mysql -u {os.getenv('DB_USER', 'root')} -p\n")
        elif err.errno == 1049:  # Unknown database
            print(f"\n❌ Banco de dados '{os.getenv('DB_NAME', 'task_manager')}' não existe!")
            print(f"\n💡 Solução:")
            print(f"   mysql -u root -p < database.sql\n")
        elif err.errno == 2003:  # Can't connect
            print(f"\n❌ Não foi possível conectar ao MySQL!")
            print(f"\n💡 Verifique se o MySQL está rodando:")
            print(f"   sudo systemctl status mysql")
            print(f"   # ou")
            print(f"   sudo systemctl start mysql\n")
        else:
            print(f"\n❌ Erro ao conectar: {err}\n")
        
        return False

def check_jwt_config():
    """Check JWT configuration"""
    print("\n🔐 Verificando configuração do JWT...")
    
    jwt_secret = os.getenv('JWT_SECRET_KEY', 'default-secret-key-change-in-production')
    
    if jwt_secret == 'default-secret-key-change-in-production' or len(jwt_secret) < 16:
        print("⚠️  JWT_SECRET_KEY fraca ou padrão!")
        print("\n💡 Recomendação:")
        print("   Use uma chave forte (mínimo 32 caracteres)\n")
        return False
    
    print(f"✅ JWT_SECRET_KEY configurada ({len(jwt_secret)} caracteres)")
    return True

def check_cors_config():
    """Check CORS configuration"""
    print("\n🌐 Verificando configuração do CORS...")
    
    cors_origins = os.getenv('CORS_ORIGINS', '*')
    origins = [o.strip() for o in cors_origins.split(',')]
    
    print(f"   Origens permitidas: {len(origins)}")
    for origin in origins:
        print(f"      - {origin}")
    
    if '*' in origins:
        print("⚠️  CORS configurado para aceitar qualquer origem (*)")
        print("   OK para desenvolvimento, mas evite em produção\n")
    
    print("✅ CORS configurado")
    return True

def main():
    """Main validation"""
    print("=" * 60)
    print("🔍 VALIDAÇÃO DA CONFIGURAÇÃO - Task Manager API")
    print("=" * 60)
    
    checks = []
    
    # Check .env file
    checks.append(('env_file', check_env_file()))
    
    if checks[0][1]:  # Only continue if .env exists
        checks.append(('db_config', check_database_config()))
        
        if checks[1][1]:  # Only test connection if config is OK
            checks.append(('db_connection', test_database_connection()))
        
        checks.append(('jwt_config', check_jwt_config()))
        checks.append(('cors_config', check_cors_config()))
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 RESUMO DA VALIDAÇÃO")
    print("=" * 60)
    
    passed = sum(1 for _, status in checks if status)
    total = len(checks)
    
    for check_name, status in checks:
        symbol = "✅" if status else "❌"
        print(f"{symbol} {check_name}")
    
    print(f"\n{passed}/{total} verificações passaram")
    
    if passed == total:
        print("\n🎉 Tudo pronto! Você pode iniciar a API:")
        print("   python index.py\n")
        return 0
    else:
        print("\n⚠️  Corrija os problemas acima antes de iniciar a API\n")
        return 1

if __name__ == '__main__':
    sys.exit(main())
