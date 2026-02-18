#!/usr/bin/env python3
"""
Diagnóstico direto do bug de direção LONG/SHORT
"""
import json
import os
import re

def analyze_watchlist():
    """Analisar watchlist para ver direções"""
    print("🔍 ANALISANDO WATCHLIST")
    print("=" * 40)
    
    try:
        with open('watchlist.json', 'r') as f:
            data = json.load(f)
        
        if 'pares' not in data:
            print("❌ Estrutura watchlist inválida")
            return
        
        print(f"📊 Total pares: {len(data['pares'])}")
        print("\n📋 Pares atuais:")
        for i, pair in enumerate(data['pares']):
            symbol = pair.get('symbol', 'N/A')
            pattern = pair.get('padrao', 'N/A')
            direction = pair.get('direcao', 'N/A')
            confidence = pair.get('confiabilidade', 0)
            
            print(f"  {i+1}. {symbol}")
            print(f"     Padrão: {pattern}")
            print(f"     Direção: {direction}")
            print(f"     Confiança: {confidence:.2f}")
            print()
            
    except Exception as e:
        print(f"❌ Erro ao analisar watchlist: {e}")

def analyze_executor_code():
    """Analisar código do executor"""
    print("\n🔍 ANALISANDO CÓDIGO DO EXECUTOR")
    print("=" * 40)
    
    try:
        with open('bot_executor.py', 'r') as f:
            content = f.read()
        
        # Encontrar função execute_trade
        pattern = r'def execute_trade\(.*?\):(.*?)(?=\n\s*def|\n\s*$)'
        match = re.search(pattern, content, re.DOTALL)
        
        if match:
            execute_code = match.group(1)
            print("📍 Função execute_trade encontrada")
            
            # Analisar como direction é usada
            lines = execute_code.split('\n')
            direction_lines = []
            
            for i, line in enumerate(lines):
                if 'direction' in line.lower():
                    direction_lines.append((i, line.strip()))
            
            if direction_lines:
                print("\n📝 Linhas com 'direction':")
                for line_num, line_text in direction_lines:
                    print(f"   Linha ~{line_num}: {line_text}")
            else:
                print("   ℹ️  'direction' não encontrada na função execute_trade")
        
        # Buscar onde direction é obtida
        print("\n🔎 Buscando origem da direção:")
        origin_patterns = [
            r'direction\s*=\s*([^#\n]+)',
            r'get.*direction',
            r'pattern.*direction',
            r'direcao.*direction'
        ]
        
        for pattern in origin_patterns:
            matches = re.finditer(pattern, content, re.IGNORECASE)
            for match in matches:
                line_start = max(0, match.start() - 50)
                line_end = min(len(content), match.end() + 50)
                context = content[line_start:line_end].replace('\n', ' ')
                print(f"   Contexto: ...{context}...")
                
    except Exception as e:
        print(f"❌ Erro ao analisar código: {e}")

def analyze_pattern_direction_mapping():
    """Analisar mapeamento padrão → direção"""
    print("\n🔍 ANALISANDO MAPEAMENTO PADRÃO → DIREÇÃO")
    print("=" * 40)
    
    # Verificar lib_padroes.py
    if os.path.exists('lib_padroes.py'):
        try:
            with open('lib_padroes.py', 'r') as f:
                content = f.read()
            
            # Buscar classes de padrão
            class_pattern = r'class (\w+).*?:'
            classes = re.findall(class_pattern, content)
            
            print("📍 Classes de padrão encontradas:")
            for class_name in classes[:10]:  # Limitar a 10
                print(f"   • {class_name}")
            
            # Buscar mapeamento direção
            direction_map = {}
            direction_patterns = [
                r'(\w+).*?=.*?[\"\'](LONG|SHORT)[\"\']',
                r'direction.*?=.*?[\"\'](LONG|SHORT)[\"\']',
                r'returns.*?[\"\'](LONG|SHORT)[\"\']'
            ]
            
            for pattern in direction_patterns:
                matches = re.finditer(pattern, content, re.IGNORECASE)
                for match in matches:
                    print(f"   Mapeamento encontrado: {match.group(0)}")
                    
        except Exception as e:
            print(f"❌ Erro ao analisar lib_padroes.py: {e}")
    else:
        print("❌ lib_padroes.py não encontrado")

def check_current_trades():
    """Verificar trades atuais"""
    print("\n🔍 VERIFICANDO TRADES ATUAIS")
    print("=" * 40)
    
    # Verificar trades_history.json
    if os.path.exists('trades_history.json'):
        try:
            with open('trades_history.json', 'r') as f:
                data = json.load(f)
            
            if isinstance(data, list):
                trades = data
            elif isinstance(data, dict) and 'trades' in data:
                trades = data['trades']
            else:
                trades = []
            
            print(f"📈 Total trades no histórico: {len(trades)}")
            
            if trades:
                print("\n📋 Últimos 5 trades:")
                for trade in trades[-5:]:
                    if isinstance(trade, dict):
                        symbol = trade.get('symbol', 'N/A')
                        direction = trade.get('direction', 'N/A')
                        pattern = trade.get('pattern_name', trade.get('pattern', 'N/A'))
                        print(f"  • {symbol}: {direction} (Padrão: {pattern})")
                    else:
                        print(f"  • Trade em formato inválido: {trade}")
                        
        except Exception as e:
            print(f"❌ Erro ao ler trades_history.json: {e}")
    else:
        print("❌ trades_history.json não encontrado")

def main():
    """Função principal"""
    print("🎯 DIAGNÓSTICO DO BUG DE DIREÇÃO LONG/SHORT")
    print("=" * 60)
    print("Problema: Site mostra LONG, corretora executa SHORT")
    print("Objetivo: Encontrar onde direção é invertida")
    print("=" * 60)
    
    analyze_watchlist()
    analyze_executor_code()
    analyze_pattern_direction_mapping()
    check_current_trades()
    
    print("\n🎯 CONCLUSÃO DO DIAGNÓSTICO:")
    print("=" * 40)
    print("1. Verificar watchlist.json - direção está correta?")
    print("2. Analisar bot_executor.py - onde direction é definida?")
    print("3. Verificar lib_padroes.py - mapeamento padrão→direção")
    print("4. Checar trades atuais - qual direção foi executada?")
    print("\n🔧 PRÓXIMOS PASSOS:")
    print("1. Corrigir mapeamento padrão → direção")
    print("2. Garantir executor usa direção do padrão")
    print("3. Testar com nova ordem")
    print("4. Verificar site vs corretora")

if __name__ == "__main__":
    main()
