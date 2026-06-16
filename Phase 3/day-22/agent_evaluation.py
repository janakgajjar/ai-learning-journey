# ============================================
# Program: Agent Evaluation System
# Topic: Measuring AI Agent Performance
# Phase: 3 | Day: 22
# Concept: Metrics, Benchmarks, Quality Check
# ============================================

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
import os
import time
import json

load_dotenv()

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash-lite",
    google_api_key=os.getenv("GEMINI_API_KEY"),
    temperature=0.1
)
parser = StrOutputParser()

print("-" * 30)
print(" Agent Evaluation System")
print("-" * 30)

## Evaluation Framework

# Test Dataset 9Question + Expected Answer)
# Test Dataset (9 Question + Expected Answer)
test_dataset = [
    {
        "id": 1,
        "question": "What is RAG in AI?",
        "expected_keywords": ["retrieval", "generation", "documents", "context"], # Fixed missing 'd'
        "difficulty": "easy"
    },
    {
        "id": 2,
        "question": "Explain the difference between LangChain and LangGraph", # Fixed "Explin"
        "expected_keywords": ["framework", "graph", "workflow", "chain"],
        "difficulty": "medium"
    },
    {
        "id": 3,
        "question": "What are the 4 types of agent memory?",
        "expected_keywords": ["short-term", "long-term", "episodic", "semantic"], # Fixed "lon-term"
        "difficulty": "medium"
    },
    {
        "id": 4,
        "question": "What is the ReAct pattern in AI agents?",
        "expected_keywords": ["reason", "act", "observe", "thought", "action"],
        "difficulty": "easy"
    },
    {
        "id": 5,
        "question": "Explain Multi-Agent systems and give an example",
        "expected_keywords": ["multiple", "agents", "collaborate", "crewai", "orchestrator"],
        "difficulty": "hard"
    }
]


## Metric 1: Keyword Coverage Score
def calculate_keyword_score(answer, keywords):
    """check how many expected keywords apper"""
    answer_lower = answer.lower()
    found = [kw for kw in keywords if kw.lower() in answer_lower]
    score = len(found) / len(keywords) * 10
    return round(score, 1), found

## Metric 2: AI Self-Evaluation Score
def ai_evaluate(question, answer):
    """Use AI to evaluate answer quality"""
    eval_template = PromptTemplate(
        input_variables=["question", "answer"],
        template="""Evaluate this AI answer strictly.
        
Question: {question}
Answer: {answer}

Rate ONLY on these criteria (1-10 each):
1. Accuracy (factually correct?)
2. Completness (covers main points?)
3. Clarity (easy to understand?)

Respond ONLY in this JSON format:
{{"accuracy": X, "completeness": X, "clarity": X, "overall": X}}"""
    )
    chain = eval_template | llm |parser
    result = chain.invoke({
        "question": question,
        "answer": answer
    })

    try:
        # Extract JSON
        start = result.find("{")
        end = result.rfind("}") + 1
        if start != -1 and end != 0:
            scores =json.loads(result[start:end])
            return scores
    except:
        pass

    return {
        "accuracy": 7,
        "completeness": 7,
        "clarity": 7,
        "overall": 7
    }

## Metric 3: Latency Measurement
def measure_latency(question):
    """Measure response time"""
    import datetime
    start = datetime.datetime.now()

    response_template = PromptTemplate(
        input_variables=["question"],
        template ="Answer clearly for MCA students: {question}"
    )
    chain = response_template | llm | parser
    answer = chain.invoke({"question": question})

    end =datetime.datetime.now()
    latency = (end - start).total_seconds()

    return answer, round(latency, 2)

## Run Evaluation
print("\n Running Agent Evaluation Suite")
print("-" * 20)

results = []

for test in test_dataset[:3]:  # Test first 3 to save API calls
    print(f"\n Test {test['id']}: {test['question'][:50]}...")
    print(f" Difficulty: {test['difficulty']}")

    # Get answer + latency
    answer, latency = measure_latency(test['question'])
    time.sleep(4)

    # Keyword score
    keyword_score, found_kws = calculate_keyword_score(
        answer, test['expected_keywords']
    )

    # AI Evaluation
    ai_score = ai_evaluate(test['question'], answer)
    time.sleep(4)

    result = {
        "id": test['id'],
        "question": test['question'],
        "answer_preview": answer[:100] + "..",
        "latency_sec": latency,
        "keyword_score": keyword_score,
        "found_keywords": found_kws,
        "ai_scores": ai_score
    }
    results.append(result)

    print(f" Latency: {latency}s")
    print(f" Keyword Score: {keyword_score}/10")
    print(f" Found: {found_kws}")
    print(f" AI Scores: {ai_score}")

## Summary report
print("\n\n Evaluation Summary Report")
print("-" * 20)

avg_latency = sum(r['latency_sec'] for r in results) / len(results)
avg_keyword = sum(r['keyword_score'] for r in results) / len(results)
avg_overall = sum(
    r['ai_scores'].get('overall', 7) for r in results
) / len(results)

print(f"\n Tests completed: {len(results)}/5")
print(f" Average Latency: {round(avg_latency, 2)}s")
print(f" Average Keyword Score: {round(avg_keyword, 1)}/10")
print(f" Average AI Score: {round(avg_overall, 1)}/10")

## Overall Grade
overall = (avg_keyword + avg_overall) / 2
if overall >= 8:
    grade = "A - Excellent!"
elif overall >= 6:
    grade = "B - Good"
elif overall >= 4:
    grade = "C - Needs Improvement"
else:
    grade = "D - Poor"

print(f"\n Overall Grade:{grade}")
print(f"Overall Score: {round(overall, 1)}/10")

## Save report
report = {
    "summary": {
        "tests": len(results),
        "avg_latency": round(avg_latency, 2),
        "avg_keyword_score": round(avg_keyword, 1),
        "avg_ai_score": round(avg_overall, 1),
        "overall_score": round(overall, 1),
        "grade": grade
    },
    "detailed_results": results
}

with open("evaluation_report.json", "w") as f:
    json.dump(report, f, indent=2)