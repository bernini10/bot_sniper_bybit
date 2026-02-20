#!/usr/bin/env python3
"""
Teste da nova API key do Gemini com pacote atualizado
"""
import os
import google.genai as genai
from dotenv import load_dotenv

load_dotenv()

# Carregar nova API key
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY', 'AIzaSyBXFMhWlz9AVtqzR3P4-FW5gMJX1kTJ0SM')

print(f"🔑 API Key carregada: {GOOGLE_API_KEY[:20]}...")

# Configurar Gemini com novo pacote
try:
    client = genai.Client(api_key=GOOGLE_API_KEY)
    print("✅ Cliente Gemini configurado com sucesso")
    
    # Listar modelos disponíveis
    print("\n🔍 Listando modelos disponíveis...")
    models = list(client.models.list())
    
    if models:
        print(f"✅ {len(models)} modelos encontrados")
        
        # Filtrar modelos de vision/gemini
        gemini_models = [m for m in models if 'gemini' in m.name.lower()]
        
        if gemini_models:
            print("\n🤖 Modelos Gemini disponíveis:")
            for model in gemini_models[:5]:  # Mostrar apenas os primeiros 5
                print(f"  - {model.name} (suporta: {model.supported_generation_methods})")
            
            # Testar com um modelo específico
            model_name = "gemini-2.0-flash"  # Modelo mais comum
            
            print(f"\n🧪 Testando modelo: {model_name}")
            
            try:
                # Teste simples de texto
                response = client.models.generate_content(
                    model=model_name,
                    contents="Olá, Gemini! Esta é uma mensagem de teste. Responda com 'API funcionando corretamente!'"
                )
                
                print(f"✅ Resposta do Gemini: {response.text}")
                print("\n🎉 API DO GEMINI FUNCIONANDO CORRETAMENTE COM NOVO PACOTE!")
                
            except Exception as e:
                print(f"❌ Erro ao testar modelo: {e}")
                print(f"Tipo de erro: {type(e).__name__}")
        else:
            print("⚠️  Nenhum modelo Gemini encontrado")
    else:
        print("❌ Nenhum modelo disponível")
        
except Exception as e:
    print(f"❌ Erro ao configurar cliente Gemini: {e}")
    print(f"Tipo de erro: {type(e).__name__}")
    print(f"Detalhes: {str(e)}")

# Verificar se o sistema atual está usando o pacote antigo
print("\n🔧 Verificando dependências do sistema...")
try:
    import subprocess
    result = subprocess.run(['pip', 'show', 'google-generativeai'], capture_output=True, text=True)
    if result.returncode == 0:
        print("⚠️  Pacote antigo 'google-generativeai' instalado")
        lines = result.stdout.split('\n')
        for line in lines:
            if 'Version:' in line:
                print(f"  Versão: {line}")
    else:
        print("✅ Pacote antigo não encontrado")
        
    result = subprocess.run(['pip', 'show', 'google-genai'], capture_output=True, text=True)
    if result.returncode == 0:
        print("✅ Pacote novo 'google-genai' instalado")
        lines = result.stdout.split('\n')
        for line in lines:
            if 'Version:' in line:
                print(f"  Versão: {line}")
    else:
        print("⚠️  Pacote novo 'google-genai' não instalado")
        
except Exception as e:
    print(f"Erro ao verificar dependências: {e}")