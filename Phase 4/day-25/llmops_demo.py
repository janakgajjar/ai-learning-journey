# ============================================
# Program: LLMOps 
# Topic: Latency + Token Tacking
# # Phase: 4 | Day: 25
# ============================================

import os
import time
import datetime
import json
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
 
load_dotenv()

os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_PROJECT"] = "ai-learning-journey"
os.environ["LANGCHAIN_API_KEY"] = os.getenv(
    "LANGCHAIN_API_KEY", ""
)

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash-lite",
    google_api_key=os.getenv("GEMINI_API_KEY"),
    temperature=0.3
)

parser = StrOutputParser()

print("-" * 30)
print(" LLMOps + Monitoring Demo")
print("-" * 30)

## Demo 1: LATENCY MEASUREMENT
print("\n Demo 1: Latency Measurement")
print("-" * 20)

def measure_latency(question: str):
    start_time = datetime.datetime.now()

    prompt = PromptTemplate(
            input_variables=["question"],
            template="Answer briefly: {question}"
    )
    chain = prompt | llm | parser
            
    answer = chain.invoke({"question": question}) 
            
    end_time = datetime.datetime.now()
    
    # Latency Calculate
    latency = (end_time - start_time).total_seconds()

    return answer, round(latency, 2)

test_questions = [
    "What is AI?",
    "Compare RAG vs Fine-tuning with examples"
]

latency_results = []

for q in test_questions:
    print(f"\n Testing: '{q[:40]}'")

    answer, latency = measure_latency(q)

    latency_results.append({
        "question": q,
        "latency": latency,
        "answer_length": len(answer)
    })

    print(f" Latency: {latency}s")
    print(f" Answer length: {len(answer)} chars")

    time.sleep(30)

avg_latency = sum(
    r["latency"] for r in latency_results
) / len(latency_results)

print(f"\n Average Latency: {round(avg_latency, 2)}s")

## Demo 2: Token Tracking
print("\n Demo 2: Token + Cost Tracking")
print("-" * 20)

def track_tokens(prompt_text: str):
    word_count = len(prompt_text.split())
    estimated_tokens = int(word_count * 1.3)

    #llm call
    response =llm.invoke(prompt_text)
    answer = response.content

    # response tokens estimate
    response_words = len(answer.split())
    response_tokens = int(response_words * 1.3)

    #cost estimate
    total_tokens = estimated_tokens + response_tokens
    estimated_cost = total_tokens * 0.000000125

    return {
        "prompt_tokens": estimated_tokens,
        "response_tokens": response_tokens,
        "total_tokens": total_tokens,
        "estimated_cost_usd": round(estimated_cost, 8),
        "answer": answer
    }

prompts = {
    "Short": "What is RAG?",
    "Medium": """Explain RAG (Retrieval Augmented Generation)
    in detail with architecture, components, and examples.""",
    "Long": """Provide a comprehensive analysis of RAG systems:
    1.Defination and overview
    2.Architecture components
    3.Comparison with fine-tuning
    4.Real-world use case
    5.Advantages nd limitations
    6.Implementation steps
    7.Best practices for production"""
}

print("\nPrompt Size Comparsion:")
for size, prompt in prompts.items():
    result = track_tokens(prompt)
    print(f"\n Prompt:")
    print(f"Input tokens: ~{result['prompt_tokens']}")
    print(f" Output tokens: ~{result['response_tokens']}")
    print(f" Total tokens: ~{result['total_tokens']}")
    print(f" Est. Cost: ${result['estimated_cost_usd']}")
    time.sleep(120)

report = {
    "latency-results": latency_results,
    "token_results": "Tracked above"
}

with open("part1_report.json", "w") as f:
    json.dump(report, f, indent=2)