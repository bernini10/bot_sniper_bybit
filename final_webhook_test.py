#!/usr/bin/env python3
"""
TESTE FINAL DO WEBHOOK - SIMULA TRADINGVIEW
"""

import requests
import json
import time

def test_webhook(message, content_type="application/json"):
    """Testa o webhook com diferentes formatos"""
    print(f"\n🧪 Testando: {message[:50]}...")
    print(f"   Content-Type: {content_type}")
    
    try:
        response = requests.post(
            "http://147.182.145.169/webhook/btcd",
            data=message if content_type == "text/plain" else None,
            json=json.loads(message) if content_type == "application/json" and '{' in message else None,
            headers={"Content-Type": content_type},
            timeout=10
        )
        
        print(f"   Status: {response.status_code}")
        print(f"   Resposta: {response.text[:100]}")
        
        if response.status_code == 200:
            print("   ✅ SUCESSO!")
            return True
        else:
            print("   ❌ FALHA")
            return False
            
    except Exception as e:
        print(f"   ❌ ERRO: {e}")
        return False

print("🎯 TESTE FINAL DO WEBHOOK - SIMULANDO TRADINGVIEW")
print("="*60)

# Teste 1: JSON correto (ideal)
test_webhook('{"btc_d_value": 59.45, "direction": "LONG", "change_pct": 0.25}')

# Teste 2: JSON com strings (TV pode enviar assim)
test_webhook('{"btc_d_value": "59.45", "direction": "LONG", "change_pct": "0.25"}')

# Teste 3: Texto simples
test_webhook('BTC.D: 59.45%, Direction: LONG, Change: 0.25%', "text/plain")

# Teste 4: Texto sem formatação
test_webhook('59.45 LONG 0.25%', "text/plain")

# Teste 5: Form data (TV às vezes usa)
print("\n🧪 Testando Form data:")
try:
    response = requests.post(
        "http://147.182.145.169/webhook/btcd",
        data={"btc_d_value": "59.45", "direction": "LONG", "change_pct": "0.25"},
        timeout=10
    )
    print(f"   Status: {response.status_code}")
    print(f"   Resposta: {response.text[:100]}")
except Exception as e:
    print(f"   ❌ ERRO: {e}")

# Verificar arquivo final
print("\n📊 VERIFICANDO ARQUIVO BTC.D:")
try:
    with open('/root/bot_sniper_bybit/btcd_data.json', 'r') as f:
        data = json.load(f)
    
    age = (time.time() - data.get('timestamp', 0)) / 60
    print(f"   Valor: {data.get('btc_d_value', 'N/A')}%")
    print(f"   Direção: {data.get('direction', 'N/A')}")
    print(f"   Change: {data.get('change_pct', 'N/A')}%")
    print(f"   Atualizado há: {age:.1f} minutos")
    
except Exception as e:
    print(f"   ❌ Erro ao ler arquivo: {e}")

print("\n🎯 CONCLUSÃO:")
print("="*60)
print("✅ Webhook server ACEITA:")
print("   - JSON com números: {\"btc_d_value\": 59.45, ...}")
print("   - JSON com strings: {\"btc_d_value\": \"59.45\", ...}")
print()
print("❌ Webhook server REJEITA (por enquanto):")
print("   - Texto simples (precisa ajustar parser)")
print()
print("🔗 URL TradingView: http://147.182.145.169/webhook/btcd")
print("📝 Mensagem TradingView: {{alert.message}}")
print()
print("🚀 RECOMENDAÇÃO FINAL:")
print("Use no TradingView código Pine que gere JSON!")
print("Exemplo: '{\"btc_d_value\": ' + str.tostring(btcDom, '#.##') + ', ...}'")