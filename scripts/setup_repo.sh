#!/bin/bash

# Script para configurar repositório GitHub e preparar para deploy
# Uso: ./scripts/setup_repo.sh [GITHUB_USER] [REPO_NAME]
# Se não fornecer argumentos, usa os valores padrão configurados

set -e

GITHUB_USER=${1:-"flaviohbonfim"}
REPO_NAME=${2:-"llm-as-a-judge-study"}

echo "🚀 Configurando repositório para LLMs as a Judge Study"
echo ""

# Verifica se git está instalado
if ! command -v git &> /dev/null; then
    echo "❌ Git não está instalado. Por favor, instale o Git primeiro."
    exit 1
fi

# Verifica se estamos em um repositório git
if [ ! -d .git ]; then
    echo "📦 Inicializando repositório Git..."
    git init
    git branch -M main
fi

# Atualiza mkdocs.yml com o nome do usuário
if [ -f mkdocs.yml ]; then
    echo "⚙️  Atualizando mkdocs.yml com suas informações..."
    sed -i.bak "s/SEU_USUARIO/$GITHUB_USER/g" mkdocs.yml
    rm mkdocs.yml.bak 2>/dev/null || true
fi

# Atualiza README.md
if [ -f README.md ]; then
    echo "⚙️  Atualizando README.md com suas informações..."
    sed -i.bak "s/SEU_USUARIO/$GITHUB_USER/g" README.md
    rm README.md.bak 2>/dev/null || true
fi

# Adiciona arquivos
echo "📝 Adicionando arquivos ao Git..."
git add .

# Verifica se há mudanças para commitar
if git diff --staged --quiet; then
    echo "ℹ️  Nenhuma mudança para commitar."
else
    echo "💾 Fazendo commit inicial..."
    git commit -m "docs: Adiciona estudo completo sobre LLMs as a Judge"
fi

# Verifica se o remote já existe
if git remote get-url origin &> /dev/null; then
    echo "ℹ️  Remote 'origin' já configurado."
    REMOTE_URL=$(git remote get-url origin)
    echo "   URL atual: $REMOTE_URL"
else
    echo "🔗 Configurando remote do GitHub..."
    git remote add origin "https://github.com/$GITHUB_USER/$REPO_NAME.git"
fi

echo ""
echo "✅ Configuração concluída!"
echo ""
echo "📋 Próximos passos:"
echo ""
echo "1. Crie o repositório no GitHub:"
echo "   https://github.com/new"
echo "   Nome: $REPO_NAME"
echo ""
echo "2. Faça push para o GitHub:"
echo "   git push -u origin main"
echo ""
echo "3. Escolha uma opção de deploy:"
echo ""
echo "   Opção A - GitBook (Mais fácil):"
echo "   - Acesse: https://www.gitbook.com/"
echo "   - Crie um espaço e importe do GitHub"
echo "   - Veja: docs/DEPLOYMENT_GUIDE.md"
echo ""
echo "   Opção B - GitHub Pages + MkDocs (Recomendado):"
echo "   - Vá em Settings > Pages do repositório"
echo "   - Selecione 'GitHub Actions' como source"
echo "   - O deploy será automático após o push"
echo "   - Veja: docs/DEPLOYMENT_GUIDE.md"
echo ""
echo "📚 Documentação completa: docs/DEPLOYMENT_GUIDE.md"
echo ""

