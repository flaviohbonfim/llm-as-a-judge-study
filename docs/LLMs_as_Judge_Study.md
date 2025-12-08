# 🎯 Estudo Profundo: LLMs as a Judge
## Identificando os Melhores Tipos de LLMs para Avaliação de Agentes

**Data:** 2024  
**Contexto:** Projetos Python com Google ADK e Langfuse  
**Objetivo:** Identificar os melhores tipos de LLMs para atuar como juízes na avaliação de agentes de IA

---

## 📋 Sumário Executivo

Este documento apresenta um estudo abrangente sobre o uso de Large Language Models (LLMs) como juízes (judges) na avaliação de agentes de IA. O estudo foca em:

- **Conceito de LLMs as a Judge**: Modelos que avaliam a qualidade de respostas, trajetórias e comportamento de agentes
- **Tipos de Avaliação**: Trajetória de ferramentas, qualidade de resposta, comportamento do agente
- **Modelos Recomendados**: Análise comparativa de diferentes LLMs para função de judge
- **Integração Prática**: Como integrar judges com Google ADK e Langfuse
- **Métricas e Benchmarks**: Como medir a eficácia dos judges
- **Melhores Práticas**: Padrões e recomendações para implementação

---

## 1. Introdução ao Conceito: LLMs as a Judge

### 1.1 O que são LLMs as a Judge?

**LLMs as a Judge** é uma técnica onde um modelo de linguagem grande é usado para avaliar a qualidade, correção e adequação de respostas geradas por outros modelos ou agentes. Em vez de usar métricas tradicionais baseadas em regras ou ground truth humano, o judge LLM atua como um avaliador inteligente que pode:

- Avaliar a qualidade semântica de respostas
- Comparar múltiplas respostas e ranquear
- Avaliar trajetórias de agentes (sequência de ações)
- Detectar problemas de segurança, alinhamento ou qualidade
- Fornecer feedback estruturado e explicável

### 1.2 Por que usar LLMs como Judge?

#### Vantagens:

1. **Escalabilidade**: Avalia milhares de respostas automaticamente
2. **Consistência**: Aplica os mesmos critérios de avaliação
3. **Custo**: Mais barato que avaliação humana em larga escala
4. **Velocidade**: Avaliações em tempo real ou quase real
5. **Flexibilidade**: Pode avaliar múltiplos aspectos simultaneamente
6. **Explicabilidade**: Pode fornecer justificativas para suas avaliações

#### Desafios:

1. **Viés do Modelo**: O judge pode ter seus próprios vieses
2. **Alinhamento**: Necessidade de garantir que o judge avalia o que realmente importa
3. **Consistência**: Pode haver variação entre avaliações
4. **Custo Computacional**: Requer chamadas adicionais a LLMs
5. **Ground Truth**: Ainda pode ser necessário validação humana

### 1.3 Tipos de Avaliação com LLMs as Judge

#### 1.3.1 Avaliação de Trajetória (Trajectory Evaluation)

Avalia a sequência de ações que o agente tomou:

- **Ordem das ações**: As ações foram executadas na ordem correta?
- **Ferramentas utilizadas**: O agente usou as ferramentas apropriadas?
- **Eficiência**: O agente tomou o caminho mais eficiente?
- **Completude**: Todas as ações necessárias foram executadas?

**Exemplo de Prompt para Judge:**

```python
TRAJECTORY_EVALUATION_PROMPT = """
Você é um juiz especializado em avaliar trajetórias de agentes de IA.

Trajetória Esperada: {expected_trajectory}
Trajetória Real: {actual_trajectory}

Avalie:
1. As ações foram executadas na ordem correta? (0-1)
2. Todas as ações necessárias foram executadas? (0-1)
3. Alguma ação desnecessária foi executada? (0-1)
4. A trajetória foi eficiente? (0-1)

Forneça uma pontuação geral de 0-1 e uma justificativa detalhada.
"""
```

#### 1.3.2 Avaliação de Qualidade de Resposta (Response Quality Evaluation)

Avalia a qualidade da resposta final do agente:

- **Correção**: A resposta está factualmente correta?
- **Relevância**: A resposta responde à pergunta do usuário?
- **Completude**: A resposta está completa?
- **Clareza**: A resposta é clara e bem estruturada?
- **Segurança**: A resposta é segura e apropriada?

**Exemplo de Prompt para Judge:**

```python
RESPONSE_QUALITY_PROMPT = """
Você é um juiz especializado em avaliar respostas de agentes de IA.

Pergunta do Usuário: {user_query}
Resposta do Agente: {agent_response}
Contexto: {context}

Avalie a resposta em:
1. Correção factual (0-1)
2. Relevância à pergunta (0-1)
3. Completude (0-1)
4. Clareza e estrutura (0-1)
5. Segurança e apropriação (0-1)

Forneça uma pontuação geral de 0-1 e feedback detalhado.
"""
```

#### 1.3.3 Avaliação Comparativa (Comparative Evaluation)

Compara múltiplas respostas e ranqueia:

- **Ranking**: Qual resposta é melhor?
- **Diferenças**: Quais são as diferenças principais?
- **Trade-offs**: Quais são os prós e contras de cada resposta?

**Exemplo de Prompt para Judge:**

```python
COMPARATIVE_EVALUATION_PROMPT = """
Você é um juiz especializado em comparar respostas de agentes.

Pergunta: {user_query}
Resposta A: {response_a}
Resposta B: {response_b}

Compare as respostas e:
1. Identifique qual é melhor (A ou B)
2. Forneça uma pontuação relativa (0-1 para cada)
3. Liste os pontos fortes e fracos de cada resposta
4. Explique sua decisão
"""
```

#### 1.3.4 Avaliação de Comportamento (Behavioral Evaluation)

Avalia o comportamento geral do agente:

- **Alinhamento**: O agente seguiu as instruções?
- **Ética**: O comportamento foi ético?
- **Robustez**: O agente lidou bem com edge cases?
- **Consistência**: O comportamento foi consistente?

---

## 2. Modelos LLM Adequados para Função de Judge

### 2.1 Critérios para Seleção de Judge LLM

Ao escolher um LLM para função de judge, considere:

1. **Capacidade de Raciocínio**: Precisa entender nuances e contexto
2. **Consistência**: Deve fornecer avaliações consistentes
3. **Capacidade de Seguir Instruções**: Deve seguir prompts de avaliação precisamente
4. **Custo**: Deve ser economicamente viável para uso em escala
5. **Latência**: Deve ser rápido o suficiente para uso em produção
6. **Disponibilidade**: Deve estar disponível através de APIs confiáveis
7. **Capacidade de Output Estruturado**: Deve poder fornecer avaliações estruturadas

### 2.2 Análise Comparativa de Modelos

#### 2.2.1 Modelos GPT (OpenAI)

**GPT-4 Turbo / GPT-4o**
- ✅ Excelente capacidade de raciocínio
- ✅ Alta consistência
- ✅ Suporte a JSON mode para outputs estruturados
- ✅ Boa capacidade de seguir instruções complexas
- ⚠️ Custo mais alto
- ⚠️ Latência moderada

**GPT-3.5 Turbo**
- ✅ Custo mais baixo
- ✅ Latência baixa
- ✅ Boa capacidade de raciocínio
- ⚠️ Menos consistente que GPT-4
- ⚠️ Pode ter dificuldade com avaliações muito complexas

**Recomendação**: GPT-4o para avaliações críticas, GPT-3.5 Turbo para avaliações em larga escala.

#### 2.2.2 Modelos Gemini (Google)

**Gemini 2.0 Flash**
- ✅ Excelente custo-benefício
- ✅ Latência muito baixa
- ✅ Boa capacidade de raciocínio
- ✅ Integração nativa com Google ADK
- ⚠️ Pode ser menos consistente que GPT-4 em casos complexos

**Gemini 2.0 Pro**
- ✅ Excelente capacidade de raciocínio
- ✅ Alta consistência
- ✅ Suporte a contexto muito longo
- ⚠️ Custo mais alto que Flash
- ⚠️ Latência maior

**Recomendação**: Gemini 2.0 Flash para maioria dos casos, Gemini 2.0 Pro para avaliações muito complexas.

#### 2.2.3 Modelos Claude (Anthropic)

**Claude 3.5 Sonnet**
- ✅ Excelente capacidade de raciocínio
- ✅ Muito consistente
- ✅ Excelente em análise detalhada
- ✅ Suporte a contexto muito longo
- ⚠️ Custo moderado-alto
- ⚠️ Latência moderada

**Claude 3 Haiku**
- ✅ Custo muito baixo
- ✅ Latência muito baixa
- ✅ Boa capacidade de raciocínio
- ⚠️ Menos consistente que Sonnet

**Recomendação**: Claude 3.5 Sonnet para avaliações críticas, Claude 3 Haiku para avaliações em larga escala.

#### 2.2.4 Modelos Open Source

**Llama 3.1 70B / 405B**
- ✅ Custo muito baixo (self-hosted)
- ✅ Controle total sobre o modelo
- ✅ Sem limites de rate
- ⚠️ Requer infraestrutura própria
- ⚠️ Pode ser menos consistente que modelos comerciais
- ⚠️ Requer fine-tuning para melhor performance

**Mixtral 8x7B / 8x22B**
- ✅ Custo muito baixo (self-hosted)
- ✅ Boa capacidade de raciocínio
- ⚠️ Requer infraestrutura própria
- ⚠️ Pode precisar de fine-tuning

**Recomendação**: Para organizações com infraestrutura adequada e necessidade de controle total.

### 2.3 Tabela Comparativa Resumida

| Modelo | Custo | Latência | Raciocínio | Consistência | Recomendação |
|--------|-------|----------|------------|--------------|--------------|
| GPT-4o | Alto | Média | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | Crítico |
| GPT-3.5 Turbo | Baixo | Baixa | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | Larga escala |
| Gemini 2.0 Flash | Muito Baixo | Muito Baixa | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | **Recomendado** |
| Gemini 2.0 Pro | Médio | Média | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | Complexo |
| Claude 3.5 Sonnet | Médio-Alto | Média | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | Crítico |
| Claude 3 Haiku | Muito Baixo | Muito Baixa | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | Larga escala |
| Llama 3.1 70B | Muito Baixo* | Média* | ⭐⭐⭐⭐ | ⭐⭐⭐ | Self-hosted |

*Custo e latência dependem da infraestrutura própria

### 2.4 Recomendações por Caso de Uso

#### Para Avaliações em Tempo Real (Produção)
- **Primário**: Gemini 2.0 Flash ou Claude 3 Haiku
- **Alternativa**: GPT-3.5 Turbo

#### Para Avaliações Críticas (Qualidade Máxima)
- **Primário**: GPT-4o ou Claude 3.5 Sonnet
- **Alternativa**: Gemini 2.0 Pro

#### Para Avaliações em Larga Escala (Batch)
- **Primário**: Gemini 2.0 Flash ou Claude 3 Haiku
- **Alternativa**: GPT-3.5 Turbo

#### Para Avaliações com Alto Volume e Baixo Custo
- **Primário**: Modelos open source self-hosted (Llama 3.1)
- **Alternativa**: Gemini 2.0 Flash

---

## 3. Integração com Google ADK

### 3.1 Arquitetura de Integração

O Google ADK já possui suporte nativo para avaliação através do `AgentEvaluator`. Podemos estender isso para usar LLMs as Judge:

```
┌─────────────────┐
│   Agent ADK     │
│   (Sob Teste)   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  AgentEvaluator │
│   (ADK Native)  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  LLM Judge      │
│  (Customizado)  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   Langfuse      │
│  (Tracing/Log)  │
└─────────────────┘
```

### 3.2 Implementação de Judge com ADK

#### 3.2.1 Criando um Judge Agent

```python
from google.adk import Agent
from typing import Dict, Any, List
import json

# Judge Agent especializado em avaliação
judge_agent = Agent(
    name="evaluation_judge",
    description="Especialista em avaliar qualidade de respostas e trajetórias de agentes",
    instruction="""
    Você é um juiz especializado em avaliar agentes de IA.
    
    Sua tarefa é avaliar:
    1. A qualidade da resposta do agente
    2. A trajetória de ações tomadas
    3. A adequação ao contexto e requisitos
    
    Sempre forneça:
    - Uma pontuação numérica de 0-1
    - Uma justificativa detalhada
    - Pontos fortes e fracos identificados
    - Recomendações de melhoria
    
    Formate sua resposta como JSON estruturado.
    """,
    model="gemini-2.0-flash",  # Ou outro modelo adequado
)
```

#### 3.2.2 Classe de Judge Customizada

```python
from google.adk import Runner, Session
from typing import Optional, Dict, Any
import json

class LLMJudge:
    """Judge usando LLM para avaliar agentes ADK"""
    
    def __init__(
        self,
        judge_agent: Agent,
        runner: Runner,
        evaluation_criteria: Dict[str, str]
    ):
        self.judge_agent = judge_agent
        self.runner = runner
        self.criteria = evaluation_criteria
    
    async def evaluate_trajectory(
        self,
        expected_trajectory: List[str],
        actual_trajectory: List[str],
        context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Avalia a trajetória de ações do agente"""
        
        prompt = f"""
        Avalie a trajetória do agente:
        
        Trajetória Esperada: {json.dumps(expected_trajectory, ensure_ascii=False)}
        Trajetória Real: {json.dumps(actual_trajectory, ensure_ascii=False)}
        Contexto: {json.dumps(context or {}, ensure_ascii=False)}
        
        Critérios de Avaliação:
        {json.dumps(self.criteria, ensure_ascii=False, indent=2)}
        
        Forneça uma avaliação em JSON com:
        - score: pontuação de 0-1
        - order_match: as ações estão na ordem correta? (0-1)
        - completeness: todas as ações necessárias foram executadas? (0-1)
        - efficiency: a trajetória foi eficiente? (0-1)
        - justification: justificativa detalhada
        - strengths: pontos fortes
        - weaknesses: pontos fracos
        """
        
        session = Session()
        response = await self.runner.run(
            agent=self.judge_agent,
            session=session,
            user_content=prompt
        )
        
        # Parse da resposta JSON
        try:
            evaluation = json.loads(response.content)
            return evaluation
        except json.JSONDecodeError:
            # Fallback: tentar extrair JSON da resposta
            return self._extract_json_from_response(response.content)
    
    async def evaluate_response(
        self,
        user_query: str,
        agent_response: str,
        expected_response: Optional[str] = None,
        context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Avalia a qualidade da resposta do agente"""
        
        prompt = f"""
        Avalie a resposta do agente:
        
        Pergunta do Usuário: {user_query}
        Resposta do Agente: {agent_response}
        Resposta Esperada (referência): {expected_response or "N/A"}
        Contexto: {json.dumps(context or {}, ensure_ascii=False, indent=2)}
        
        Critérios de Avaliação:
        {json.dumps(self.criteria, ensure_ascii=False, indent=2)}
        
        Forneça uma avaliação em JSON com:
        - score: pontuação geral de 0-1
        - correctness: correção factual (0-1)
        - relevance: relevância à pergunta (0-1)
        - completeness: completude (0-1)
        - clarity: clareza e estrutura (0-1)
        - safety: segurança e apropriação (0-1)
        - justification: justificativa detalhada
        - strengths: pontos fortes
        - weaknesses: pontos fracos
        - recommendations: recomendações de melhoria
        """
        
        session = Session()
        response = await self.runner.run(
            agent=self.judge_agent,
            session=session,
            user_content=prompt
        )
        
        try:
            evaluation = json.loads(response.content)
            return evaluation
        except json.JSONDecodeError:
            return self._extract_json_from_response(response.content)
    
    async def compare_responses(
        self,
        user_query: str,
        responses: List[Dict[str, str]],
        context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Compara múltiplas respostas e ranqueia"""
        
        responses_text = "\n\n".join([
            f"Resposta {i+1}:\n{resp.get('response', '')}"
            for i, resp in enumerate(responses)
        ])
        
        prompt = f"""
        Compare e ranqueie as seguintes respostas:
        
        Pergunta: {user_query}
        
        {responses_text}
        
        Contexto: {json.dumps(context or {}, ensure_ascii=False, indent=2)}
        
        Forneça uma comparação em JSON com:
        - rankings: lista ordenada de índices (melhor primeiro)
        - scores: pontuações de 0-1 para cada resposta
        - comparison: comparação detalhada entre as respostas
        - winner: índice da melhor resposta
        - reasoning: raciocínio por trás da decisão
        """
        
        session = Session()
        response = await self.runner.run(
            agent=self.judge_agent,
            session=session,
            user_content=prompt
        )
        
        try:
            comparison = json.loads(response.content)
            return comparison
        except json.JSONDecodeError:
            return self._extract_json_from_response(response.content)
    
    def _extract_json_from_response(self, text: str) -> Dict[str, Any]:
        """Extrai JSON de uma resposta que pode conter texto adicional"""
        import re
        json_match = re.search(r'\{.*\}', text, re.DOTALL)
        if json_match:
            try:
                return json.loads(json_match.group())
            except json.JSONDecodeError:
                pass
        return {"error": "Não foi possível extrair JSON da resposta", "raw": text}
```

#### 3.2.3 Integração com AgentEvaluator do ADK

```python
from google.adk.evaluation import AgentEvaluator
from typing import List, Dict, Any

class LLMJudgeEvaluator(AgentEvaluator):
    """Extensão do AgentEvaluator do ADK com LLM Judge"""
    
    def __init__(
        self,
        agent_to_evaluate: Agent,
        judge: LLMJudge,
        **kwargs
    ):
        super().__init__(agent_to_evaluate, **kwargs)
        self.judge = judge
    
    async def evaluate_with_judge(
        self,
        test_cases: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Avalia casos de teste usando LLM Judge"""
        
        results = []
        
        for test_case in test_cases:
            # Executa o agente sendo avaliado
            agent_result = await self._run_agent(test_case)
            
            # Avalia com o judge
            trajectory_eval = None
            if test_case.get("expected_trajectory"):
                trajectory_eval = await self.judge.evaluate_trajectory(
                    expected_trajectory=test_case["expected_trajectory"],
                    actual_trajectory=agent_result["trajectory"],
                    context=test_case.get("context")
                )
            
            response_eval = await self.judge.evaluate_response(
                user_query=test_case["user_query"],
                agent_response=agent_result["response"],
                expected_response=test_case.get("expected_response"),
                context=test_case.get("context")
            )
            
            results.append({
                "test_case": test_case,
                "agent_result": agent_result,
                "trajectory_evaluation": trajectory_eval,
                "response_evaluation": response_eval,
                "overall_score": self._calculate_overall_score(
                    trajectory_eval,
                    response_eval
                )
            })
        
        return {
            "results": results,
            "summary": self._generate_summary(results)
        }
    
    def _calculate_overall_score(
        self,
        trajectory_eval: Optional[Dict[str, Any]],
        response_eval: Dict[str, Any]
    ) -> float:
        """Calcula pontuação geral combinando trajetória e resposta"""
        
        scores = []
        
        if trajectory_eval:
            scores.append(trajectory_eval.get("score", 0))
        
        if response_eval:
            scores.append(response_eval.get("score", 0))
        
        return sum(scores) / len(scores) if scores else 0.0
    
    def _generate_summary(self, results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Gera resumo das avaliações"""
        
        scores = [r["overall_score"] for r in results]
        
        return {
            "total_tests": len(results),
            "average_score": sum(scores) / len(scores) if scores else 0,
            "min_score": min(scores) if scores else 0,
            "max_score": max(scores) if scores else 0,
            "pass_rate": sum(1 for s in scores if s >= 0.7) / len(scores) if scores else 0
        }
```

---

## 4. Integração com Langfuse

### 4.1 Por que Integrar Langfuse?

Langfuse oferece:

- **Tracing**: Rastreamento completo de execuções
- **Feedback**: Coleta de feedback humano e automático
- **Analytics**: Análise de performance e custos
- **Prompt Management**: Versionamento e gerenciamento de prompts
- **Scores**: Armazenamento de pontuações de avaliação

### 4.2 Implementação de Integração

#### 4.2.1 Judge com Tracing Langfuse

```python
from langfuse import Langfuse
from langfuse.decorators import langfuse_context
from typing import Dict, Any, Optional
import asyncio

class LangfuseLLMJudge(LLMJudge):
    """LLM Judge integrado com Langfuse para tracing e analytics"""
    
    def __init__(
        self,
        judge_agent: Agent,
        runner: Runner,
        evaluation_criteria: Dict[str, str],
        langfuse_client: Langfuse
    ):
        super().__init__(judge_agent, runner, evaluation_criteria)
        self.langfuse = langfuse_client
    
    async def evaluate_trajectory(
        self,
        expected_trajectory: List[str],
        actual_trajectory: List[str],
        context: Optional[Dict[str, Any]] = None,
        trace_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """Avalia trajetória com tracing Langfuse"""
        
        # Cria trace no Langfuse
        trace = self.langfuse.trace(
            name="trajectory_evaluation",
            id=trace_id,
            metadata={
                "expected_trajectory": expected_trajectory,
                "actual_trajectory": actual_trajectory,
                "context": context
            }
        )
        
        try:
            # Executa avaliação
            evaluation = await super().evaluate_trajectory(
                expected_trajectory,
                actual_trajectory,
                context
            )
            
            # Registra score no Langfuse
            trace.score(
                name="trajectory_score",
                value=evaluation.get("score", 0),
                comment=evaluation.get("justification", "")
            )
            
            # Registra scores individuais
            for metric, value in evaluation.items():
                if isinstance(value, (int, float)) and 0 <= value <= 1:
                    trace.score(
                        name=f"trajectory_{metric}",
                        value=value
                    )
            
            return evaluation
            
        except Exception as e:
            trace.update(
                level="ERROR",
                status_message=str(e)
            )
            raise
    
    async def evaluate_response(
        self,
        user_query: str,
        agent_response: str,
        expected_response: Optional[str] = None,
        context: Optional[Dict[str, Any]] = None,
        trace_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """Avalia resposta com tracing Langfuse"""
        
        trace = self.langfuse.trace(
            name="response_evaluation",
            id=trace_id,
            input={
                "user_query": user_query,
                "agent_response": agent_response,
                "expected_response": expected_response
            },
            metadata=context or {}
        )
        
        try:
            evaluation = await super().evaluate_response(
                user_query,
                agent_response,
                expected_response,
                context
            )
            
            # Registra score geral
            trace.score(
                name="response_score",
                value=evaluation.get("score", 0),
                comment=evaluation.get("justification", "")
            )
            
            # Registra scores individuais
            for metric in ["correctness", "relevance", "completeness", "clarity", "safety"]:
                if metric in evaluation:
                    trace.score(
                        name=f"response_{metric}",
                        value=evaluation[metric]
                    )
            
            # Registra pontos fortes e fracos como observações
            if evaluation.get("strengths"):
                trace.observation(
                    name="strengths",
                    value=evaluation["strengths"]
                )
            
            if evaluation.get("weaknesses"):
                trace.observation(
                    name="weaknesses",
                    value=evaluation["weaknesses"]
                )
            
            return evaluation
            
        except Exception as e:
            trace.update(
                level="ERROR",
                status_message=str(e)
            )
            raise
```

#### 4.2.2 Feedback Loop com Langfuse

```python
class LangfuseFeedbackJudge:
    """Integra feedback humano com avaliação automática do judge"""
    
    def __init__(
        self,
        judge: LangfuseLLMJudge,
        langfuse_client: Langfuse
    ):
        self.judge = judge
        self.langfuse = langfuse_client
    
    async def evaluate_with_feedback(
        self,
        trace_id: str,
        user_query: str,
        agent_response: str,
        human_feedback: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Combina avaliação automática com feedback humano"""
        
        # Avaliação automática
        auto_eval = await self.judge.evaluate_response(
            user_query=user_query,
            agent_response=agent_response,
            trace_id=trace_id
        )
        
        # Se houver feedback humano, combina
        if human_feedback:
            combined_score = self._combine_scores(
                auto_eval.get("score", 0),
                human_feedback.get("score", 0)
            )
            
            # Registra feedback humano no Langfuse
            self.langfuse.score(
                trace_id=trace_id,
                name="human_feedback",
                value=human_feedback.get("score", 0),
                comment=human_feedback.get("comment", "")
            )
            
            # Registra score combinado
            self.langfuse.score(
                trace_id=trace_id,
                name="combined_score",
                value=combined_score,
                comment="Combinação de avaliação automática e feedback humano"
            )
            
            auto_eval["human_feedback"] = human_feedback
            auto_eval["combined_score"] = combined_score
        
        return auto_eval
    
    def _combine_scores(
        self,
        auto_score: float,
        human_score: float,
        auto_weight: float = 0.7,
        human_weight: float = 0.3
    ) -> float:
        """Combina scores automático e humano com pesos"""
        return (auto_score * auto_weight) + (human_score * human_weight)
```

---

## 5. Exemplos Práticos Completos

### 5.1 Exemplo 1: Avaliação de Agente RAG

```python
import asyncio
from google.adk import Agent, Runner, Session
from langfuse import Langfuse

# Configuração
langfuse = Langfuse(
    secret_key="your-secret-key",
    public_key="your-public-key",
    host="https://cloud.langfuse.com"
)

# Judge Agent
judge_agent = Agent(
    name="rag_evaluator",
    description="Especialista em avaliar respostas de agentes RAG",
    instruction="""
    Você avalia respostas de agentes RAG considerando:
    1. Precisão das informações citadas
    2. Relevância das fontes utilizadas
    3. Completude da resposta
    4. Clareza na apresentação
    
    Sempre forneça JSON estruturado com scores e justificativas.
    """,
    model="gemini-2.0-flash"
)

# Criar judge
judge = LangfuseLLMJudge(
    judge_agent=judge_agent,
    runner=Runner(),
    evaluation_criteria={
        "accuracy": "As informações estão corretas?",
        "citation_quality": "As citações são relevantes?",
        "completeness": "A resposta está completa?",
        "clarity": "A resposta é clara?"
    },
    langfuse_client=langfuse
)

# Casos de teste
test_cases = [
    {
        "user_query": "Quais são os principais segmentos de negócio da Alphabet?",
        "expected_response": "Google Services, Google Cloud, Other Bets",
        "expected_trajectory": ["search_documents", "retrieve_context", "generate_response"],
        "context": {"domain": "finance", "document_type": "10-K"}
    }
]

# Executar avaliação
async def evaluate_rag_agent():
    results = []
    
    for test_case in test_cases:
        # Simula execução do agente RAG (substitua pelo seu agente real)
        agent_response = "A Alphabet possui três segmentos principais..."
        agent_trajectory = ["search_documents", "retrieve_context", "generate_response"]
        
        # Avalia trajetória
        traj_eval = await judge.evaluate_trajectory(
            expected_trajectory=test_case["expected_trajectory"],
            actual_trajectory=agent_trajectory,
            context=test_case.get("context")
        )
        
        # Avalia resposta
        resp_eval = await judge.evaluate_response(
            user_query=test_case["user_query"],
            agent_response=agent_response,
            expected_response=test_case.get("expected_response"),
            context=test_case.get("context")
        )
        
        results.append({
            "test_case": test_case,
            "trajectory_evaluation": traj_eval,
            "response_evaluation": resp_eval
        })
    
    return results

# Executar
# results = asyncio.run(evaluate_rag_agent())
```

### 5.2 Exemplo 2: Avaliação Comparativa de Modelos

```python
async def compare_models(
    user_query: str,
    responses: List[Dict[str, str]],
    judge: LLMJudge
) -> Dict[str, Any]:
    """Compara respostas de diferentes modelos"""
    
    comparison = await judge.compare_responses(
        user_query=user_query,
        responses=responses
    )
    
    print(f"Melhor resposta: {comparison['winner']}")
    print(f"Scores: {comparison['scores']}")
    print(f"Raciocínio: {comparison['reasoning']}")
    
    return comparison

# Uso
responses = [
    {"model": "gpt-4", "response": "Resposta do GPT-4..."},
    {"model": "gemini-2.0-flash", "response": "Resposta do Gemini..."},
    {"model": "claude-3.5-sonnet", "response": "Resposta do Claude..."}
]

comparison = asyncio.run(compare_models(
    user_query="Explique o conceito de LLMs as a Judge",
    responses=responses,
    judge=judge
))
```

### 5.3 Exemplo 3: Pipeline de Avaliação Contínua

```python
class ContinuousEvaluationPipeline:
    """Pipeline de avaliação contínua com LLM Judge"""
    
    def __init__(
        self,
        agent_to_evaluate: Agent,
        judge: LangfuseLLMJudge,
        test_suite: List[Dict[str, Any]]
    ):
        self.agent = agent_to_evaluate
        self.judge = judge
        self.test_suite = test_suite
        self.runner = Runner()
    
    async def run_evaluation_cycle(self) -> Dict[str, Any]:
        """Executa um ciclo completo de avaliação"""
        
        results = []
        
        for test_case in self.test_suite:
            # Executa agente
            session = Session()
            agent_result = await self.runner.run(
                agent=self.agent,
                session=session,
                user_content=test_case["user_query"]
            )
            
            # Extrai trajetória (se disponível)
            trajectory = self._extract_trajectory(agent_result)
            
            # Avalia com judge
            trace_id = self.judge.langfuse.get_current_trace_id()
            
            traj_eval = None
            if test_case.get("expected_trajectory"):
                traj_eval = await self.judge.evaluate_trajectory(
                    expected_trajectory=test_case["expected_trajectory"],
                    actual_trajectory=trajectory,
                    trace_id=trace_id
                )
            
            resp_eval = await self.judge.evaluate_response(
                user_query=test_case["user_query"],
                agent_response=agent_result.content,
                expected_response=test_case.get("expected_response"),
                trace_id=trace_id
            )
            
            results.append({
                "test_case_id": test_case.get("id"),
                "trajectory_evaluation": traj_eval,
                "response_evaluation": resp_eval,
                "trace_id": trace_id
            })
        
        return {
            "results": results,
            "summary": self._generate_summary(results)
        }
    
    def _extract_trajectory(self, agent_result) -> List[str]:
        """Extrai trajetória do resultado do agente"""
        # Implementar extração baseada na estrutura do ADK
        trajectory = []
        # Exemplo: percorrer eventos do agente
        return trajectory
    
    def _generate_summary(self, results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Gera resumo das avaliações"""
        scores = [
            r["response_evaluation"].get("score", 0)
            for r in results
            if r.get("response_evaluation")
        ]
        
        return {
            "total_tests": len(results),
            "average_score": sum(scores) / len(scores) if scores else 0,
            "pass_rate": sum(1 for s in scores if s >= 0.7) / len(scores) if scores else 0,
            "failing_tests": [
                r["test_case_id"]
                for r in results
                if r.get("response_evaluation", {}).get("score", 0) < 0.7
            ]
        }
```

---

## 6. Métricas e Benchmarks

### 6.1 Métricas de Qualidade do Judge

#### 6.1.1 Consistência (Consistency)

Mede quão consistente o judge é em avaliações similares:

```python
def measure_judge_consistency(
    judge: LLMJudge,
    test_cases: List[Dict[str, Any]],
    num_runs: int = 3
) -> Dict[str, float]:
    """Mede consistência do judge executando múltiplas vezes"""
    
    all_scores = []
    
    for test_case in test_cases:
        scores = []
        for _ in range(num_runs):
            eval_result = await judge.evaluate_response(
                user_query=test_case["user_query"],
                agent_response=test_case["agent_response"]
            )
            scores.append(eval_result.get("score", 0))
        
        all_scores.append(scores)
    
    # Calcula variância média
    variances = [np.var(scores) for scores in all_scores]
    avg_variance = np.mean(variances)
    
    # Calcula coeficiente de variação
    cv_scores = [
        np.std(scores) / np.mean(scores) if np.mean(scores) > 0 else 0
        for scores in all_scores
    ]
    avg_cv = np.mean(cv_scores)
    
    return {
        "average_variance": avg_variance,
        "average_coefficient_of_variation": avg_cv,
        "consistency_score": 1 - min(avg_cv, 1.0)  # 0-1, maior é melhor
    }
```

#### 6.1.2 Correlação com Avaliação Humana

```python
def measure_human_correlation(
    judge: LLMJudge,
    human_evaluations: List[Dict[str, Any]]
) -> Dict[str, float]:
    """Mede correlação entre avaliação do judge e avaliação humana"""
    
    from scipy.stats import pearsonr, spearmanr
    
    judge_scores = []
    human_scores = []
    
    for eval_data in human_evaluations:
        judge_eval = await judge.evaluate_response(
            user_query=eval_data["user_query"],
            agent_response=eval_data["agent_response"]
        )
        
        judge_scores.append(judge_eval.get("score", 0))
        human_scores.append(eval_data["human_score"])
    
    # Correlação de Pearson (linear)
    pearson_corr, pearson_p = pearsonr(judge_scores, human_scores)
    
    # Correlação de Spearman (rank)
    spearman_corr, spearman_p = spearmanr(judge_scores, human_scores)
    
    return {
        "pearson_correlation": pearson_corr,
        "pearson_p_value": pearson_p,
        "spearman_correlation": spearman_corr,
        "spearman_p_value": spearman_p,
        "agreement_rate": sum(
            1 for j, h in zip(judge_scores, human_scores)
            if abs(j - h) < 0.2
        ) / len(judge_scores)
    }
```

#### 6.1.3 Viés e Justiça (Bias and Fairness)

```python
def measure_judge_bias(
    judge: LLMJudge,
    test_suite: List[Dict[str, Any]]
) -> Dict[str, Any]:
    """Mede viés do judge em diferentes categorias"""
    
    categories = {}
    
    for test_case in test_suite:
        category = test_case.get("category", "unknown")
        
        if category not in categories:
            categories[category] = []
        
        eval_result = await judge.evaluate_response(
            user_query=test_case["user_query"],
            agent_response=test_case["agent_response"]
        )
        
        categories[category].append(eval_result.get("score", 0))
    
    # Calcula médias por categoria
    category_means = {
        cat: np.mean(scores)
        for cat, scores in categories.items()
    }
    
    # Identifica disparidades
    overall_mean = np.mean(list(category_means.values()))
    disparities = {
        cat: mean - overall_mean
        for cat, mean in category_means.items()
    }
    
    return {
        "category_means": category_means,
        "overall_mean": overall_mean,
        "disparities": disparities,
        "max_disparity": max(abs(d) for d in disparities.values())
    }
```

### 6.2 Benchmarks Recomendados

#### 6.2.1 MT-Bench (Multi-Turn Benchmark)

Adaptado para avaliação de agentes:

```python
MT_BENCH_CASES = [
    {
        "category": "writing",
        "user_query": "Escreva um poema sobre inteligência artificial",
        "criteria": ["creativity", "coherence", "literary_quality"]
    },
    {
        "category": "reasoning",
        "user_query": "Resolva este problema de lógica: ...",
        "criteria": ["correctness", "reasoning_quality", "explanation"]
    },
    # ... mais casos
]
```

#### 6.2.2 HELM (Holistic Evaluation of Language Models)

Adaptado para agentes:

```python
HELM_SCENARIOS = [
    "question_answering",
    "summarization",
    "code_generation",
    "reasoning",
    "safety"
]
```

### 6.3 Métricas de Custo-Eficiência

```python
def calculate_cost_efficiency(
    judge: LLMJudge,
    evaluations: List[Dict[str, Any]],
    cost_per_token: float
) -> Dict[str, float]:
    """Calcula custo-eficiência do judge"""
    
    total_tokens = 0
    total_evaluations = len(evaluations)
    
    for eval_data in evaluations:
        # Estima tokens (simplificado)
        prompt_tokens = estimate_tokens(eval_data["prompt"])
        response_tokens = estimate_tokens(eval_data["response"])
        total_tokens += prompt_tokens + response_tokens
    
    total_cost = total_tokens * cost_per_token
    cost_per_evaluation = total_cost / total_evaluations
    
    return {
        "total_evaluations": total_evaluations,
        "total_tokens": total_tokens,
        "total_cost": total_cost,
        "cost_per_evaluation": cost_per_evaluation,
        "tokens_per_evaluation": total_tokens / total_evaluations
    }
```

---

## 7. Melhores Práticas

### 7.1 Design de Prompts para Judge

#### Princípios:

1. **Seja Específico**: Defina claramente os critérios de avaliação
2. **Use Exemplos**: Inclua exemplos de boas e más respostas
3. **Estruture o Output**: Solicite JSON estruturado
4. **Defina Escalas**: Especifique claramente a escala de pontuação
5. **Peça Justificativas**: Solicite explicações para transparência

#### Template de Prompt Recomendado:

```python
JUDGE_PROMPT_TEMPLATE = """
Você é um juiz especializado em avaliar {domain}.

TAREFA:
Avalie a seguinte resposta de um agente de IA.

PERGUNTA DO USUÁRIO:
{user_query}

RESPOSTA DO AGENTE:
{agent_response}

{optional_sections}

CRITÉRIOS DE AVALIAÇÃO:
{criteria}

ESCALA DE PONTUAÇÃO:
- 0.0-0.3: Insatisfatório
- 0.4-0.6: Aceitável
- 0.7-0.8: Bom
- 0.9-1.0: Excelente

FORMATO DE RESPOSTA:
Forneça sua avaliação em JSON com a seguinte estrutura:
{{
    "score": <float 0-1>,
    "scores_by_criterion": {{
        "criterion1": <float 0-1>,
        "criterion2": <float 0-1>
    }},
    "justification": "<explicação detalhada>",
    "strengths": ["<ponto forte 1>", "<ponto forte 2>"],
    "weaknesses": ["<ponto fraco 1>", "<ponto fraco 2>"],
    "recommendations": ["<recomendação 1>", "<recomendação 2>"]
}}

IMPORTANTE:
- Seja objetivo e justo
- Considere o contexto fornecido
- Forneça feedback construtivo
- Justifique suas pontuações
"""
```

### 7.2 Estratégias de Redução de Custo

1. **Caching**: Cache avaliações de respostas idênticas
2. **Batching**: Agrupe múltiplas avaliações em uma única chamada
3. **Modelos Menores**: Use modelos menores para avaliações simples
4. **Amostragem**: Avalie apenas uma amostra representativa
5. **Avaliação Hierárquica**: Use judge menor primeiro, judge maior apenas se necessário

```python
class CostOptimizedJudge:
    """Judge otimizado para custo"""
    
    def __init__(
        self,
        fast_judge: LLMJudge,  # Modelo rápido/barato
        accurate_judge: LLMJudge,  # Modelo preciso/caro
        threshold: float = 0.7
    ):
        self.fast_judge = fast_judge
        self.accurate_judge = accurate_judge
        self.threshold = threshold
        self.cache = {}
    
    async def evaluate_with_fallback(
        self,
        user_query: str,
        agent_response: str,
        **kwargs
    ) -> Dict[str, Any]:
        """Avalia com fallback para judge mais preciso se necessário"""
        
        # Verifica cache
        cache_key = f"{user_query}:{agent_response}"
        if cache_key in self.cache:
            return self.cache[cache_key]
        
        # Avalia com judge rápido primeiro
        fast_eval = await self.fast_judge.evaluate_response(
            user_query=user_query,
            agent_response=agent_response,
            **kwargs
        )
        
        fast_score = fast_eval.get("score", 0)
        
        # Se score está próximo do threshold, usa judge preciso
        if abs(fast_score - self.threshold) < 0.1:
            accurate_eval = await self.accurate_judge.evaluate_response(
                user_query=user_query,
                agent_response=agent_response,
                **kwargs
            )
            result = accurate_eval
        else:
            result = fast_eval
        
        # Cache resultado
        self.cache[cache_key] = result
        
        return result
```

### 7.3 Tratamento de Erros e Edge Cases

```python
class RobustJudge(LLMJudge):
    """Judge com tratamento robusto de erros"""
    
    async def evaluate_response(
        self,
        user_query: str,
        agent_response: str,
        max_retries: int = 3,
        **kwargs
    ) -> Dict[str, Any]:
        """Avalia com retry e fallback"""
        
        for attempt in range(max_retries):
            try:
                result = await super().evaluate_response(
                    user_query=user_query,
                    agent_response=agent_response,
                    **kwargs
                )
                
                # Valida resultado
                if self._validate_result(result):
                    return result
                else:
                    raise ValueError("Resultado inválido")
                    
            except Exception as e:
                if attempt == max_retries - 1:
                    # Fallback: retorna avaliação básica
                    return self._fallback_evaluation(
                        user_query=user_query,
                        agent_response=agent_response,
                        error=str(e)
                    )
                
                # Aguarda antes de retry
                await asyncio.sleep(2 ** attempt)
        
        raise RuntimeError("Falha ao avaliar após múltiplas tentativas")
    
    def _validate_result(self, result: Dict[str, Any]) -> bool:
        """Valida estrutura do resultado"""
        required_fields = ["score", "justification"]
        return all(field in result for field in required_fields) and \
               0 <= result.get("score", -1) <= 1
    
    def _fallback_evaluation(
        self,
        user_query: str,
        agent_response: str,
        error: str
    ) -> Dict[str, Any]:
        """Avaliação básica de fallback"""
        return {
            "score": 0.5,  # Score neutro
            "justification": f"Avaliação automática falhou: {error}",
            "error": True,
            "fallback": True
        }
```

### 7.4 Calibração do Judge

```python
class CalibratedJudge(LLMJudge):
    """Judge calibrado com dados de referência"""
    
    def __init__(self, *args, calibration_data: List[Dict[str, Any]] = None, **kwargs):
        super().__init__(*args, **kwargs)
        self.calibration_data = calibration_data or []
        self.calibration_factor = self._calculate_calibration_factor()
    
    def _calculate_calibration_factor(self) -> float:
        """Calcula fator de calibração baseado em dados de referência"""
        if not self.calibration_data:
            return 1.0
        
        # Executa avaliações e compara com referência
        # Retorna fator de ajuste
        return 1.0  # Simplificado
    
    async def evaluate_response(self, *args, **kwargs) -> Dict[str, Any]:
        """Avalia com calibração aplicada"""
        result = await super().evaluate_response(*args, **kwargs)
        
        # Aplica calibração
        if "score" in result:
            result["score"] = min(1.0, result["score"] * self.calibration_factor)
            result["original_score"] = result["score"] / self.calibration_factor
        
        return result
```

---

## 8. Casos de Uso Específicos

### 8.1 Avaliação de Agentes Conversacionais

```python
CONVERSATIONAL_JUDGE_CRITERIA = {
    "coherence": "A resposta é coerente com o contexto da conversa?",
    "relevance": "A resposta é relevante para a pergunta do usuário?",
    "helpfulness": "A resposta é útil para o usuário?",
    "naturalness": "A resposta soa natural e conversacional?",
    "completeness": "A resposta está completa ou precisa de follow-up?"
}
```

### 8.2 Avaliação de Agentes de Código

```python
CODE_JUDGE_CRITERIA = {
    "correctness": "O código está correto e funciona?",
    "efficiency": "O código é eficiente?",
    "readability": "O código é legível e bem estruturado?",
    "best_practices": "O código segue melhores práticas?",
    "documentation": "O código está bem documentado?"
}
```

### 8.3 Avaliação de Agentes RAG

```python
RAG_JUDGE_CRITERIA = {
    "answer_quality": "A resposta está correta e completa?",
    "source_relevance": "As fontes são relevantes?",
    "citation_accuracy": "As citações estão corretas?",
    "groundedness": "A resposta está fundamentada nas fontes?",
    "attribution": "A atribuição às fontes está clara?"
}
```

---

## 9. Conclusões e Recomendações

### 9.1 Resumo das Recomendações

#### Para Projetos com Google ADK:

1. **Judge Principal**: Gemini 2.0 Flash
   - Excelente integração com ADK
   - Custo-benefício ideal
   - Latência baixa

2. **Judge para Casos Críticos**: Gemini 2.0 Pro ou GPT-4o
   - Maior capacidade de raciocínio
   - Maior consistência

3. **Integração**: Use Langfuse para tracing e analytics
   - Rastreamento completo
   - Feedback loops
   - Análise de performance

#### Estratégia de Implementação:

1. **Fase 1**: Implementar judge básico com Gemini 2.0 Flash
2. **Fase 2**: Integrar com Langfuse para observabilidade
3. **Fase 3**: Adicionar avaliação comparativa e benchmarks
4. **Fase 4**: Otimizar custos e performance
5. **Fase 5**: Calibrar com dados de produção

### 9.2 Próximos Passos

1. **Implementar POC**: Criar prova de conceito com judge básico
2. **Coletar Dados**: Executar avaliações em casos reais
3. **Calibrar**: Ajustar judge com feedback humano
4. **Escalar**: Expandir para mais casos de uso
5. **Monitorar**: Acompanhar performance e custos

### 9.3 Recursos Adicionais

- [Google ADK Documentation](https://github.com/google/labs-adk)
- [Langfuse Documentation](https://langfuse.com/docs)
- [MT-Bench Paper](https://arxiv.org/abs/2306.05685)
- [HELM Benchmark](https://crfm.stanford.edu/helm/)

---

## 10. Apêndices

### 10.1 Exemplo Completo de Implementação

Ver arquivo `examples/complete_judge_implementation.py` para exemplo completo.

### 10.2 Templates de Prompts

Ver arquivo `templates/judge_prompts.py` para templates reutilizáveis.

### 10.3 Configurações Recomendadas

Ver arquivo `configs/judge_configs.yaml` para configurações recomendadas.

---

**Documento criado em:** 2024  
**Última atualização:** 2024  
**Autor:** Equipe de IA  
**Versão:** 1.0

