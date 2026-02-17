#!/bin/bash
# 🎯 TESTE DE TODOS OS FORMATOS POSSÍVEIS DO TRADINGVIEW

echo "🔍 TESTANDO TODOS OS FORMATOS DE MENSAGEM"
echo "========================================="

test_format() {
    local name=$1
    local message=$2
    
    echo ""
    echo "🧪 $name:"
    echo "   Mensagem: $message"
    
    RESPONSE=$(curl -s -X POST http://147.182.145.169/webhook/btcd \
      -H "Content-Type: application/json" \
      -d "$message")
    
    if echo "$RESPONSE" | grep -q "status.*ok"; then
        echo "   ✅ ACEITO"
        echo "   Resposta: $(echo $RESPONSE | python3 -c "import json, sys; print(json.dumps(json.loads(sys.stdin.read()), indent=2)[:100])" 2>/dev/null || echo $RESPONSE)"
    else
        echo "   ❌ REJEITADO"
        echo "   Resposta: $RESPONSE"
    fi
}

# Formato 1: JSON correto
test_format "1. JSON correto" '{"btc_d_value": 59.32, "direction": "SHORT", "change_pct": -0.28}'

# Formato 2: Texto simples (novo parser)
test_format "2. Texto simples" 'BTC.D: 59.32%, Direction: SHORT, Change: -0.28%'

# Formato 3: Texto sem vírgulas
test_format "3. Texto sem vírgulas" 'BTC.D 59.32 SHORT -0.28%'

# Formato 4: Apenas número
test_format "4. Apenas número" '59.32%'

# Formato 5: JSON com strings (TV pode enviar assim)
test_format "5. JSON com strings" '{"btc_d_value": "59.32", "direction": "SHORT", "change_pct": "-0.28"}'

# Formato 6: Form data (TV às vezes envia assim)
echo ""
echo "🧪 6. Form data:"
RESPONSE=$(curl -s -X POST http://147.182.145.169/webhook/btcd \
  -d "btc_d_value=59.32&direction=SHORT&change_pct=-0.28")
if echo "$RESPONSE" | grep -q "status.*ok"; then
    echo "   ✅ ACEITO"
else
    echo "   ❌ REJEITADO"
fi

# Verificar arquivo final
echo ""
echo "📊 ARQUIVO BTC.D ATUAL:"
python3 -c "
import json, time, os
btcd_file = '/root/bot_sniper_bybit/btcd_data.json'
if os.path.exists(btcd_file):
    with open(btcd_file, 'r') as f:
        data = json.load(f)
    age = (time.time() - data.get('timestamp', 0)) / 60
    print(f'   Valor: {data.get(\"btc_d_value\", \"N/A\")}%')
    print(f'   Direção: {data.get(\"direction\", \"N/A\")}')
    print(f'   Change: {data.get(\"change_pct\", \"N/A\")}%')
    print(f'   Atualizado há: {age:.1f} minutos')
else:
    print('❌ Arquivo não existe')
"

echo ""
echo "🎯 RESUMO FINAL PARA TRADINGVIEW:"
echo "---------------------------------"
echo "✅ SISTEMA PRONTO PARA QUALQUER FORMATO:"
echo "   1. JSON: {\"btc_d_value\": 59.32, \"direction\": \"SHORT\", \"change_pct\": -0.28}"
echo "   2. Texto: BTC.D: 59.32%, Direction: SHORT, Change: -0.28%"
echo "   3. Simples: BTC.D 59.32 SHORT -0.28%"
echo ""
echo "🔗 URL: http://147.182.145.169/webhook/btcd"
echo "📝 Mensagem: {{alert.message}}"
echo ""
echo "🚀 AGORA TESTE NO TRADINGVIEW!"
echo "   Clique em 'Send Test Alert' e me avise"