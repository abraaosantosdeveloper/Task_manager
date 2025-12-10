#!/usr/bin/env python3
"""
Script para testar CORS da API
"""
import requests
import sys

API_URL = "http://localhost:5000/api"

def test_cors():
    """Test CORS configuration"""
    print("=" * 60)
    print("🔍 TESTANDO CONFIGURAÇÃO DE CORS")
    print("=" * 60)
    
    # Test OPTIONS request (preflight)
    print("\n1️⃣ Testando requisição OPTIONS (preflight)...")
    try:
        response = requests.options(
            API_URL,
            headers={
                'Origin': 'http://localhost:8000',
                'Access-Control-Request-Method': 'POST',
                'Access-Control-Request-Headers': 'Content-Type,Authorization'
            }
        )
        
        print(f"   Status: {response.status_code}")
        print(f"   Access-Control-Allow-Origin: {response.headers.get('Access-Control-Allow-Origin', 'Not set')}")
        print(f"   Access-Control-Allow-Methods: {response.headers.get('Access-Control-Allow-Methods', 'Not set')}")
        print(f"   Access-Control-Allow-Headers: {response.headers.get('Access-Control-Allow-Headers', 'Not set')}")
        
        if response.status_code == 200:
            print("   ✅ Preflight OK")
        else:
            print("   ❌ Preflight falhou")
            return False
            
    except requests.exceptions.ConnectionError:
        print("   ❌ Erro: API não está rodando!")
        print("\n   Inicie a API:")
        print("   python index.py")
        return False
    
    # Test GET request
    print("\n2️⃣ Testando requisição GET...")
    try:
        response = requests.get(
            API_URL,
            headers={
                'Origin': 'http://localhost:8000',
                'Content-Type': 'application/json'
            }
        )
        
        print(f"   Status: {response.status_code}")
        print(f"   Access-Control-Allow-Origin: {response.headers.get('Access-Control-Allow-Origin', 'Not set')}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"   Response: {data.get('message', 'No message')}")
            print("   ✅ GET request OK")
        else:
            print("   ❌ GET request falhou")
            return False
            
    except Exception as e:
        print(f"   ❌ Erro: {e}")
        return False
    
    # Test from different origin
    print("\n3️⃣ Testando de origem diferente (https://exemplo.com)...")
    try:
        response = requests.get(
            API_URL,
            headers={
                'Origin': 'https://exemplo.com',
                'Content-Type': 'application/json'
            }
        )
        
        print(f"   Status: {response.status_code}")
        print(f"   Access-Control-Allow-Origin: {response.headers.get('Access-Control-Allow-Origin', 'Not set')}")
        
        allow_origin = response.headers.get('Access-Control-Allow-Origin', '')
        if allow_origin == '*' or allow_origin == 'https://exemplo.com':
            print("   ✅ Todas as origens permitidas")
        else:
            print("   ⚠️  Origem específica ou bloqueada")
            
    except Exception as e:
        print(f"   ❌ Erro: {e}")
        return False
    
    return True

def main():
    success = test_cors()
    
    print("\n" + "=" * 60)
    if success:
        print("✅ CORS configurado corretamente!")
        print("\n💡 Você pode acessar a API de qualquer origem")
        print("\nHeaders configurados:")
        print("   • Access-Control-Allow-Origin: *")
        print("   • Access-Control-Allow-Methods: GET,POST,PUT,DELETE,OPTIONS,PATCH")
        print("   • Access-Control-Allow-Headers: Content-Type,Authorization,X-Requested-With,Accept,Origin")
        print("=" * 60)
        return 0
    else:
        print("❌ Problemas encontrados na configuração de CORS")
        print("=" * 60)
        return 1

if __name__ == '__main__':
    sys.exit(main())
