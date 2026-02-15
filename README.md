# 🦅 Bot Sniper Bybit v2.4.0 - Continuous Learning Edition

Um sistema de trading algorítmico de alta performance para o mercado de futuros de criptomoedas, equipado com **Inteligência Artificial que aprende continuamente** com os próprios resultados. Arquitetura modular, gestão de risco profissional, validação por IA de visão e sistema de feedback loop completo.

## 🧠 Nova Era: IA que Aprende com Experiência

### Sistema de Aprendizado Contínuo (v2.4.0)
*   **Feedback Loop Completo:** Conecta predições da IA com resultados reais de P&L
*   **Treinamento Incremental:** Modelo evolui automaticamente preservando conhecimento anterior  
*   **Confiança Adaptiva:** IA ajusta confiança dos padrões baseado em performance histórica
*   **Auto-Otimização:** Padrões ruins perdem peso, bons ganham força automaticamente

### Performance Tracking & Analytics
*   **Base de Performance:** 6,800+ amostras coletadas com resultados reais
*   **Métricas por Padrão:** Taxa de sucesso, P&L médio, duração por tipo de setup
*   **Ajuste Automático:** Pesos dos padrões se adaptam baseado em histórico de acertos
*   **Compactação Inteligente:** Preserva dados importantes, arquiva histórico antigo

## 🚀 Funcionalidades Principais

### Core System
*   **Arquitetura "Hunter-Killer":**
    *   `Scanner`: Varredura contínua de 30+ pares em múltiplos timeframes + **coleta 24/7** para IA
    *   `Monitor`: Vigia de preço "Just-in-Time" com **validação por Vision AI**
    *   `Executor`: Módulo "Fire-and-Forget" com **proteção anti-duplicação** e feedback automático

### 🛡️ Risk Management & Capital Defense
*   **Gestão de Risco Profissional:**
    *   Cálculo de lote baseado em risco fixo (1.5-5% da banca por trade)
    *   **Proteção contra múltiplas entradas** no mesmo ativo (bug corrigido v2.4.0)
*   **Break-Even Automático:** Move o Stop para entrada ao atingir 25% do alvo
*   **Proteção de Liquidação:** Ajuste automático de Stop Loss se muito próximo da liquidação
*   **Filtro de Correlação:** Sistema BTC/BTC.D com 5 cenários de mercado

### 🎯 Vision AI Integration (v2.3.0 → v2.4.0)
*   **Validação Gráfica:** Google Gemini/GPT-4o analisa gráficos antes de aprovar trades
*   **Confiança Melhorada:** Sistema combina confiança técnica + histórico de performance
*   **Rejeição Inteligente:** IA identifica "falsos rompimentos" e remove da watchlist
*   **Feedback Contínuo:** Cada resultado real alimenta o modelo de confiança

## ⚡ NEW in v2.4.0 - Continuous Learning System

### 🔄 Sistema de Feedback Loop Completo

#### Brain Performance Tracker
*   **Conexão Predição ↔ Resultado:** Liga cada análise da IA com o P&L real do trade
*   **Métricas Detalhadas:** Success rate, P&L médio, duração por padrão
*   **Histórico Completo:** Base de dados rastreando 100+ trades com performance real

#### Continuous Learning Engine  
*   **Treinamento Incremental:** Modelo treina automaticamente a cada 50+ novos dados
*   **Preservação de Conhecimento:** Nunca "esquece" aprendizado anterior
*   **Adaptação de Pesos:** Padrões com baixa performance perdem influência automaticamente
*   **Validação de Melhorias:** Só aplica novos modelos se houver melhoria real (>5%)

#### Enhanced Vision Confidence
*   **Multiplicadores Adaptativos:** IA ajusta confiança baseada em histórico do padrão
*   **Exemplo:** BANDEIRA_ALTA que falhou 3x seguidas tem confiança reduzida para 0.3x
*   **Auto-Correção:** Padrões com alta taxa de sucesso ganham boost de confiança (1.5x)

### 📊 Coleta Contínua de Dados
*   **Modo 24/7:** Scanner coleta dados mesmo com watchlist cheia (não para mais)
*   **Separação Lógica:** Coleta para IA ≠ Trading ativo
*   **Volume Massivo:** ~100-200 novas amostras por dia vs. ~10-20 anterior
*   **Rate Limit Inteligente:** Delays dinâmicos para não sobrecarregar APIs

### 🔧 Sistema de Manutenção Automática
*   **Compactação Inteligente:** Preserva dados válidos, arquiva inválidos antigos
*   **Limpeza de Imagens:** Remove gráficos antigos mantendo os de padrões válidos  
*   **Auto-Execução:** Roda automaticamente a cada 12h sem intervenção
*   **Rotação de Logs:** Histórico preservado mas compactado para economizar espaço

## 📈 Padrões Suportados & Performance

| Padrão | Amostras | Taxa Sucesso* | Confiança Base | Status IA |
|--------|----------|---------------|----------------|-----------|
| OCO | 1,987 | ~65% | 0.80 | ✅ Otimizado |
| TOPO_DUPLO | 1,384 | ~58% | 0.75 | ✅ Ajustado |
| CUNHA_ASCENDENTE | 1,155 | ~52% | 0.68 | ⚖️ Monitorado |
| OCO_INVERTIDO | 906 | ~61% | 0.80 | ✅ Otimizado |
| FUNDO_DUPLO | 654 | ~55% | 0.75 | ✅ Ajustado |
| BANDEIRA_ALTA | 15 | ~40%** | 0.70→0.42 | ⚠️ Penalizado |
| TRIANGULO_* | 510 | ~49% | 0.72 | ⚖️ Em Análise |

*\* Performance histórica baseada em Vision AI + resultados reais*  
*\*\* BANDEIRA_ALTA sofreu penalização após incidente AAVE (-10 USDT)*

## 🎯 Fluxo Operacional Atualizado

```
📡 Scanner (24/7)
    ├── Detecta Padrão
    ├── 🧠 SEMPRE: Coleta para IA (brain_collector)
    ├── ✅ Se Watchlist tem slot: Envia para Monitor
    └── ❌ Se cheia: Só coleta (não tradea)

👁️ Monitor + Vision AI
    ├── Recebe padrão da watchlist
    ├── Gera gráfico automaticamente  
    ├── 🤖 IA analisa: VALID/INVALID (confiança melhorada)
    ├── ✅ Se VALID: Mantém na watchlist
    └── ❌ Se INVALID: Remove + blacklist 6h

⚡ Executor (Fire & Forget)
    ├── 🛡️ Verifica: Posição já existe? (anti-duplicação)
    ├── 💰 Calcula: Tamanho baseado em risco
    ├── 🎯 Executa: Ordem a mercado
    ├── 🛡️ Define: Stop Loss + Take Profit
    └── 📊 Registra: Feedback para IA (ao fechar)

🧠 Continuous Learning (Background)
    ├── 🔄 A cada 12h: Processa novos feedbacks
    ├── 🎯 A cada 50+ dados: Retreina modelo
    ├── 📊 Atualiza: Pesos e confiança por padrão
    └── 🗄️ Arquiva: Dados antigos mantendo essenciais
```

## ⚙️ Configuração & Setup

### Pré-requisitos
*   Python 3.8+
*   Chaves API Bybit (Futures)
*   Google API Key (Gemini Pro Vision)
*   Servidor com IP público (para webhooks TradingView)

### Instalação Rápida
```bash
git clone https://github.com/bernini10/bot_sniper_bybit.git
cd bot_sniper_bybit
pip install -r requirements.txt

# Configurar chaves (copie .env.example para .env)
cp .env.example .env
nano .env

# Inicializar sistema de IA
python3 brain_initialization.py --mode full

# Iniciar sistema completo
./restart_system_v2.3.1.sh
```

### Configuração do Vision AI
1. **Google API:** Obtenha chave em [Google AI Studio](https://makersuite.google.com/app/apikey)
2. **Adicione ao .env:**
   ```
   GOOGLE_API_KEY=sua_chave_aqui
   ```
3. **Teste:** `python3 vision_validator.py` (deve processar amostras pendentes)

## 📊 Dashboard & Monitoramento

### Interface Web (Dashboard v2.3.0)
*   **URL:** `http://SEU_IP:5000`
*   **Watchlist:** Padrões ativos com status da Vision AI
*   **Performance:** Métricas de P&L por padrão
*   **Trades:** Histórico completo com detalhes
*   **Vision:** Seletor manual de validação por IA

### Logs & Debug
```bash
# Logs principais
tail -f scanner_bybit.log      # Padrões detectados
tail -f monitor_bybit.log      # Validações da IA
tail -f vision.log             # Análises gráficas
tail -f brain_initialization.log  # Sistema de aprendizado

# Status do sistema
python3 brain_initialization.py --mode status
```

### Métricas de Performance
```bash
# Relatório completo de IA
python3 -c "
from brain_performance_tracker import performance_tracker
summary = performance_tracker.get_performance_summary()
print(f'Taxa Sucesso: {summary[\"general\"][\"success_rate\"]:.1%}')
print(f'P&L Total: {summary[\"general\"][\"total_pnl\"]:.3f} USDT')
print(f'Feedbacks: {summary[\"general\"][\"total_feedback\"]}')
"
```

## 🔄 Próximos Passos (Roadmap v2.5.0+)

### 🎯 Em Desenvolvimento
*   **Backtesting Inteligente:** Simulação usando dados históricos + IA treinada
*   **Multi-Exchange:** Expansão para Binance, OKX com arbitragem de padrões
*   **Risk Scaling:** Aumento automático de posição baseado em streak de acertos
*   **Portfolio Balance:** Diversificação automática entre setores (DeFi, L1, Gaming, etc)

### 🧠 Melhorias de IA
*   **Vision AI 2.0:** Modelo próprio treinado especificamente em padrões crypto
*   **Sentiment Analysis:** Integração com feeds de notícias e redes sociais
*   **Market Regime Detection:** Identificação automática de bull/bear/crab markets
*   **Ensemble Models:** Combinação de múltiplos modelos para maior precisão

### ⚡ Performance & Scale
*   **GPU Acceleration:** Treinamento de modelos em GPU para responses mais rápidas
*   **Distributed Architecture:** Multi-nodes para maior capacidade de processamento
*   **Real-Time WebSocket:** Atualizações instantâneas no dashboard
*   **Mobile Alerts:** App mobile para notificações push

### 🛡️ Risk & Safety
*   **Stress Testing:** Simulação de cenários extremos de mercado
*   **Position Correlation:** Análise de correlação entre posições ativas
*   **Dynamic Risk:** Ajuste automático de risco baseado em volatilidade
*   **Emergency Protocols:** Fechamento automático em cenários de crise

## 🏆 Resultados & Conquistas

### v2.4.0 Achievements
*   ✅ **Bug Crítico Resolvido:** Múltiplas entradas no mesmo ativo (caso AAVE)
*   ✅ **IA Implementada:** Sistema de feedback loop funcionando 24/7
*   ✅ **Performance Tracking:** 6,874+ amostras com resultados reais
*   ✅ **Auto-Otimização:** Padrões se ajustam automaticamente baseado em performance
*   ✅ **Coleta Massiva:** 10x mais dados coletados para treinamento da IA

### Próximos Milestones
*   🎯 **1,000 Feedbacks:** Primeira grande análise de performance (ETA: 2 semanas)
*   🎯 **Modelo v2.0.0:** Primeiro retreino significativo com performance melhorada
*   🎯 **Taxa 70%+:** Objetivo de taxa de sucesso acima de 70% em padrões principais
*   🎯 **ROI Tracking:** Implementação de tracking de ROI por período

## 📞 Suporte & Comunidade

*   **GitHub Issues:** [Reportar bugs/sugestões](https://github.com/bernini10/bot_sniper_bybit/issues)
*   **Documentação:** Consulte os arquivos `.md` para detalhes técnicos
*   **Updates:** Acompanhe releases no GitHub para novas versões

---

## ⚠️ Disclaimer

Este software é fornecido "como está" para fins educacionais e de pesquisa. Trading de criptomoedas envolve risco significativo de perda financeira. Use apenas capital que pode perder. Teste sempre em conta demo primeiro. Os desenvolvedores não se responsabilizam por perdas financeiras.

**Versão:** v2.4.0-continuous-learning-system  
**Última Atualização:** Fevereiro 2026  
**Licença:** MIT  
**Python:** 3.8+  
**Status:** 🟢 Produção Estável com IA Ativa