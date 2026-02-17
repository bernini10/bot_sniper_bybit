# 🐛 DIAGNÓSTICO: BUG DIREÇÃO LONG/SHORT

## 🎯 PROBLEMA
- **Site/dashboard mostra:** LONG
- **Corretora (Bybit) executa:** SHORT
- **Resultado:** Operação oposta ao padrão analisado

## 🔍 CAUSA RAIZ (INVESTIGAÇÃO INICIAL)

### 1. FLUXO ATUAL DE DIREÇÃO:
```
Padrão detectado → Vision AI valida → Watchlist (direção) → Executor (trade) → Dashboard (display)
```

### 2. PONTOS DE FALHA POSSÍVEIS:

#### A) WATCHLIST (watchlist.json)
- Direção armazenada pode estar errada
- Padrão → direção mapeamento incorreto

#### B) EXECUTOR (bot_executor.py)
- Lógica de direção invertida
- Não está lendo direção do padrão corretamente
- Transformação LONG↔SHORT bugada

#### C) DASHBOARD (dashboard_server.py)
- Display incorreto (só visual)
- Lê de fonte diferente do executor

#### D) VISION AI
- Retorna direção errada para padrão
- Mas validações mostram "VALID" com confiança alta

## 🎯 EVIDÊNCIAS COLETADAS

### 1. Watchlist atual:
(Precisa verificar conteúdo real)

### 2. Logs executor:
(Precisa analisar entradas recentes)

### 3. Código bot_executor.py:
- Função `execute_trade` usa `direction` parameter
- Precisa verificar origem desse `direction`

### 4. Backup corrigido:
- `bot_executor_v2_fixed.py` existe (correção anterior)
- Precisa comparar diferenças

## 🔧 SOLUÇÃO PROPOSTA

### FASE 1: DIAGNÓSTICO PRECISO
1. Verificar watchlist.json atual
2. Analisar logs de trades recentes
3. Identificar EXATAMENTE onde direção é invertida

### FASE 2: CORREÇÃO
1. Garantir que direção vem do PADRÃO (não lógica)
2. Remover qualquer transformação LONG↔SHORT
3. Validar com novo trade

### FASE 3: VERIFICAÇÃO
1. Aguardar 10 minutos após correção
2. Verificar site vs corretora
3. Repetir até 100% correto

## 🚀 AÇÃO IMEDIATA

### 1. ANALISAR TRADE ATUAL:
```python
# Verificar:
# - Qual padrão foi detectado
# - Qual direção o padrão indica
# - Qual direção foi executada
# - Qual direção o dashboard mostra
```

### 2. CORRIGIR MAPEAMENTO PADRÃO→DIREÇÃO:
```python
# Garantir que:
# Padrão de alta (Bullish) → LONG
# Padrão de baixa (Bearish) → SHORT
# Sem inversões ou "lógica inteligente"
```

### 3. IMPLEMENTAR VALIDAÇÃO:
```python
# Antes de executar trade:
# 1. Ler direção do padrão
# 2. Confirmar com Vision AI
# 3. Executar EXATAMENTE essa direção
# 4. Logar tudo para auditoria
```

## 📊 PRÓXIMOS PASSOS

1. **Agora:** Analisar watchlist e logs
2. **5 min:** Identificar ponto exato do bug
3. **10 min:** Implementar correção
4. **20 min:** Testar com monitoramento
5. **30 min:** Verificar site vs corretora
6. **Contínuo:** Monitorar novas ordens

## ⚠️ RISCOS

- **Trade aberto agora:** Pode estar na direção errada
- **Correção:** Pode afetar trades em andamento
- **Dashboard:** Pode mostrar informação desatualizada

## ✅ CRITÉRIO DE SUCESSO

- Site e corretora mostram MESMA direção
- Direção corresponde ao PADRÃO analisado
- Novas ordens seguem padrão corretamente
- Sistema estável após correção
