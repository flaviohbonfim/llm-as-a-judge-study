# 🎯 LLMs as a Judge - Estudo Completo

> Estudo profundo sobre o uso de Large Language Models (LLMs) para avaliar agentes de IA, com foco em projetos Python usando Google ADK e Langfuse.

[![Documentation](https://img.shields.io/badge/docs-latest-blue.svg)](https://flaviohbonfim.github.io/llm-as-a-judge-study)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

## 📚 Documentação

📖 **[Acesse a Documentação Completa](https://flaviohbonfim.github.io/llm-as-a-judge-study)**

## 🚀 Quick Start

**Novo no tema?** Comece pelo [Quick Start Guide](docs/QUICK_START_JUDGE.md) - você estará avaliando agentes em 5 minutos!

```python
from google.adk import Agent, Runner
from examples.llm_judge_implementation import LLMJudge

# Configure o judge
judge_agent = Agent(
    name="evaluation_judge",
    description="Especialista em avaliar agentes de IA",
    instruction="Você é um juiz especializado...",
    model="gemini-2.0-flash"
)

judge = LLMJudge(
    judge_agent=judge_agent,
    runner=Runner()
)

# Avalie uma resposta
evaluation = await judge.evaluate_response(
    user_query="O que é Python?",
    agent_response="Python é uma linguagem de programação..."
)
```

## 📖 Conteúdo

### Documentação Principal

- **[Quick Start Guide](docs/QUICK_START_JUDGE.md)** ⚡ - Comece em 5 minutos
- **[Resumo Executivo](docs/RESUMO_EXECUTIVO_LLMs_Judge.md)** 📊 - Principais conclusões
- **[Estudo Completo](docs/LLMs_as_Judge_Study.md)** 📖 - Estudo profundo e abrangente
- **[Índice Completo](docs/INDEX_LLMs_Judge.md)** 🗂️ - Navegação e organização
- **[Guia de Deploy](docs/DEPLOYMENT_GUIDE.md)** 🚀 - Como publicar no GitHub/GitBook

### Código e Exemplos

- **[Implementação Completa](examples/llm_judge_implementation.py)** - Classes Python prontas
- **[Templates de Prompts](examples/judge_prompts_templates.py)** - Templates reutilizáveis
- **[Configurações](examples/judge_configs.yaml)** - Configurações recomendadas

## 🎯 Principais Conclusões

### Modelos Recomendados

- **Para uso geral**: Gemini 2.0 Flash (melhor custo-benefício, integração nativa com ADK)
- **Para casos críticos**: GPT-4o ou Gemini 2.0 Pro
- **Para larga escala**: Claude 3 Haiku ou Gemini 2.0 Flash

### Tipos de Avaliação

1. **Trajetória** - Avalia sequência de ações do agente
2. **Qualidade de Resposta** - Avalia correção, relevância, completude
3. **Comparativa** - Compara e ranqueia múltiplas respostas
4. **Comportamental** - Avalia alinhamento e ética

## 🛠️ Instalação

```bash
# Clone o repositório
git clone https://github.com/flaviohbonfim/llm-as-a-judge-study.git
cd llm-as-a-judge-study

# Instale dependências
pip install -r requirements-docs.txt

# Para desenvolvimento
pip install google-adk langfuse
```

## 📊 Estrutura do Projeto

```
llm-as-a-judge-study/
├── docs/                          # Documentação completa
│   ├── README.md
│   ├── INDEX_LLMs_Judge.md
│   ├── QUICK_START_JUDGE.md
│   ├── RESUMO_EXECUTIVO_LLMs_Judge.md
│   ├── LLMs_as_Judge_Study.md
│   └── DEPLOYMENT_GUIDE.md
├── examples/                      # Exemplos práticos
│   ├── README_JUDGE.md
│   ├── llm_judge_implementation.py
│   ├── judge_prompts_templates.py
│   └── judge_configs.yaml
├── scripts/                       # Scripts auxiliares
│   └── setup_repo.sh
├── .github/
│   └── workflows/
│       └── deploy.yml             # Deploy automático
├── mkdocs.yml                     # Configuração MkDocs
├── requirements-docs.txt           # Dependências
├── COMANDOS_RAPIDOS.md            # Comandos prontos
└── README.md                       # Este arquivo
```

## 🚀 Deploy da Documentação

Para publicar a documentação como site:

1. **GitBook** (Mais fácil): Veja [Guia de Deploy](docs/DEPLOYMENT_GUIDE.md#opção-1-gitbook-mais-fácil)
2. **GitHub Pages + MkDocs** (Recomendado): Veja [Guia de Deploy](docs/DEPLOYMENT_GUIDE.md#opção-2-github-pages-mkdocs-recomendado-para-controle-total)

**Comandos rápidos**: Veja [COMANDOS_RAPIDOS.md](COMANDOS_RAPIDOS.md)

## 🤝 Contribuindo

Contribuições são bem-vindas! Por favor:

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

## 🙏 Agradecimentos

- Google ADK Team
- Langfuse Team
- Comunidade open source

## 📞 Contato

Para dúvidas ou sugestões, abra uma [issue](https://github.com/flaviohbonfim/llm-as-a-judge-study/issues).

---

**Desenvolvido com ❤️ para a comunidade de IA**

