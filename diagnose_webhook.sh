#!/bin/bash
# 🎯 DIAGNÓSTICO COMPLETO DO WEBHOOK BTC.D

echo "🔍 DIAGNÓSTICO DO WEBHOOK BTC.D"
echo "================================="
echo "Data: $(date)"
echo ""

# 1. VERIFICAR WEBHOOK SERVER
echo "1️⃣  WEBHOOK SERVER STATUS:"
echo "---------------------------"

# Processo
if ps aux | grep webhook_server.py | grep -v grep > /dev/null; then
    echo "✅ Webhook server rodando"
    ps aux | grep webhook_server.py | grep -v grep
else
    echo "❌ Webhook server NÃO está rodando"
fi

echo ""

# 2. VERIFICAR PORTA
echo "2️⃣  PORTA 5555:"
echo "---------------"

if ss -tlnp | grep :5555 > /dev/null; then
    echo "✅ Porta 5555 ouvindo"
    ss -tlnp | grep :5555
else
    echo "❌ Porta 5555 NÃO está ouvindo"
fi

echo ""

# 3. VERIFICAR ARQUIVO BTC.D
echo "3️⃣  ARQUIVO BTC.D DATA:"
echo "----------------------"

BTCD_FILE="/root/bot_sniper_bybit/btcd_data.json"

if [ -f "$BTCD_FILE" ]; then
    echo "✅ Arquivo existe: $BTCD_FILE"
    
    # Ler dados
    VALUE=$(python3 -c "import json, time; d=json.load(open('$BTCD_FILE')); print(d.get('btc_d_value', 'N/A'))")
    DIRECTION=$(python3 -c "import json, time; d=json.load(open('$BTCD_FILE')); print(d.get('direction', 'N/A'))")
    TIMESTAMP=$(python3 -c "import json, time; d=json.load(open('$BTCD_FILE')); print(d.get('timestamp', 0))")
    
    CURRENT_TIME=$(date +%s)
    AGE_SECONDS=$((CURRENT_TIME - ${TIMESTAMP%.*}))
    AGE_MINUTES=$((AGE_SECONDS / 60))
    
    echo "   Valor: $VALUE%"
    echo "   Direção: $DIRECTION"
    echo "   Última atualização: há $AGE_MINUTES minutos ($AGE_SECONDS segundos)"
    
    if [ $AGE_MINUTES -gt 30 ]; then
        echo "   ⚠️  DADOS ANTIGOS! TradingView não está enviando."
    else
        echo "   ✅ Dados recentes"
    fi
    
else
    echo "❌ Arquivo NÃO existe: $BTCD_FILE"
fi

echo ""

# 4. TESTAR ENDPOINT LOCAL
echo "4️⃣  TESTE DO ENDPOINT LOCAL:"
echo "---------------------------"

echo "Testando POST para webhook..."
RESPONSE=$(curl -s -X POST http://localhost:5555/webhook/btcd \
  -H "Content-Type: application/json" \
  -d '{"btc_d_value": 59.25, "direction": "LONG", "change_pct": 0.3}')

if echo "$RESPONSE" | grep -q "status.*ok"; then
    echo "✅ Endpoint local funciona"
    echo "   Resposta: $RESPONSE"
else
    echo "❌ Endpoint local FALHOU"
    echo "   Resposta: $RESPONSE"
fi

echo ""

# 5. VERIFICAR IP PÚBLICO
echo "5️⃣  CONFIGURAÇÃO EXTERNA:"
echo "-------------------------"

PUBLIC_IP=$(curl -s ifconfig.me 2>/dev/null || echo "NÃO DETECTADO")
echo "IP Público: $PUBLIC_IP"
echo "URL do Webhook: http://$PUBLIC_IP:5555/webhook/btcd"

echo ""

# 6. VERIFICAR FIREWALL
echo "6️⃣  FIREWALL/PORTA EXTERNA:"
echo "---------------------------"

# Testar se porta está acessível externamente (simplificado)
echo "Para testar externamente, use:"
echo "  curl -X POST http://$PUBLIC_IP:5555/webhook/btcd \\"
echo "    -H \"Content-Type: application/json\" \\"
echo "    -d '{\"btc_d_value\": 59.5, \"direction\": \"SHORT\", \"change_pct\": -0.2}'"

echo ""

# 7. RESUMO
echo "🎯 RESUMO DO DIAGNÓSTICO:"
echo "-------------------------"

if [ $AGE_MINUTES -gt 30 ] 2>/dev/null; then
    echo "❌ PROBLEMA PRINCIPAL: TradingView não está enviando dados"
    echo ""
    echo "📝 CAUSAS POSSÍVEIS:"
    echo "   1. Alerta desativado no TradingView"
    echo "   2. URL incorreta no alerta"
    echo "   3. Formato da mensagem incorreto"
    echo "   4. Firewall bloqueando porta 5555"
    echo ""
    echo "🔧 SOLUÇÕES:"
    echo "   1. Verificar alerta no TV: http://147.182.145.169:5555/webhook/btcd"
    echo "   2. Usar formato JSON: {\"btc_d_value\": {{plot...}}, ...}"
    echo "   3. Testar com \"Send Test Alert\" no TV"
    echo "   4. Verificar logs do webhook server"
else
    echo "✅ Sistema funcionando normalmente"
fi

echo ""
echo "📊 DADOS ATUAIS VIA PROXY:"
python3 -c "
from lib_utils import check_btc_dominance_proxy
import ccxt
exchange = ccxt.bybit({'enableRateLimit': True})
proxy_result = check_btc_dominance_proxy(exchange)
print(f'   BTC.D Proxy: {proxy_result}')
"

echo ""
echo "🔚 Diagnóstico completo."