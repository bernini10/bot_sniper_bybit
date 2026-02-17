#!/bin/bash
# Script para preparar publicação do bot_sniper_AI

echo "🚀 PREPARANDO PUBLICAÇÃO DO bot_sniper_AI"
echo "=========================================="

echo ""
echo "🎯 ETAPA 1: ATUALIZAR REPOSITÓRIO LOCAL"
echo "---------------------------------------"

# 1. Substituir README antigo pelo novo
if [ -f "README_NEW.md" ]; then
    echo "📝 Atualizando README.md..."
    cp README_NEW.md README.md
    echo "✅ README atualizado com badges e nova estrutura"
else
    echo "⚠️  README_NEW.md não encontrado"
fi

# 2. Adicionar todos os novos arquivos
echo "📁 Adicionando arquivos de configuração GitHub..."
git add .github/ CONTRIBUTING.md CODE_OF_CONDUCT.md README.md

# 3. Verificar se há mudanças
echo "🔍 Verificando mudanças..."
CHANGES=$(git status --porcelain | wc -l)
if [ "$CHANGES" -gt 0 ]; then
    echo "📝 Criando commit de preparação..."
    git commit -m "chore: Prepare repository for community launch
    
    🎯 ADICIONADO:
    • Professional README with badges
    • GitHub issue templates (bug, feature, question)
    • Pull Request template
    • CONTRIBUTING.md guidelines
    • CODE_OF_CONDUCT.md
    • Reddit post ready for publication
    
    🚀 PREPARADO PARA:
    • Community engagement
    • Contributor onboarding
    • Sponsorship opportunities
    • Multi-exchange expansion"
    
    echo "✅ Commit criado"
else
    echo "ℹ️  Nenhuma mudança para commitar"
fi

echo ""
echo "🎯 ETAPA 2: ENVIAR PARA GITHUB"
echo "------------------------------"
echo "📤 Enviando mudanças para GitHub..."
git push origin main
echo "✅ Mudanças enviadas"

echo ""
echo "🎯 ETAPA 3: VERIFICAR STATUS"
echo "---------------------------"
echo "🌐 Repositório: https://github.com/bernini10/bot_sniper_AI"
echo "📊 Para verificar:"
echo "   1. README com badges aparece corretamente"
echo "   2. Issue templates estão disponíveis"
echo "   3. Contributing guidelines visíveis"

echo ""
echo "🎯 ETAPA 4: POSTAR NO REDDIT"
echo "---------------------------"
echo "📝 Post pronto em: REDDIT_POST_READY.md"
echo ""
echo "📋 INSTRUÇÕES PARA POSTAR:"
echo "   1. Criar conta no Reddit (se não tiver)"
echo "   2. Ir para: https://www.reddit.com/r/algotrading/submit"
echo "   3. Título: Copiar de REDDIT_POST_READY.md"
echo "   4. Conteúdo: Copiar todo o conteúdo do arquivo"
echo "   5. Flair: 'Showcase' ou 'Open Source'"
echo "   6. Postar e engajar com comentários"
echo ""
echo "💡 DICAS PARA REDDIT:"
echo "   • Responder a todos os comentários rapidamente"
echo "   • Ser transparente sobre limitações"
echo "   • Oferecer ajuda para quem quer testar"
echo "   • Compartilhar em outros subreddits relevantes:"
echo "     - r/MachineLearning"
echo "     - r/Python"
echo "     - r/opensource"
echo "     - r/cryptocurrency"

echo ""
echo "🎯 ETAPA 5: ATIVAR FEATURES GITHUB"
echo "---------------------------------"
echo "📋 FEATURES PARA ATIVAR MANUALMENTE:"
echo "   1. GitHub Discussions:"
echo "      Settings → General → Features → Discussions"
echo ""
echo "   2. GitHub Projects:"
echo "      Ir para 'Projects' tab → New project"
echo ""
echo "   3. GitHub Wiki:"
echo "      Settings → General → Features → Wiki"
echo ""
echo "   4. GitHub Pages (opcional):"
echo "      Settings → Pages → Source: main branch /docs folder"
echo ""
echo "   5. GitHub Sponsors (se elegível):"
echo "      https://github.com/sponsors/bernini10"

echo ""
echo "🎯 ETAPA 6: MONITORAR ENGAGEMENT"
echo "-------------------------------"
echo "📊 METRICS PARA ACOMPANHAR:"
echo "   • Stars (alvo: 100+ em 30 dias)"
echo "   • Forks (alvo: 20+ em 30 dias)"
echo "   • Issues/PRs abertos"
echo "   • Discussions ativas"
echo "   • Clone traffic (em Insights → Traffic)"

echo ""
echo "✅ PREPARAÇÃO COMPLETA!"
echo "======================="
echo ""
echo "📋 RESUMO DO QUE FOI PREPARADO:"
echo "   1. ✅ README profissional com badges"
echo "   2. ✅ Templates de issue (bug, feature, question)"
echo "   3. ✅ Pull Request template"
echo "   4. ✅ CONTRIBUTING.md guidelines"
echo "   5. ✅ CODE_OF_CONDUCT.md"
echo "   6. ✅ Post Reddit pronto para publicar"
echo "   7. ✅ Script de publicação automática"
echo ""
echo "🚀 PRÓXIMOS PASSOS:"
echo "   1. Executar: ./publish_preparation.sh"
echo "   2. Postar no Reddit usando REDDIT_POST_READY.md"
echo "   3. Ativar GitHub Discussions/Projects"
echo "   4. Engajar com a comunidade"
echo "   5. Monitorar métricas e ajustar estratégia"
echo ""
echo "🎯 BOA SORTE COM O LANÇAMENTO!"
