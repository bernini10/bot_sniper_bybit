#!/usr/bin/env python3
"""
Análise do mapeamento direção (LONG/SHORT) → side (Buy/Sell)
"""
import re

def find_direction_to_side_mapping():
    """Encontrar onde direção é convertida para side"""
    print("🔍 BUSCANDO MAPEAMENTO DIREÇÃO → SIDE")
    print("=" * 60)
    
    with open('bot_executor.py', 'r') as f:
        content = f.read()
    
    # Padrões comuns de mapeamento
    mapping_patterns = [
        # if direcao == "LONG": side = "Buy"
        r'if.*?direcao.*?LONG.*?side.*?Buy',
        r'if.*?direction.*?LONG.*?side.*?Buy',
        r'if.*?LONG.*?side.*?Buy',
        
        # side = "Buy" if direcao == "LONG" else "Sell"
        r'side\s*=\s*.*?Buy.*?if.*?LONG.*?else.*?Sell',
        r'side\s*=\s*.*?Sell.*?if.*?SHORT.*?else.*?Buy',
        
        # Mapeamento direto
        r'side\s*=\s*["\']Buy["\']\s*if.*?LONG',
        r'side\s*=\s*["\']Sell["\']\s*if.*?SHORT',
        
        # Dicionário de mapeamento
        r'direction_map\s*=\s*\{.*?LONG.*?Buy.*?SHORT.*?Sell',
        r'side_map\s*=\s*\{.*?LONG.*?Buy.*?SHORT.*?Sell',
    ]
    
    found_mappings = []
    
    for pattern in mapping_patterns:
        matches = re.finditer(pattern, content, re.DOTALL | re.IGNORECASE)
        for match in matches:
            start = max(0, match.start() - 50)
            end = min(len(content), match.end() + 50)
            context = content[start:end].replace('\n', ' ')
            found_mappings.append(context)
    
    if found_mappings:
        print("📍 MAPEAMENTOS ENCONTRADOS:")
        for i, mapping in enumerate(set(found_mappings)):
            print(f"\n{i+1}. {mapping}")
    else:
        print("❌ Nenhum mapeamento explícito encontrado")
        
        # Buscar qualquer uso de side
        print("\n🔍 BUSCANDO QUALQUER USO DE 'side':")
        side_pattern = r'side\s*='
        matches = re.finditer(side_pattern, content, re.IGNORECASE)
        
        for match in matches:
            start = max(0, match.start() - 100)
            end = min(len(content), match.end() + 100)
            context = content[start:end].replace('\n', ' ')
            if 'Buy' in context or 'Sell' in context:
                print(f"\n📍 Contexto com side:")
                print(f"   ...{context}...")

def analyze_execute_function():
    """Analisar função específica de execução"""
    print("\n🔍 ANALISANDO FUNÇÃO DE EXECUÇÃO ESPECÍFICA")
    print("=" * 60)
    
    with open('bot_executor.py', 'r') as f:
        lines = f.readlines()
    
    # Encontrar função que tem 'execute' no nome
    in_function = False
    current_function = ""
    function_lines = []
    
    for i, line in enumerate(lines):
        if line.strip().startswith('def ') and 'execute' in line.lower():
            if in_function and function_lines:
                print(f"\n📍 FUNÇÃO ANTERIOR: {current_function}")
                analyze_function_lines(function_lines)
            
            in_function = True
            current_function = line.strip()
            function_lines = [line]
        elif in_function:
            function_lines.append(line)
            
            # Verificar fim da função
            if line.strip() == '' and i > 0 and lines[i-1].strip() == '':
                in_function = False
                if function_lines:
                    print(f"\n📍 FUNÇÃO: {current_function}")
                    analyze_function_lines(function_lines)
                function_lines = []
    
    if in_function and function_lines:
        print(f"\n📍 ÚLTIMA FUNÇÃO: {current_function}")
        analyze_function_lines(function_lines)

def analyze_function_lines(function_lines):
    """Analisar linhas de uma função"""
    # Buscar side e direction
    for line in function_lines:
        if 'side' in line.lower() or 'direction' in line.lower():
            print(f"   {line.rstrip()}")
    
    # Buscar chamada Bybit
    for line in function_lines:
        if 'self.exchange' in line and ('order' in line.lower() or 'trade' in line.lower()):
            print(f"   🔧 Chamada exchange: {line.strip()}")

def main():
    print("🎯 ANÁLISE DO BUG: DIREÇÃO ERRADA NA EXECUÇÃO")
    print("=" * 60)
    print("Problema: Padrão diz LONG, mas executa SHORT (ou vice-versa)")
    print("Objetivo: Encontrar onde mapeamento direção→side está errado")
    print("=" * 60)
    
    find_direction_to_side_mapping()
    analyze_execute_function()
    
    print("\n🎯 HIPÓTESES:")
    print("1. Mapeamento LONG→Sell / SHORT→Buy (invertido)")
    print("2. Bybit espera 'Buy'/'Sell' mas recebe 'long'/'short'")
    print("3. Direção vem errada do padrão")
    print("4. Bug na lógica condicional")

if __name__ == "__main__":
    main()
