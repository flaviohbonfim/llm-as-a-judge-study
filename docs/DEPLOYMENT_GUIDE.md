# 🚀 Guia de Deploy: Publicando Documentação no GitHub

Este guia mostra como publicar a documentação do estudo LLMs as a Judge no GitHub e visualizá-la como uma página profissional.

## 📋 Opções Disponíveis

### 1. GitBook (Recomendado - Mais Fácil)
✅ Interface visual moderna  
✅ Sincronização automática com GitHub  
✅ Fácil de usar  
⚠️ Requer conta GitBook (gratuita)

### 2. GitHub Pages + MkDocs (Recomendado - Open Source)
✅ Totalmente gratuito  
✅ Controle total  
✅ Customizável  
⚠️ Requer configuração inicial

### 3. Docusaurus (Alternativa)
✅ Moderno e rápido  
✅ Suporte a React  
⚠️ Requer mais configuração

## 🎯 Opção 1: GitBook (Mais Fácil)

### Passo 1: Criar Repositório no GitHub

```bash
# 1. Crie um novo repositório no GitHub
# Acesse: https://github.com/new
# Nome sugerido: llm-as-a-judge-study

# 2. No terminal, navegue até o diretório do projeto
cd llm-as-a-judge-study

# 3. Inicialize git (se ainda não tiver)
git init

# 4. Adicione os arquivos
git add docs/ examples/

# 5. Commit inicial
git commit -m "docs: Adiciona estudo completo sobre LLMs as a Judge"

# 6. Adicione o remote do GitHub
git remote add origin https://github.com/flaviohbonfim/llm-as-a-judge-study.git

# 7. Push para GitHub
git branch -M main
git push -u origin main
```

### Passo 2: Conectar com GitBook

1. **Acesse GitBook**: https://www.gitbook.com/
2. **Crie uma conta** (gratuita)
3. **Crie um novo espaço** (Space)
4. **Escolha "Import from GitHub"**
5. **Conecte seu repositório GitHub**
6. **Selecione o repositório** `llm-as-a-judge-study`
7. **Configure o caminho**: `/docs` (ou raiz se preferir)

### Passo 3: Configurar Estrutura no GitBook

Crie um arquivo `SUMMARY.md` na raiz do repositório para organizar a navegação:

```markdown
# LLMs as a Judge - Estudo Completo

* [Introdução](README.md)
* [Índice](INDEX_LLMs_Judge.md)
* [Quick Start](QUICK_START_JUDGE.md)
* [Resumo Executivo](RESUMO_EXECUTIVO_LLMs_Judge.md)
* [Estudo Completo](LLMs_as_Judge_Study.md)
* [Guia de Deploy](DEPLOYMENT_GUIDE.md)
```

### Passo 4: Sincronização Automática

O GitBook sincroniza automaticamente com o GitHub. Toda vez que você fizer push, a documentação será atualizada.

---

## 🎯 Opção 2: GitHub Pages + MkDocs (Recomendado para Controle Total)

### Passo 1: Criar Repositório no GitHub

```bash
# Mesmo processo da Opção 1
cd llm-as-a-judge-study
git init
git add .
git commit -m "docs: Adiciona estudo completo sobre LLMs as a Judge"
git remote add origin https://github.com/flaviohbonfim/llm-as-a-judge-study.git
git branch -M main
git push -u origin main
```

### Passo 2: Configurar MkDocs

Crie um arquivo `mkdocs.yml` na raiz do projeto:

```yaml
site_name: LLMs as a Judge - Estudo Completo
site_description: Estudo profundo sobre uso de LLMs para avaliar agentes de IA
site_author: Seu Nome
site_url: https://flaviohbonfim.github.io/llm-as-a-judge-study

theme:
  name: material
  palette:
    - scheme: default
      primary: blue
      accent: blue
      toggle:
        icon: material/brightness-7
        name: Switch to dark mode
    - scheme: slate
      primary: blue
      accent: blue
      toggle:
        icon: material/brightness-4
        name: Switch to light mode
  features:
    - navigation.tabs
    - navigation.sections
    - navigation.expand
    - navigation.top
    - search.suggest
    - search.highlight
    - content.code.annotate

markdown_extensions:
  - pymdownx.highlight:
      anchor_linenums: true
  - pymdownx.inlinehilite
  - pymdownx.snippets
  - pymdownx.superfences:
      custom_fences:
        - name: mermaid
          class: mermaid
          format: !!python/name:pymdownx.superfences.fence_code_format
  - admonition
  - pymdownx.details
  - attr_list
  - md_in_html

nav:
  - Início: README.md
  - Índice: docs/INDEX_LLMs_Judge.md
  - Quick Start: docs/QUICK_START_JUDGE.md
  - Resumo Executivo: docs/RESUMO_EXECUTIVO_LLMs_Judge.md
  - Estudo Completo: docs/LLMs_as_Judge_Study.md
  - Guia de Deploy: docs/DEPLOYMENT_GUIDE.md
  - Exemplos:
    - Implementação: examples/llm_judge_implementation.py
    - Templates: examples/judge_prompts_templates.py
    - Configurações: examples/judge_configs.yaml
```

### Passo 3: Instalar Dependências

Crie um arquivo `requirements-docs.txt`:

```txt
mkdocs>=1.5.0
mkdocs-material>=9.0.0
mkdocs-mermaid2-plugin>=1.0.0
```

Instale:

```bash
pip install -r requirements-docs.txt
```

### Passo 4: Testar Localmente

```bash
# Servir localmente
mkdocs serve

# Acesse: http://127.0.0.1:8000
```

### Passo 5: Configurar GitHub Actions

Crie `.github/workflows/deploy.yml`:

```yaml
name: Deploy Docs

on:
  push:
    branches:
      - main
    paths:
      - 'docs/**'
      - 'mkdocs.yml'
      - '.github/workflows/deploy.yml'

permissions:
  contents: write

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      
      - name: Install dependencies
        run: |
          pip install -r requirements-docs.txt
      
      - name: Build docs
        run: mkdocs build
      
      - name: Deploy to GitHub Pages
        uses: peaceiris/actions-gh-pages@v3
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: ./site
```

### Passo 6: Habilitar GitHub Pages

1. Vá em **Settings** do repositório
2. **Pages** → **Source**: Selecione **GitHub Actions**
3. Faça um push para ativar o workflow

### Passo 7: Deploy

```bash
git add .
git commit -m "docs: Configura MkDocs e GitHub Pages"
git push
```

A documentação estará disponível em: `https://flaviohbonfim.github.io/llm-as-a-judge-study`

---

## 🎯 Opção 3: Docusaurus (Alternativa Moderna)

### Passo 1: Instalar Docusaurus

```bash
npx create-docusaurus@latest llms-judge-docs classic
cd llms-judge-docs
```

### Passo 2: Copiar Documentos

```bash
# Copie os arquivos markdown (se necessário)
# cp -r ../llm-as-a-judge-study/docs/* docs/
```

### Passo 3: Configurar

Edite `docusaurus.config.js` para incluir seus documentos.

### Passo 4: Deploy no GitHub Pages

```bash
npm run deploy
```

---

## 📝 Estrutura Recomendada do Repositório

```
llm-as-a-judge-study/
├── .github/
│   └── workflows/
│       └── deploy.yml          # GitHub Actions (se usar MkDocs)
├── docs/
│   ├── README.md
│   ├── INDEX_LLMs_Judge.md
│   ├── QUICK_START_JUDGE.md
│   ├── RESUMO_EXECUTIVO_LLMs_Judge.md
│   ├── LLMs_as_Judge_Study.md
│   └── DEPLOYMENT_GUIDE.md
├── examples/
│   ├── README_JUDGE.md
│   ├── llm_judge_implementation.py
│   ├── judge_prompts_templates.py
│   └── judge_configs.yaml
├── README.md                   # README principal do repositório
├── mkdocs.yml                  # Configuração MkDocs (se usar)
└── requirements-docs.txt       # Dependências (se usar MkDocs)
```

---

## 🎨 Personalização

### GitBook

- Acesse **Settings** → **Appearance** no GitBook
- Customize cores, logo, favicon
- Configure domínio customizado (opcional)

### MkDocs Material

Edite `mkdocs.yml` para personalizar:
- Cores e tema
- Logo e favicon
- Plugins adicionais
- Navegação

---

## 🔄 Atualizações Futuras

### GitBook
```bash
# Simplesmente faça push
git add .
git commit -m "docs: Atualiza documentação"
git push
# GitBook atualiza automaticamente
```

### GitHub Pages + MkDocs
```bash
# Faça push normalmente
git add .
git commit -m "docs: Atualiza documentação"
git push
# GitHub Actions faz o deploy automaticamente
```

---

## 📊 Comparação Rápida

| Recurso | GitBook | MkDocs | Docusaurus |
|---------|---------|--------|------------|
| Facilidade | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐ |
| Customização | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| Custo | Grátis* | Grátis | Grátis |
| Sincronização | Automática | Via CI/CD | Via CI/CD |
| Controle | Médio | Total | Total |

*GitBook tem plano gratuito com limitações

---

## ✅ Checklist Final

- [ ] Repositório criado no GitHub
- [ ] Arquivos commitados e push realizados
- [ ] Documentação configurada (GitBook ou MkDocs)
- [ ] Testado localmente (se aplicável)
- [ ] Deploy realizado
- [ ] Link de acesso funcionando
- [ ] README.md atualizado com link

---

## 🎉 Pronto!

Sua documentação estará disponível publicamente e com visual profissional!

**Recomendação**: Comece com **GitBook** pela facilidade, depois migre para **MkDocs** se precisar de mais controle.

---

**Dúvidas?** Consulte:
- [GitBook Docs](https://docs.gitbook.com/)
- [MkDocs Material](https://squidfunk.github.io/mkdocs-material/)
- [GitHub Pages](https://pages.github.com/)

