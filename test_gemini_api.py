#!/usr/bin/env python3
"""
Teste da nova API key do Gemini
"""
import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

# Carregar nova API key
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY', 'AIzaSyBXFMhWlz9AVtqzR3P4-FW5gMJX1kTJ0SM')

print(f"🔑 API Key carregada: {GOOGLE_API_KEY[:20]}...")

# Configurar Gemini
try:
    genai.configure(api_key=GOOGLE_API_KEY)
    print("✅ Gemini configurado com sucesso")
    
    # Listar modelos disponíveis
    print("\n🔍 Listando modelos disponíveis...")
    models = list(genai.list_models())
    
    if models:
        print(f"✅ {len(models)} modelos encontrados")
        
        # Filtrar modelos de vision
        vision_models = [m for m in models if 'vision' in m.name.lower() or 'gemini' in m.name.lower()]
        
        if vision_models:
            print("\n📸 Modelos de Vision disponíveis:")
            for model in vision_models[:5]:  # Mostrar apenas os primeiros 5
                print(f"  - {model.name}")
            
            # Testar com um modelo específico
            model_name = "gemini-1.5-pro" if any('1.5' in m.name for m in vision_models) else vision_models[0].name
            
            print(f"\n🧪 Testando modelo: {model_name}")
            
            try:
                model = genai.GenerativeModel(model_name)
                
                # Teste simples de texto
                response = model.generate_content("Olá, Gemini! Esta é uma mensagem de teste. Responda com 'API funcionando corretamente!'")
                
                print(f"✅ Resposta do Gemini: {response.text}")
                print("\n🎉 API DO GEMINI FUNCIONANDO CORRETAMENTE!")
                
            except Exception as e:
                print(f"❌ Erro ao testar modelo: {e}")
        else:
            print("⚠️  Nenhum modelo de vision encontrado")
    else:
        print("❌ Nenhum modelo disponível")
        
except Exception as e:
    print(f"❌ Erro ao configurar Gemini: {e}")
    print(f"Detalhes: {str(e)}")

# Testar também com requests direto para verificar a chave
print("\n🔗 Testando conexão direta com API...")
import requests

try:
    url = f"https://generativelanguage.googleapis.com/v1beta/models?key={GOOGLE_API_KEY}"
    response = requests.get(url, timeout=10)
    
    if response.status_code == 200:
        print("✅ Conexão com API Google estabelecida")
        data = response.json()
        if 'models' in data:
            print(f"✅ {len(data['models'])} modelos disponíveis na API")
        else:
            print(f"⚠️  Resposta inesperada: {data}")
    elif response.status_code == 403:
        print("❌ ERRO 403: API key inválida ou sem permissões")
        print(f"Resposta: {response.text}")
    elif response.status_code == 400:
        print("❌ ERRO 400: Requisição mal formada")
        print(f"Resposta: {response.text}")
    else:
        print(f"⚠️  Status code {response.status_code}: {response.text}")
        
except requests.exceptions.RequestException as e:
    print(f"❌ Erro de conexão: {e}")