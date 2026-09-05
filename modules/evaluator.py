import json


def create_evaluation_prompt(question, answer):

    return f"""
You are an AI response evaluator for CognitiveNexus.

Evaluate the following question and answer.

USER QUESTION:
{question}

AI ANSWER:
{answer}

Evaluate the answer using these four criteria:

1. Relevance
2. Completeness
3. Accuracy
4. Hallucination Risk

Give each score from 1 to 10.

Return ONLY valid JSON using this format:

{{
    "relevance": 0,
    "completeness": 0,
    "accuracy": 0,
    "hallucination_risk": 0,
    "overall_score": 0,
    "summary": "Short explanation of the evaluation."
}}
"""


def parse_evaluation(response_text):

    try:

        return json.loads(response_text)

    except Exception:

        return {
            "relevance": "N/A",
            "completeness": "N/A",
            "accuracy": "N/A",
            "hallucination_risk": "N/A",
            "overall_score": "N/A",
            "summary": response_text
        }