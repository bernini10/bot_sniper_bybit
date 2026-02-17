#!/usr/bin/env python3
"""
Teste direto do bug de direção
"""
import json

def test_direction_logic():
    """Testar a lógica de direção atual"""
    print("🎯 TESTANDO LÓGICA DE DIREÇÃO ATUAL")
    print("=" * 60)
    
    # Lógica atual do bot_executor.py
    def current_logic(direcao):
        return 'sell' if direcao == 'SHORT' else 'buy'
    
    # Test cases
    test_cases = [
        ('SHORT', 'sell'),
        ('LONG', 'buy'),
    ]
    
    print("📊 TESTE DA LÓGICA ATUAL:")
    for direcao_input, expected in test_cases:
        result = current_logic(direcao_input)
        status = "✅" if result == expected else "❌"
        print(f"   {status} direcao='{direcao_input}' → side='{result}' (esperado: '{expected}')")
    
    print("\n🔍 PROBLEMA POSSÍVEL:")
    print("   1. Se 'direcao' vem como 'short' ou 'long' (minúsculo)")
    print("   2. Se 'direcao' vem invertido do padrão")
    print("   3. Se Bybit interpreta diferente")
    
    print("\n🎯 VERIFICANDO WATCHLIST ATUAL:")
    try:
        with open('watchlist.json', 'r') as f:
            data = json.load(f)
        
        if 'pares' in data:
            for pair in data['pares']:
                symbol = pair.get('symbol', 'N/A')
                direcao = pair.get('direcao', 'N/A')
                padrao = pair.get('padrao', 'N/A')
                
                # Aplicar lógica atual
                side = current_logic(direcao)
                
                print(f"   {symbol}:")
                print(f"     • Padrão: {padrao}")
                print(f"     • Direção: {direcao}")
                print(f"     • Side calculado: {side}")
                
                # Verificar se faz sentido
                if 'TOPO' in padrao and direcao != 'SHORT':
                    print(f"     ⚠️  TOPO_DUPLO deveria ser SHORT, mas é {direcao}")
                elif 'FUNDO' in padrao and direcao != 'LONG':
                    print(f"     ⚠️  FUNDO_DUPLO deveria ser LONG, mas é {direcao}")
                    
    except Exception as e:
        print(f"❌ Erro: {e}")

def check_recent_trades():
    """Verificar trades recentes"""
    print("\n🎯 VERIFICANDO TRADES RECENTES")
    print("=" * 60)
    
    try:
        with open('trades_history.json', 'r') as f:
            data = json.load(f)
        
        if isinstance(data, list):
            trades = data[-10:]  # Últimos 10 trades
        elif isinstance(data, dict) and 'trades' in data:
            trades = data['trades'][-10:]
        else:
            trades = []
        
        print(f"📈 Últimos {len(trades)} trades:")
        for trade in trades:
            if isinstance(trade, dict):
                symbol = trade.get('symbol', 'N/A')
                direction = trade.get('direction', 'N/A')
                side = trade.get('side', 'N/A')
                pattern = trade.get('pattern_name', trade.get('pattern', 'N/A'))
                
                print(f"   • {symbol}: direction='{direction}', side='{side}', pattern='{pattern}'")
                
                # Verificar consistência
                if direction and side:
                    if direction.upper() == 'LONG' and side.lower() != 'buy':
                        print(f"     ⚠️  INCONSISTÊNCIA: LONG mas side='{side}'")
                    elif direction.upper() == 'SHORT' and side.lower() != 'sell':
                        print(f"     ⚠️  INCONSISTÊNCIA: SHORT mas side='{side}'")
                        
    except Exception as e:
        print(f"❌ Erro ao ler trades: {e}")

if __name__ == "__main__":
    print("🔍 DIAGNÓSTICO COMPLETO DO BUG DE DIREÇÃO")
    print("=" * 60)
    test_direction_logic()
    check_recent_trades()
    
    print("\n🎯 CONCLUSÃO:")
    print("1. A lógica 'side = sell if direcao == SHORT else buy' parece correta")
    print("2. O problema pode estar em:")
    print("   a) 'direcao' vindo errado do padrão")
    print("   b) Dashboard mostrando informação errada")
    print("   c) Bybit executando ordem diferente")
    print("3. Preciso ver LOGS REAIS de execução")
