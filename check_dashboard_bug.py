#!/usr/bin/env python3
"""
Verificar exatamente o bug do dashboard vs corretora
"""
import json
import os

def check_dashboard_data():
    """Verificar que dados o dashboard está mostrando"""
    print("🎯 VERIFICANDO DADOS DO DASHBOARD")
    print("=" * 60)
    
    # Verificar templates do dashboard
    if os.path.exists('templates/dashboard.html'):
        print("📁 Template dashboard.html encontrado")
        
        # Buscar como direção é mostrada
        with open('templates/dashboard.html', 'r') as f:
            html = f.read()
        
        if 'direction' in html.lower() or 'side' in html.lower():
            print("✅ Template mostra direction/side")
            
            # Extrair parte relevante
            import re
            direction_sections = re.findall(r'\{.*?direction.*?\}', html, re.DOTALL | re.IGNORECASE)
            if direction_sections:
                print("\n📍 Seções com direction no template:")
                for section in direction_sections[:3]:
                    print(f"   {section[:100]}...")
    
    # Verificar dados da API
    print("\n🔍 VERIFICANDO DADOS DA API DO DASHBOARD:")
    
    # Tentar acessar endpoint localmente
    import requests
    try:
        response = requests.get('http://localhost:8080/api/positions', timeout=5)
        if response.status_code == 200:
            data = response.json()
            print("✅ Dados da API /api/positions:")
            print(json.dumps(data, indent=2)[:500])
        else:
            print(f"❌ API retornou status {response.status_code}")
    except Exception as e:
        print(f"⚠️  Não consegui acessar API: {e}")
        print("   Dashboard pode não estar rodando ou endpoint diferente")

def compare_with_bybit():
    """Comparar com dados reais da Bybit"""
    print("\n🎯 COMPARANDO DASHBOARD vs BYBIT REAL")
    print("=" * 60)
    
    # Dados que temos da Bybit (do diagnóstico anterior)
    bybit_positions = [
        {'symbol': 'GRT/USDT:USDT', 'side': 'short', 'contracts': 1125.8},
        {'symbol': 'EGLD/USDT:USDT', 'side': 'short', 'contracts': 2.48}
    ]
    
    print("📊 POSIÇÕES REAIS NA BYBIT:")
    for pos in bybit_positions:
        print(f"   • {pos['symbol']}: {pos['side'].upper()} ({pos['contracts']} contracts)")
    
    print("\n🎯 PROBLEMA IDENTIFICADO:")
    print("   Bybit tem: GRT/USDT: SHORT, EGLD/USDT: SHORT")
    print("   Você disse que dashboard mostra: LONG")
    print("")
    print("🔍 CAUSA POSSÍVEL:")
    print("   1. Dashboard lê de fonte errada")
    print("   2. Cache desatualizado")
    print("   3. Bug no template/display")
    print("   4. Dados transformados incorretamente")

def suggest_fix():
    """Sugerir correção"""
    print("\n🎯 SUGESTÃO DE CORREÇÃO")
    print("=" * 60)
    
    print("1. VERIFICAR dashboard_server.py:")
    print("   - Como obtém posições?")
    print("   - Usa exchange.fetch_positions() ou lê de arquivo?")
    print("")
    print("2. VERIFICAR CACHE:")
    print("   - positions_cache.json existe?")
    print("   - Está atualizado?")
    print("")
    print("3. CORREÇÃO IMEDIATA:")
    print("   - Forçar dashboard a buscar direto da Bybit")
    print("   - Limpar cache")
    print("   - Atualizar template para mostrar side corretamente")
    print("")
    print("4. IMPLEMENTAR FIX:")
    print("""
   # No dashboard_server.py, garantir:
   positions = exchange.fetch_positions()
   open_positions = [p for p in positions if float(p['contracts']) > 0]
   
   # Converter side para formato correto
   for pos in open_positions:
       pos['display_side'] = 'LONG' if pos['side'].lower() == 'buy' else 'SHORT'
   """)

if __name__ == "__main__":
    print("🔍 DIAGNÓSTICO DO BUG DASHBOARD vs BYBIT")
    print("=" * 60)
    check_dashboard_data()
    compare_with_bybit()
    suggest_fix()
    
    print("\n🎯 AÇÃO IMEDIATA:")
    print("   1. Verificar dashboard_server.py linha por linha")
    print("   2. Corrigir obtenção de posições")
    print("   3. Testar com refresh")
    print("   4. Verificar se bug persiste")
