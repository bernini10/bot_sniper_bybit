#!/usr/bin/env python3
"""
Encontrar bug exato na obtenção de posições
"""
import re

def find_position_function():
    """Encontrar função que obtém posições"""
    print("🔍 BUSCANDO FUNÇÃO QUE OBTÉM POSIÇÕES DA BYBIT")
    print("=" * 60)
    
    with open('dashboard_server.py', 'r') as f:
        lines = f.readlines()
    
    # Procurar função que chama exchange
    in_function = False
    current_function = ""
    
    for i, line in enumerate(lines):
        # Início de função
        if line.strip().startswith('def '):
            if in_function:
                # Terminou função anterior
                pass
            in_function = True
            current_function = line.strip()
            
        # Dentro de função, procurar fetch_positions
        elif in_function and 'fetch_positions' in line:
            print(f"\n📍 FUNÇÃO: {current_function}")
            print(f"   Linha {i+1}: {line.strip()}")
            
            # Mostrar contexto da função
            print(f"\n   Contexto da função (linhas {i-5} a {i+5}):")
            for j in range(max(0, i-5), min(len(lines), i+6)):
                marker = " ← fetch_positions" if j == i else ""
                print(f"   {j+1:3d}: {lines[j].rstrip()}{marker}")
            
            # Analisar como side é tratada
            print(f"\n   🔍 ANALISANDO TRATAMENTO DE 'side':")
            for j in range(max(0, i-10), min(len(lines), i+20)):
                if 'side' in lines[j].lower():
                    print(f"      Linha {j+1}: {lines[j].rstrip()}")
                    
                    # Verificar conversão
                    line_lower = lines[j].lower()
                    if 'buy' in line_lower and 'long' in line_lower:
                        print(f"        → Conversão: buy → LONG")
                    elif 'sell' in line_lower and 'short' in line_lower:
                        print(f"        → Conversão: sell → SHORT")
                    elif 'if' in line_lower and 'else' in line_lower:
                        print(f"        → Lógica condicional")
            
            print("\n   🔍 BUSCANDO RETORNO/ATRIBUIÇÃO:")
            for j in range(i, min(len(lines), i+30)):
                if '=' in lines[j] and 'position' in lines[j].lower():
                    print(f"      Linha {j+1}: {lines[j].rstrip()}")
                elif 'return' in lines[j] or 'jsonify' in lines[j]:
                    print(f"      Linha {j+1}: {lines[j].rstrip()}")
                    break

def analyze_main_route():
    """Analisar rota principal"""
    print("\n🔍 ANALISANDO ROTA PRINCIPAL /")
    print("=" * 60)
    
    with open('dashboard_server.py', 'r') as f:
        content = f.read()
    
    # Encontrar rota principal
    main_route_pattern = r"@app\.route\(['\"]/['\"].*?\n(.*?return render_template.*?\n)"
    main_match = re.search(main_route_pattern, content, re.DOTALL)
    
    if main_match:
        route_code = main_match.group(1)
        print("📍 CÓDIGO DA ROTA PRINCIPAL:")
        print("-" * 40)
        
        lines = route_code.split('\n')
        
        # Buscar onde posições são obtidas
        positions_found = False
        for i, line in enumerate(lines):
            if 'position' in line.lower() and '=' in line:
                positions_found = True
                print(f"\n   📍 OBTENÇÃO DE POSIÇÕES (linha ~{i}):")
                print(f"      {line.strip()}")
                
                # Mostrar contexto
                for j in range(max(0, i-3), min(len(lines), i+4)):
                    print(f"      {lines[j].rstrip()}")
        
        if not positions_found:
            print("   ❌ Não encontrei obtenção de posições na rota principal")
            
        # Buscar dados passados para template
        print(f"\n   🔍 DADOS PASSADOS PARA TEMPLATE:")
        for i, line in enumerate(lines):
            if 'render_template' in line:
                print(f"      Linha final: {line.strip()}")
                
                # Extrair variáveis passadas
                if '**' in line:
                    print(f"      → Passa todas variáveis locais")
                else:
                    # Tentar extrair variáveis específicas
                    pass
                
                # Verificar variáveis definidas antes
                print(f"\n      📋 VARIÁVEIS DEFINIDAS ANTES:")
                vars_found = set()
                for j in range(0, i):
                    if '=' in lines[j] and not lines[j].strip().startswith('#'):
                        var_parts = lines[j].split('=')
                        if len(var_parts) > 0:
                            var_name = var_parts[0].strip()
                            if var_name and not var_name.startswith(' '):
                                vars_found.add(var_name)
                
                for var in sorted(vars_found):
                    print(f"         • {var}")

if __name__ == "__main__":
    print("🎯 DIAGNÓSTICO DO BUG DE POSIÇÕES NO DASHBOARD")
    print("=" * 60)
    find_position_function()
    analyze_main_route()
    
    print("\n🎯 HIPÓTESE DO BUG:")
    print("   1. Dashboard obtém posições mas converte side incorretamente")
    print("   2. Template mostra 'LONG' mas dados são 'short'")
    print("   3. Bug na conversão buy/sell → LONG/SHORT")
    print("   4. Dados vêm de fonte errada (não da Bybit)")
