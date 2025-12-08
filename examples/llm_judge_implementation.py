"""
Implementação completa de LLM Judge para avaliação de agentes ADK.

Este módulo fornece classes e funções para avaliar agentes usando LLMs como judges,
com integração ao Google ADK e Langfuse.
"""

import asyncio
import json
import logging
import re
from typing import Dict, Any, List, Optional
from dataclasses import dataclass

from google.adk import Agent, Runner, Session
from langfuse import Langfuse

logger = logging.getLogger(__name__)


@dataclass
class EvaluationCriteria:
    """Critérios de avaliação para o judge"""
    correctness: str = "A resposta está factualmente correta?"
    relevance: str = "A resposta é relevante à pergunta?"
    completeness: str = "A resposta está completa?"
    clarity: str = "A resposta é clara e bem estruturada?"
    safety: str = "A resposta é segura e apropriada?"


class LLMJudge:
    """Judge usando LLM para avaliar agentes ADK"""
    
    def __init__(
        self,
        judge_agent: Agent,
        runner: Runner,
        evaluation_criteria: Optional[Dict[str, str]] = None
    ):
        """
        Inicializa o LLM Judge.
        
        Args:
            judge_agent: Agente ADK configurado como judge
            runner: Runner do ADK para executar o judge
            evaluation_criteria: Critérios de avaliação customizados
        """
        self.judge_agent = judge_agent
        self.runner = runner
        self.criteria = evaluation_criteria or self._default_criteria()
    
    def _default_criteria(self) -> Dict[str, str]:
        """Retorna critérios padrão de avaliação"""
        criteria = EvaluationCriteria()
        return {
            "correctness": criteria.correctness,
            "relevance": criteria.relevance,
            "completeness": criteria.completeness,
            "clarity": criteria.clarity,
            "safety": criteria.safety
        }
    
    async def evaluate_trajectory(
        self,
        expected_trajectory: List[str],
        actual_trajectory: List[str],
        context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Avalia a trajetória de ações do agente.
        
        Args:
            expected_trajectory: Trajetória esperada
            actual_trajectory: Trajetória real executada
            context: Contexto adicional para avaliação
            
        Returns:
            Dicionário com avaliação da trajetória
        """
        prompt = self._build_trajectory_prompt(
            expected_trajectory,
            actual_trajectory,
            context
        )
        
        try:
            session = Session()
            response = await self.runner.run(
                agent=self.judge_agent,
                session=session,
                user_content=prompt
            )
            
            evaluation = self._parse_response(response.content)
            return evaluation
            
        except Exception as e:
            logger.error(f"Erro ao avaliar trajetória: {e}", exc_info=True)
            return self._error_evaluation(str(e))
    
    async def evaluate_response(
        self,
        user_query: str,
        agent_response: str,
        expected_response: Optional[str] = None,
        context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Avalia a qualidade da resposta do agente.
        
        Args:
            user_query: Pergunta do usuário
            agent_response: Resposta do agente
            expected_response: Resposta esperada (opcional, para referência)
            context: Contexto adicional
            
        Returns:
            Dicionário com avaliação da resposta
        """
        prompt = self._build_response_prompt(
            user_query,
            agent_response,
            expected_response,
            context
        )
        
        try:
            session = Session()
            response = await self.runner.run(
                agent=self.judge_agent,
                session=session,
                user_content=prompt
            )
            
            evaluation = self._parse_response(response.content)
            return evaluation
            
        except Exception as e:
            logger.error(f"Erro ao avaliar resposta: {e}", exc_info=True)
            return self._error_evaluation(str(e))
    
    async def compare_responses(
        self,
        user_query: str,
        responses: List[Dict[str, str]],
        context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Compara múltiplas respostas e ranqueia.
        
        Args:
            user_query: Pergunta do usuário
            responses: Lista de respostas para comparar
            context: Contexto adicional
            
        Returns:
            Dicionário com comparação e ranking
        """
        responses_text = "\n\n".join([
            f"Resposta {i+1} ({resp.get('label', f'Modelo {i+1}')}):\n{resp.get('response', '')}"
            for i, resp in enumerate(responses)
        ])
        
        prompt = f"""
Compare e ranqueie as seguintes respostas:

Pergunta: {user_query}

{responses_text}

Contexto: {json.dumps(context or {}, ensure_ascii=False, indent=2)}

Forneça uma comparação em JSON com:
- rankings: lista ordenada de índices (melhor primeiro, 0-indexed)
- scores: pontuações de 0-1 para cada resposta (lista na ordem das respostas)
- comparison: comparação detalhada entre as respostas
- winner: índice da melhor resposta (0-indexed)
- reasoning: raciocínio por trás da decisão
"""
        
        try:
            session = Session()
            response = await self.runner.run(
                agent=self.judge_agent,
                session=session,
                user_content=prompt
            )
            
            comparison = self._parse_response(response.content)
            return comparison
            
        except Exception as e:
            logger.error(f"Erro ao comparar respostas: {e}", exc_info=True)
            return self._error_evaluation(str(e))
    
    def _build_trajectory_prompt(
        self,
        expected_trajectory: List[str],
        actual_trajectory: List[str],
        context: Optional[Dict[str, Any]]
    ) -> str:
        """Constrói prompt para avaliação de trajetória"""
        return f"""
Você é um juiz especializado em avaliar trajetórias de agentes de IA.

Trajetória Esperada: {json.dumps(expected_trajectory, ensure_ascii=False)}
Trajetória Real: {json.dumps(actual_trajectory, ensure_ascii=False)}
Contexto: {json.dumps(context or {}, ensure_ascii=False, indent=2)}

Avalie a trajetória considerando:
1. Ordem das ações: As ações foram executadas na ordem correta? (0-1)
2. Completude: Todas as ações necessárias foram executadas? (0-1)
3. Eficiência: A trajetória foi eficiente (sem ações desnecessárias)? (0-1)
4. Correção: As ações são apropriadas para o contexto? (0-1)

Forneça uma avaliação em JSON com:
- score: pontuação geral de 0-1
- order_match: as ações estão na ordem correta? (0-1)
- completeness: todas as ações necessárias foram executadas? (0-1)
- efficiency: a trajetória foi eficiente? (0-1)
- correctness: as ações são apropriadas? (0-1)
- justification: justificativa detalhada
- strengths: lista de pontos fortes
- weaknesses: lista de pontos fracos
- recommendations: recomendações de melhoria
"""
    
    def _build_response_prompt(
        self,
        user_query: str,
        agent_response: str,
        expected_response: Optional[str],
        context: Optional[Dict[str, Any]]
    ) -> str:
        """Constrói prompt para avaliação de resposta"""
        expected_section = ""
        if expected_response:
            expected_section = f"\nResposta Esperada (referência): {expected_response}"
        
        criteria_text = "\n".join([
            f"- {key}: {value}"
            for key, value in self.criteria.items()
        ])
        
        return f"""
Você é um juiz especializado em avaliar respostas de agentes de IA.

Pergunta do Usuário: {user_query}
Resposta do Agente: {agent_response}{expected_section}
Contexto: {json.dumps(context or {}, ensure_ascii=False, indent=2)}

Critérios de Avaliação:
{criteria_text}

Escala de Pontuação:
- 0.0-0.3: Insatisfatório
- 0.4-0.6: Aceitável
- 0.7-0.8: Bom
- 0.9-1.0: Excelente

Forneça uma avaliação em JSON com:
- score: pontuação geral de 0-1
- correctness: correção factual (0-1)
- relevance: relevância à pergunta (0-1)
- completeness: completude (0-1)
- clarity: clareza e estrutura (0-1)
- safety: segurança e apropriação (0-1)
- justification: justificativa detalhada
- strengths: lista de pontos fortes
- weaknesses: lista de pontos fracos
- recommendations: recomendações de melhoria
"""
    
    def _parse_response(self, text: str) -> Dict[str, Any]:
        """Extrai JSON de uma resposta que pode conter texto adicional"""
        # Tenta parse direto
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            pass
        
        # Tenta extrair JSON do texto
        json_match = re.search(r'\{.*\}', text, re.DOTALL)
        if json_match:
            try:
                return json.loads(json_match.group())
            except json.JSONDecodeError:
                pass
        
        # Fallback: retorna estrutura básica
        logger.warning(f"Não foi possível extrair JSON da resposta: {text[:200]}")
        return {
            "error": "Não foi possível extrair JSON da resposta",
            "raw_response": text,
            "score": 0.5
        }
    
    def _error_evaluation(self, error_message: str) -> Dict[str, Any]:
        """Retorna avaliação de erro"""
        return {
            "error": True,
            "error_message": error_message,
            "score": 0.0,
            "justification": f"Erro na avaliação: {error_message}"
        }


class LangfuseLLMJudge(LLMJudge):
    """LLM Judge integrado com Langfuse para tracing e analytics"""
    
    def __init__(
        self,
        judge_agent: Agent,
        runner: Runner,
        langfuse_client: Langfuse,
        evaluation_criteria: Optional[Dict[str, str]] = None
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
            evaluation = await super().evaluate_trajectory(
                expected_trajectory,
                actual_trajectory,
                context
            )
            
            if not evaluation.get("error"):
                # Registra score no Langfuse
                trace.score(
                    name="trajectory_score",
                    value=evaluation.get("score", 0),
                    comment=evaluation.get("justification", "")
                )
                
                # Registra scores individuais
                for metric in ["order_match", "completeness", "efficiency", "correctness"]:
                    if metric in evaluation and isinstance(evaluation[metric], (int, float)):
                        trace.score(
                            name=f"trajectory_{metric}",
                            value=evaluation[metric]
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
            
            if not evaluation.get("error"):
                # Registra score geral
                trace.score(
                    name="response_score",
                    value=evaluation.get("score", 0),
                    comment=evaluation.get("justification", "")
                )
                
                # Registra scores individuais
                for metric in ["correctness", "relevance", "completeness", "clarity", "safety"]:
                    if metric in evaluation and isinstance(evaluation[metric], (int, float)):
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


# Exemplo de uso
async def example_usage():
    """Exemplo de como usar o LLM Judge"""
    
    # Configuração do judge agent
    judge_agent = Agent(
        name="evaluation_judge",
        description="Especialista em avaliar qualidade de respostas e trajetórias de agentes",
        instruction="""
        Você é um juiz especializado em avaliar agentes de IA.
        Sempre forneça avaliações em JSON estruturado com scores, justificativas e recomendações.
        """,
        model="gemini-2.0-flash"
    )
    
    # Configuração do runner
    runner = Runner()
    
    # Configuração do Langfuse (opcional)
    langfuse = Langfuse(
        secret_key="your-secret-key",
        public_key="your-public-key",
        host="https://cloud.langfuse.com"
    )
    
    # Criar judge
    judge = LangfuseLLMJudge(
        judge_agent=judge_agent,
        runner=runner,
        langfuse_client=langfuse
    )
    
    # Exemplo 1: Avaliar resposta
    evaluation = await judge.evaluate_response(
        user_query="O que é inteligência artificial?",
        agent_response="Inteligência artificial é a capacidade de máquinas de realizar tarefas que normalmente requerem inteligência humana.",
        expected_response="Inteligência artificial (IA) é um campo da ciência da computação que busca criar sistemas capazes de realizar tarefas que normalmente requerem inteligência humana."
    )
    
    print(f"Score: {evaluation.get('score')}")
    print(f"Justificação: {evaluation.get('justification')}")
    
    # Exemplo 2: Avaliar trajetória
    trajectory_eval = await judge.evaluate_trajectory(
        expected_trajectory=["search", "retrieve", "generate"],
        actual_trajectory=["search", "retrieve", "generate", "validate"]
    )
    
    print(f"Trajectory Score: {trajectory_eval.get('score')}")
    
    # Exemplo 3: Comparar respostas
    responses = [
        {"label": "GPT-4", "response": "Resposta do GPT-4..."},
        {"label": "Gemini", "response": "Resposta do Gemini..."}
    ]
    
    comparison = await judge.compare_responses(
        user_query="Explique machine learning",
        responses=responses
    )
    
    print(f"Melhor resposta: {comparison.get('winner')}")
    print(f"Scores: {comparison.get('scores')}")


if __name__ == "__main__":
    asyncio.run(example_usage())

