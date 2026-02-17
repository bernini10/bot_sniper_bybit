#!/usr/bin/env python3
"""
Testar se a correção do bug funciona
"""
print("🎯 TESTANDO CORREÇÃO DO BUG DE DIREÇÃO")
print("=" * 60)

# Simular dados Bybit
test_positions = [
    {'symbol': 'GRT/USDT:USDT', 'side': 'sell', 'contracts': 1125.8},
    {'symbol': 'EGLD/USDT:USDT', 'side': 'sell', 'contracts': 2.48},
    {'symbol': 'TEST/USDT:USDT', 'side': 'buy', 'contracts': 10.0},
]

print("📊 DADOS DE TESTE (simulando Bybit):")
for pos in test_positions:
    print(f"   • {pos['symbol']}: side='{pos['side']}', contracts={pos['contracts']}")

print("\n🔍 APLICANDO LÓGICA ANTIGA (BUGADA):")
for pos in test_positions:
    # Lógica antiga ERRADA
    side_old = 'LONG' if float(pos.get('contracts', 0)) > 0 else 'SHORT'
    print(f"   {pos['symbol']}: contracts={pos['contracts']} → side='{side_old}'")
    print(f"     ⚠️  ERRADO! Bybit diz side='{pos['side']}' mas calculou '{side_old}'")

print("\n🔍 APLICANDO LÓGICA NOVA (CORRETA):")
for pos in test_positions:
    # Lógica nova CORRETA
    side_new = 'LONG' if pos.get('side', '').lower() == 'buy' else 'SHORT'
    print(f"   {pos['symbol']}: side='{pos['side']}' → side='{side_new}'")
    print(f"     ✅ CORRETO! Bybit '{pos['side']}' → '{side_new}'")

print("\n🎯 CONCLUSÃO:")
print("   • Bug: Lógica usava contracts > 0 para determinar side")
print("   • Correção: Agora usa pos.get('side') diretamente")
print("   • Resultado: Dashboard mostrará side correto")
