"""
Templates de prompts para diferentes tipos de avaliação com LLM Judge.

Este módulo fornece templates reutilizáveis para diferentes cenários de avaliação.
"""

from typing import Dict, Any, Optional
import json


class JudgePromptTemplates:
    """Templates de prompts para LLM Judge"""
    
    @staticmethod
    def trajectory_evaluation(
        expected_trajectory: list,
        actual_trajectory: list,
        context: Optional[Dict[str, Any]] = None,
        criteria: Optional[Dict[str, str]] = None
    ) -> str:
        """
        Template para avaliação de trajetória de agente.
        
        Args:
            expected_trajectory: Trajetória esperada
            actual_trajectory: Trajetória real
            context: Contexto adicional
            criteria: Critérios customizados
            
        Returns:
            Prompt formatado
        """
        default_criteria = {
            "order": "As ações foram executadas na ordem correta?",
            "completeness": "Todas as ações necessárias foram executadas?",
            "efficiency": "A trajetória foi eficiente (sem ações desnecessárias)?",
            "correctness": "As ações são apropriadas para o contexto?"
        }
        
        criteria_text = "\n".join([
            f"- {key}: {value}"
            for key, value in (criteria or default_criteria).items()
        ])
        
        return f"""
Você é um juiz especializado em avaliar trajetórias de agentes de IA.

Trajetória Esperada: {json.dumps(expected_trajectory, ensure_ascii=False)}
Trajetória Real: {json.dumps(actual_trajectory, ensure_ascii=False)}
Contexto: {json.dumps(context or {}, ensure_ascii=False, indent=2)}

Critérios de Avaliação:
{criteria_text}

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
    
    @staticmethod
    def response_quality(
        user_query: str,
        agent_response: str,
        expected_response: Optional[str] = None,
        context: Optional[Dict[str, Any]] = None,
        criteria: Optional[Dict[str, str]] = None
    ) -> str:
        """
        Template para avaliação de qualidade de resposta.
        
        Args:
            user_query: Pergunta do usuário
            agent_response: Resposta do agente
            expected_response: Resposta esperada (opcional)
            context: Contexto adicional
            criteria: Critérios customizados
            
        Returns:
            Prompt formatado
        """
        default_criteria = {
            "correctness": "A resposta está factualmente correta?",
            "relevance": "A resposta é relevante à pergunta?",
            "completeness": "A resposta está completa?",
            "clarity": "A resposta é clara e bem estruturada?",
            "safety": "A resposta é segura e apropriada?"
        }
        
        criteria_text = "\n".join([
            f"- {key}: {value}"
            for key, value in (criteria or default_criteria).items()
        ])
        
        expected_section = ""
        if expected_response:
            expected_section = f"\nResposta Esperada (referência): {expected_response}"
        
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
    
    @staticmethod
    def comparative_evaluation(
        user_query: str,
        responses: list,
        context: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Template para avaliação comparativa de múltiplas respostas.
        
        Args:
            user_query: Pergunta do usuário
            responses: Lista de respostas para comparar
            context: Contexto adicional
            
        Returns:
            Prompt formatado
        """
        responses_text = "\n\n".join([
            f"Resposta {i+1} ({resp.get('label', f'Modelo {i+1}')}):\n{resp.get('response', '')}"
            for i, resp in enumerate(responses)
        ])
        
        return f"""
Você é um juiz especializado em comparar respostas de agentes de IA.

Pergunta: {user_query}

{responses_text}

Contexto: {json.dumps(context or {}, ensure_ascii=False, indent=2)}

Compare as respostas e forneça uma avaliação em JSON com:
- rankings: lista ordenada de índices (melhor primeiro, 0-indexed)
- scores: pontuações de 0-1 para cada resposta (lista na ordem das respostas)
- comparison: comparação detalhada entre as respostas
- winner: índice da melhor resposta (0-indexed)
- reasoning: raciocínio por trás da decisão
- strengths_by_response: pontos fortes de cada resposta (lista)
- weaknesses_by_response: pontos fracos de cada resposta (lista)
"""
    
    @staticmethod
    def conversational_quality(
        conversation_history: list,
        current_response: str,
        context: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Template para avaliação de qualidade conversacional.
        
        Args:
            conversation_history: Histórico da conversa
            current_response: Resposta atual do agente
            context: Contexto adicional
            
        Returns:
            Prompt formatado
        """
        history_text = "\n".join([
            f"{turn.get('role', 'user')}: {turn.get('content', '')}"
            for turn in conversation_history
        ])
        
        return f"""
Você é um juiz especializado em avaliar qualidade conversacional de agentes de IA.

Histórico da Conversa:
{history_text}

Resposta Atual do Agente: {current_response}
Contexto: {json.dumps(context or {}, ensure_ascii=False, indent=2)}

Avalie a resposta considerando:
- coherence: A resposta é coerente com o contexto da conversa? (0-1)
- relevance: A resposta é relevante para a pergunta atual? (0-1)
- helpfulness: A resposta é útil para o usuário? (0-1)
- naturalness: A resposta soa natural e conversacional? (0-1)
- completeness: A resposta está completa ou precisa de follow-up? (0-1)

Forneça uma avaliação em JSON com:
- score: pontuação geral de 0-1
- coherence: coerência com o contexto (0-1)
- relevance: relevância (0-1)
- helpfulness: utilidade (0-1)
- naturalness: naturalidade (0-1)
- completeness: completude (0-1)
- justification: justificativa detalhada
- strengths: lista de pontos fortes
- weaknesses: lista de pontos fracos
"""
    
    @staticmethod
    def code_quality(
        user_query: str,
        code: str,
        language: str = "python",
        context: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Template para avaliação de qualidade de código.
        
        Args:
            user_query: Requisito ou pergunta do usuário
            code: Código gerado
            language: Linguagem de programação
            context: Contexto adicional
            
        Returns:
            Prompt formatado
        """
        return f"""
Você é um juiz especializado em avaliar qualidade de código gerado por agentes de IA.

Requisito/Pergunta: {user_query}
Código Gerado ({language}):
```{language}
{code}
```
Contexto: {json.dumps(context or {}, ensure_ascii=False, indent=2)}

Avalie o código considerando:
- correctness: O código está correto e funciona? (0-1)
- efficiency: O código é eficiente? (0-1)
- readability: O código é legível e bem estruturado? (0-1)
- best_practices: O código segue melhores práticas? (0-1)
- documentation: O código está bem documentado? (0-1)
- security: O código é seguro? (0-1)

Forneça uma avaliação em JSON com:
- score: pontuação geral de 0-1
- correctness: correção (0-1)
- efficiency: eficiência (0-1)
- readability: legibilidade (0-1)
- best_practices: melhores práticas (0-1)
- documentation: documentação (0-1)
- security: segurança (0-1)
- justification: justificativa detalhada
- strengths: lista de pontos fortes
- weaknesses: lista de pontos fracos
- recommendations: recomendações de melhoria
- potential_bugs: possíveis bugs identificados (lista)
"""
    
    @staticmethod
    def rag_quality(
        user_query: str,
        agent_response: str,
        sources: list,
        context: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Template para avaliação de qualidade de resposta RAG.
        
        Args:
            user_query: Pergunta do usuário
            agent_response: Resposta do agente
            sources: Fontes utilizadas pelo RAG
            context: Contexto adicional
            
        Returns:
            Prompt formatado
        """
        sources_text = "\n".join([
            f"Fonte {i+1}: {source.get('content', '')[:200]}... (ID: {source.get('id', 'N/A')})"
            for i, source in enumerate(sources)
        ])
        
        return f"""
Você é um juiz especializado em avaliar respostas de agentes RAG (Retrieval-Augmented Generation).

Pergunta do Usuário: {user_query}
Resposta do Agente: {agent_response}

Fontes Utilizadas:
{sources_text}

Contexto: {json.dumps(context or {}, ensure_ascii=False, indent=2)}

Avalie a resposta considerando:
- answer_quality: A resposta está correta e completa? (0-1)
- source_relevance: As fontes são relevantes para a pergunta? (0-1)
- citation_accuracy: As citações estão corretas? (0-1)
- groundedness: A resposta está fundamentada nas fontes? (0-1)
- attribution: A atribuição às fontes está clara? (0-1)

Forneça uma avaliação em JSON com:
- score: pontuação geral de 0-1
- answer_quality: qualidade da resposta (0-1)
- source_relevance: relevância das fontes (0-1)
- citation_accuracy: precisão das citações (0-1)
- groundedness: fundamentação nas fontes (0-1)
- attribution: atribuição às fontes (0-1)
- justification: justificativa detalhada
- strengths: lista de pontos fortes
- weaknesses: lista de pontos fracos
- recommendations: recomendações de melhoria
- hallucination_check: há informações não fundamentadas nas fontes? (boolean)
"""


# Exemplo de uso
if __name__ == "__main__":
    templates = JudgePromptTemplates()
    
    # Exemplo 1: Avaliação de resposta
    prompt = templates.response_quality(
        user_query="O que é Python?",
        agent_response="Python é uma linguagem de programação de alto nível.",
        expected_response="Python é uma linguagem de programação interpretada de alto nível..."
    )
    print("=== Prompt de Avaliação de Resposta ===")
    print(prompt)
    print("\n")
    
    # Exemplo 2: Avaliação de código
    prompt = templates.code_quality(
        user_query="Crie uma função que calcula o fatorial",
        code="def factorial(n):\n    return 1 if n <= 1 else n * factorial(n-1)",
        language="python"
    )
    print("=== Prompt de Avaliação de Código ===")
    print(prompt)

