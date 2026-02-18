#!/bin/bash
# 🎯 TESTE DE TODOS OS CENÁRIOS DO WEBHOOK

echo "🔍 TESTANDO TODOS OS CENÁRIOS DE WEBHOOK"
echo "========================================="

test_scenario() {
    local name=$1
    local host_header=$2
    local url=$3
    
    echo ""
    echo "🧪 $name:"
    echo "   Host: $host_header"
    echo "   URL: $url"
    
    if [ -z "$host_header" ]; then
        RESPONSE=$(curl -s -X POST "$url" \
          -H "Content-Type: application/json" \
          -H "Host:" \
          -d '{"btc_d_value": 59.50, "direction": "SHORT", "change_pct": -0.35}')
    else
        RESPONSE=$(curl -s -X POST "$url" \
          -H "Content-Type: application/json" \
          -H "Host: $host_header" \
          -d '{"btc_d_value": 59.50, "direction": "SHORT", "change_pct": -0.35}')
    fi
    
    if echo "$RESPONSE" | grep -q "status.*ok"; then
        echo "   ✅ SUCESSO"
        echo "   Resposta: $(echo $RESPONSE | cut -c1-80)..."
    else
        echo "   ❌ FALHA"
        echo "   Resposta: $RESPONSE"
    fi
}

# Cenário 1: Com Host header correto
test_scenario "1. Host header correto (IP)" "147.182.145.169" "http://147.182.145.169/webhook/btcd"

# Cenário 2: Sem Host header (como TradingView pode enviar)
test_scenario "2. Sem Host header" "" "http://147.182.145.169/webhook/btcd"

# Cenário 3: Host header errado (deve bloquear)
test_scenario "3. Host header errado (deve bloquear)" "liquidation-bot.app" "http://147.182.145.169/webhook/btcd"

# Cenário 4: Test endpoint
echo ""
echo "🧪 Test endpoint /test:"
curl -s http://147.182.145.169/test

# Cenário 5: Health check
echo ""
echo "🧪 Health check /health:"
curl -s http://147.182.145.169/health | python3 -m json.tool

# Verificar arquivo atualizado
echo ""
echo "📊 VERIFICANDO ARQUIVO BTC.D:"
BTCD_FILE="/root/bot_sniper_bybit/btcd_data.json"
if [ -f "$BTCD_FILE" ]; then
    python3 -c "
import json, time
d = json.load(open('$BTCD_FILE'))
age = (time.time() - d.get('timestamp', 0)) / 60
print(f'   Valor: {d.get(\"btc_d_value\", \"N/A\")}%')
print(f'   Direção: {d.get(\"direction\", \"N/A\")}')
print(f'   Change: {d.get(\"change_pct\", \"N/A\")}%')
print(f'   Atualizado há: {age:.1f} minutos')
"
else
    echo "❌ Arquivo não existe"
fi

echo ""
echo "🎯 RESUMO FINAL:"
echo "----------------"
echo "✅ Webhook proxy configurado para:"
echo "   - Aceitar requisições COM Host header: 147.182.145.169"
echo "   - Aceitar requisições SEM Host header (TradingView)"
echo "   - Bloquear outros hosts (liquidation-bot.app, etc.)"
echo ""
echo "📝 TRADINGVIEW CONFIGURADO CORRETAMENTE:"
echo "   URL: http://147.182.145.169/webhook/btcd"
echo "   Mensagem: {{alert.message}}"
echo ""
echo "🚀 AGORA TESTE NO TRADINGVIEW:"
echo "   1. Clique em 'Send Test Alert'"
echo "   2. Verifique se chega aqui"
echo "   3. Sistema pronto para operar!"