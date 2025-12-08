# 🚀 Quick Start: LLMs as a Judge

Guia rápido para começar a usar LLM Judge em 5 minutos.

## Pré-requisitos

```bash
# Instalar dependências
poetry add langfuse

# Ou com pip
pip install langfuse
```

## Passo 1: Configuração Básica

```python
from google.adk import Agent, Runner
from langfuse import Langfuse
from examples.llm_judge_implementation import LangfuseLLMJudge

# 1. Configure o judge agent
judge_agent = Agent(
    name="evaluation_judge",
    description="Especialista em avaliar agentes de IA",
    instruction="""
    Você é um juiz especializado em avaliar agentes de IA.
    Sempre forneça avaliações em JSON estruturado com scores, justificativas e recomendações.
    """,
    model="gemini-2.0-flash"  # Recomendado: melhor custo-benefício
)

# 2. Configure Langfuse (opcional, mas recomendado)
langfuse = Langfuse(
    secret_key="sk-lf-...",  # Sua chave secreta
    public_key="pk-lf-...",  # Sua chave pública
    host="https://cloud.langfuse.com"
)

# 3. Crie o judge
runner = Runner()
judge = LangfuseLLMJudge(
    judge_agent=judge_agent,
    runner=runner,
    langfuse_client=langfuse
)
```

## Passo 2: Avaliar uma Resposta

```python
import asyncio

async def avaliar_resposta():
    evaluation = await judge.evaluate_response(
        user_query="O que é Python?",
        agent_response="Python é uma linguagem de programação de alto nível.",
        expected_response="Python é uma linguagem de programação interpretada..."
    )
    
    print(f"✅ Score: {evaluation['score']:.2f}")
    print(f"📝 Justificativa: {evaluation['justification']}")
    print(f"✨ Pontos fortes: {evaluation.get('strengths', [])}")
    print(f"⚠️  Pontos fracos: {evaluation.get('weaknesses', [])}")

# Executar
asyncio.run(avaliar_resposta())
```

## Passo 3: Avaliar Trajetória

```python
async def avaliar_trajetoria():
    trajectory_eval = await judge.evaluate_trajectory(
        expected_trajectory=["search", "retrieve", "generate"],
        actual_trajectory=["search", "retrieve", "generate", "validate"]
    )
    
    print(f"✅ Score da Trajetória: {trajectory_eval['score']:.2f}")
    print(f"📊 Completude: {trajectory_eval.get('completeness', 0):.2f}")
    print(f"⚡ Eficiência: {trajectory_eval.get('efficiency', 0):.2f}")

asyncio.run(avaliar_trajetoria())
```

## Passo 4: Comparar Múltiplas Respostas

```python
async def comparar_respostas():
    comparison = await judge.compare_responses(
        user_query="Explique machine learning",
        responses=[
            {"label": "GPT-4", "response": "Machine learning é..."},
            {"label": "Gemini", "response": "Machine learning é..."},
            {"label": "Claude", "response": "Machine learning é..."}
        ]
    )
    
    print(f"🏆 Melhor resposta: {comparison['winner']}")
    print(f"📊 Scores: {comparison['scores']}")
    print(f"💭 Raciocínio: {comparison['reasoning']}")

asyncio.run(comparar_respostas())
```

## Passo 5: Integrar com Seu Agente

```python
from google.adk import Agent, Runner, Session

# Seu agente
meu_agente = Agent(
    name="meu_agente",
    description="...",
    instruction="...",
    model="gemini-2.0-flash"
)

async def avaliar_meu_agente():
    runner = Runner()
    session = Session()
    
    # Executa seu agente
    user_query = "Qual é a capital do Brasil?"
    response = await runner.run(
        agent=meu_agente,
        session=session,
        user_content=user_query
    )
    
    # Avalia com judge
    evaluation = await judge.evaluate_response(
        user_query=user_query,
        agent_response=response.content
    )
    
    print(f"Resposta do agente: {response.content}")
    print(f"Score: {evaluation['score']:.2f}")
    
    return evaluation

asyncio.run(avaliar_meu_agente())
```

## Exemplo Completo: Pipeline de Avaliação

```python
async def pipeline_completo():
    """Pipeline completo de avaliação"""
    
    # Casos de teste
    test_cases = [
        {
            "user_query": "O que é Python?",
            "expected_response": "Python é uma linguagem de programação..."
        },
        {
            "user_query": "Explique machine learning",
            "expected_response": "Machine learning é um subcampo da IA..."
        }
    ]
    
    results = []
    
    for test_case in test_cases:
        # Executa agente (substitua pelo seu agente real)
        agent_response = "..."  # Resposta do seu agente
        
        # Avalia
        evaluation = await judge.evaluate_response(
            user_query=test_case["user_query"],
            agent_response=agent_response,
            expected_response=test_case.get("expected_response")
        )
        
        results.append({
            "test_case": test_case["user_query"],
            "score": evaluation["score"],
            "evaluation": evaluation
        })
    
    # Resumo
    avg_score = sum(r["score"] for r in results) / len(results)
    print(f"📊 Score Médio: {avg_score:.2f}")
    print(f"✅ Testes Passados: {sum(1 for r in results if r['score'] >= 0.7)}/{len(results)}")
    
    return results

asyncio.run(pipeline_completo())
```

## Configuração Avançada

### Usar Critérios Customizados

```python
custom_criteria = {
    "correctness": "A resposta está correta?",
    "relevance": "A resposta é relevante?",
    "completeness": "A resposta está completa?",
    "clarity": "A resposta é clara?",
    "safety": "A resposta é segura?"
}

judge = LangfuseLLMJudge(
    judge_agent=judge_agent,
    runner=runner,
    langfuse_client=langfuse,
    evaluation_criteria=custom_criteria
)
```

### Usar Modelo Diferente

```python
# Para casos críticos, use modelo mais poderoso
judge_agent_critical = Agent(
    name="evaluation_judge_critical",
    description="...",
    instruction="...",
    model="gemini-2.0-pro"  # ou "gpt-4o"
)
```

### Sem Langfuse (Modo Simples)

```python
from examples.llm_judge_implementation import LLMJudge

# Judge sem Langfuse
judge_simple = LLMJudge(
    judge_agent=judge_agent,
    runner=runner
)
```

## Troubleshooting

### Erro: "Não foi possível extrair JSON"
- O judge pode não estar retornando JSON válido
- Solução: Verifique o prompt do judge agent

### Erro: "Langfuse connection failed"
- Langfuse não está configurado corretamente
- Solução: Use `LLMJudge` sem Langfuse ou verifique credenciais

### Avaliações Inconsistentes
- Modelos podem variar entre execuções
- Solução: Use `temperature=0.0` no judge agent

## Próximos Passos

1. ✅ Leia o estudo completo: `docs/LLMs_as_Judge_Study.md`
2. ✅ Explore exemplos: `examples/llm_judge_implementation.py`
3. ✅ Configure Langfuse para observabilidade
4. ✅ Adapte para seus casos de uso específicos

## Recursos

- 📚 **Estudo Completo**: `docs/LLMs_as_Judge_Study.md`
- 📝 **Resumo Executivo**: `docs/RESUMO_EXECUTIVO_LLMs_Judge.md`
- 💻 **Exemplos**: `examples/`
- ⚙️ **Configurações**: `examples/judge_configs.yaml`

---

**Pronto para começar!** 🚀

