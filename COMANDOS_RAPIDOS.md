# ⚡ Comandos Rápidos - Deploy da Documentação

Guia rápido com comandos prontos para copiar e colar.

## 🚀 Opção 1: GitBook (Mais Fácil)

### 1. Criar Repositório no GitHub

```bash
# Navegue até o diretório do projeto
cd llm-as-a-judge-study

# Inicialize git (se ainda não tiver)
git init
git branch -M main

# Adicione arquivos
git add .

# Commit inicial
git commit -m "docs: Adiciona estudo completo sobre LLMs as a Judge"

# Adicione seu repositório GitHub
git remote add origin https://github.com/flaviohbonfim/llm-as-a-judge-study.git

# Push
git push -u origin main
```

### 2. Conectar com GitBook

1. Acesse: https://www.gitbook.com/
2. Crie conta (gratuita)
3. Crie novo espaço → "Import from GitHub"
4. Conecte seu repositório
5. Pronto! 🎉

---

## 🚀 Opção 2: GitHub Pages + MkDocs (Recomendado)

### 1. Usar Script Automático

```bash
# Execute o script helper (já configurado com suas informações)
./scripts/setup_repo.sh

# Siga as instruções exibidas
```

### 2. Configuração Manual

```bash
# 1. Instalar dependências
pip install -r requirements-docs.txt

# 2. Testar localmente
mkdocs serve
# Acesse: http://127.0.0.1:8000

# 3. Inicializar git (se ainda não tiver)
git init
git branch -M main

# 4. Adicionar arquivos
git add .

# 5. Commit
git commit -m "docs: Adiciona estudo completo sobre LLMs as a Judge"

# 6. Adicionar remote
git remote add origin https://github.com/flaviohbonfim/llm-as-a-judge-study.git

# 7. Push
git push -u origin main

# 8. Habilitar GitHub Pages
# Vá em: Settings > Pages > Source: GitHub Actions
# O deploy será automático!
```

### 3. Atualizar Informações no mkdocs.yml

Antes de fazer push, atualize no `mkdocs.yml`:

```yaml
site_url: https://flaviohbonfim.github.io/llm-as-a-judge-study
repo_name: flaviohbonfim/llm-as-a-judge-study
repo_url: https://github.com/flaviohbonfim/llm-as-a-judge-study
```

E no `README.md`:

```markdown
[![Documentation](https://img.shields.io/badge/docs-latest-blue.svg)](https://flaviohbonfim.github.io/llm-as-a-judge-study)
```

---

## 📝 Comandos Úteis

### Verificar Status

```bash
# Ver status do git
git status

# Ver remotes configurados
git remote -v

# Ver branches
git branch
```

### Atualizar Documentação

```bash
# Após fazer mudanças
git add .
git commit -m "docs: Atualiza documentação"
git push

# GitBook: atualiza automaticamente
# GitHub Pages: deploy automático via Actions
```

### Testar MkDocs Localmente

```bash
# Servir localmente
mkdocs serve

# Build para produção
mkdocs build

# Verificar erros
mkdocs build --strict
```

### Ver Logs do Deploy (GitHub Actions)

```bash
# Acesse no GitHub:
# Actions > Deploy Docs > Ver logs
```

---

## 🔧 Troubleshooting

### Erro: "remote origin already exists"

```bash
# Remover remote existente
git remote remove origin

# Adicionar novamente
git remote add origin https://github.com/flaviohbonfim/llm-as-a-judge-study.git
```

### Erro: "mkdocs: command not found"

```bash
# Instalar dependências
pip install -r requirements-docs.txt

# Ou instalar globalmente
pip install mkdocs mkdocs-material
```

### Erro no Deploy do GitHub Actions

1. Vá em **Settings > Pages**
2. Verifique se **Source** está como **GitHub Actions**
3. Veja os logs em **Actions** para detalhes do erro

### GitBook não sincroniza

1. Verifique conexão GitHub no GitBook
2. Vá em **Settings > Integrations**
3. Reconecte o GitHub se necessário

---

## ✅ Checklist Rápido

- [ ] Repositório criado no GitHub
- [ ] `mkdocs.yml` atualizado com seu usuário/repo
- [ ] `README.md` atualizado com links corretos
- [ ] Arquivos commitados
- [ ] Push realizado
- [ ] GitBook conectado OU GitHub Pages habilitado
- [ ] Documentação acessível online

---

## 🎯 Links Úteis

- **Criar Repositório**: https://github.com/new
- **GitBook**: https://www.gitbook.com/
- **GitHub Pages**: Settings > Pages do seu repositório
- **MkDocs Material**: https://squidfunk.github.io/mkdocs-material/

---

**Dúvidas?** Consulte o [Guia de Deploy Completo](docs/DEPLOYMENT_GUIDE.md)

