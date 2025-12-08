# Exemplos de Implementação: LLMs as a Judge

Este diretório contém exemplos práticos de implementação de LLM Judge para avaliação de agentes ADK.

## Arquivos

- `llm_judge_implementation.py`: Implementação completa das classes `LLMJudge` e `LangfuseLLMJudge`
- `judge_prompts_templates.py`: Templates de prompts para diferentes tipos de avaliação
- `judge_configs.yaml`: Configurações recomendadas para diferentes cenários

## Uso Rápido

### 1. Instalação de Dependências

```bash
poetry add langfuse
```

### 2. Configuração Básica

```python
from google.adk import Agent, Runner
from langfuse import Langfuse
from examples.llm_judge_implementation import LangfuseLLMJudge

# Configurar judge agent
judge_agent = Agent(
    name="evaluation_judge",
    description="Especialista em avaliar agentes de IA",
    instruction="Você é um juiz especializado...",
    model="gemini-2.0-flash"
)

# Configurar Langfuse
langfuse = Langfuse(
    secret_key="your-secret-key",
    public_key="your-public-key",
    host="https://cloud.langfuse.com"
)

# Criar judge
judge = LangfuseLLMJudge(
    judge_agent=judge_agent,
    runner=Runner(),
    langfuse_client=langfuse
)
```

### 3. Avaliar Resposta

```python
evaluation = await judge.evaluate_response(
    user_query="O que é Python?",
    agent_response="Python é uma linguagem de programação...",
    expected_response="Python é uma linguagem interpretada..."
)

print(f"Score: {evaluation['score']}")
print(f"Justificação: {evaluation['justification']}")
```

### 4. Avaliar Trajetória

```python
trajectory_eval = await judge.evaluate_trajectory(
    expected_trajectory=["search", "retrieve", "generate"],
    actual_trajectory=["search", "retrieve", "generate", "validate"]
)
```

### 5. Comparar Respostas

```python
comparison = await judge.compare_responses(
    user_query="Explique machine learning",
    responses=[
        {"label": "GPT-4", "response": "..."},
        {"label": "Gemini", "response": "..."}
    ]
)
```

## Integração com ADK

### Usando com AgentEvaluator

```python
from google.adk.evaluation import AgentEvaluator
from examples.llm_judge_implementation import LLMJudge

class CustomEvaluator(AgentEvaluator):
    def __init__(self, agent, judge: LLMJudge):
        super().__init__(agent)
        self.judge = judge
    
    async def evaluate_with_judge(self, test_cases):
        results = []
        for test_case in test_cases:
            # Executa agente
            agent_result = await self._run_agent(test_case)
            
            # Avalia com judge
            eval_result = await self.judge.evaluate_response(
                user_query=test_case["user_query"],
                agent_response=agent_result["response"]
            )
            
            results.append(eval_result)
        return results
```

## Templates de Prompts

Use os templates pré-configurados:

```python
from examples.judge_prompts_templates import JudgePromptTemplates

templates = JudgePromptTemplates()

# Avaliação de resposta
prompt = templates.response_quality(
    user_query="...",
    agent_response="...",
    expected_response="..."
)

# Avaliação de código
prompt = templates.code_quality(
    user_query="...",
    code="...",
    language="python"
)

# Avaliação RAG
prompt = templates.rag_quality(
    user_query="...",
    agent_response="...",
    sources=[...]
)
```

## Configurações

Carregue configurações do arquivo YAML:

```python
import yaml

with open("examples/judge_configs.yaml") as f:
    config = yaml.safe_load(f)

# Usar configurações
model_name = config["models"]["primary"]["name"]
criteria = config["evaluation_criteria"]["response_quality"]
```

## Próximos Passos

1. Leia o estudo completo: `docs/LLMs_as_Judge_Study.md`
2. Experimente os exemplos básicos
3. Adapte para seus casos de uso específicos
4. Integre com seu pipeline de avaliação
5. Monitore performance e custos via Langfuse

## Recursos

- [Documentação do Google ADK](https://github.com/google/labs-adk)
- [Documentação do Langfuse](https://langfuse.com/docs)
- [Estudo Completo](../docs/LLMs_as_Judge_Study.md)

