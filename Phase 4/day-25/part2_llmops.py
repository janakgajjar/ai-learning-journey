# ============================================
# Program: LLMOps 
# Topic: Caching + Versioning + Monitoring
# Phase: 4 | Day: 25
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

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash-lite",
    google_api_key=os.getenv("GEMINI_API_KEY"),
    temperature=0.3
)
parser = StrOutputParser()

## Demo 1: CACHING SIMULATION
print("\n Demo 1: Caching - Same Answer Fast!!")
print("-" * 20)

cache = {}

def cached_llm_call(question: str):
    if question in cache:
        print("Cache HIT ! No API call needed!!")
        return cache[question], 0.0 # 0 latency from cache
    
    print(" Caceh MISS!! Calling API..")

    start = datetime.datetime.now()
    response = llm.invoke(question)
    end = datetime.datetime.now()

    latency = (end - start).total_seconds()
    answer = response.content

    cache[question] = answer

    return answer, round(latency, 2)

same_question = "what is Agentic AI?"

print(f"\n Question: '{same_question}'")
print("\nCall 1 (First time):")
ans1, lat1 = cached_llm_call(same_question)
print(f" Latency: {lat1}s")

time.sleep(10)

print("\nCall 2 (Same question - from cache):")
ans2, lat2 =cached_llm_call(same_question)
print(f"Latency: {lat2}s")

print("\nCall 3 (Same Question - from cache):")
ans3, lat3 = cached_llm_call(same_question)
print(f"Latency: {lat3}s")

if lat1 > 0:
    savings = round(((lat1 - lat2) / lat1) * 100, 1)
    print(f"\n Cache saved {savings} % time on repeat calls!")


## Demo 2: PROMPT VERSIONING
print("\n Demo 2: Prompt VersionManagement")
print("-" * 20)

prompt_versions = {
    "v1_basic": "Explain {topic}",
    
    "v2_structured": """Explain {topic} clearly.
    Include: definition, example, use case.""",
    
    "v3_optimized": """You are an expert AI tutor 
    for MCA students.
    
    Explain '{topic}' with:
    1. Simple definition (1 sentence)
    2. Real-world example
    3. Why students should learn this
    
    Keep it under 150 words."""
}

topic = "Vector Databases"
print(f"\nTesting different prompts for: '{topic}'")

version_results = {}

for version, template in prompt_versions.items():
    print(f"\n {version}:")

    prompt_text = template.replace("{topic}", topic)

    start = datetime.datetime.now()
    response = llm.invoke(prompt_text)
    end = datetime.datetime.now()

    latency = (end - start).total_seconds()
    answer = response.content

    version_results[version] = {
        "latency": round(latency, 2),
        "length": len(answer),
        "preview": answer[:100]
    }

    print(f" Latency: {round(latency, 2)}s")
    print(f" Length: {len(answer)} chars")
    print(f" Preview: {answer[:80]}...")

    time.sleep(10)

best = min(
    version_results.items(),
    key=lambda x: x[1]["latency"] 
)
print(f"\n Fastest Version: {best[0]}")


## Demo 3: PRODUCTION MONITORING LOG
print("\n Demo 3: Production Monitoring")
print("-" * 20)

monitoring_log = []

def monitored_llm_call(
        question: str,
        user_id: str = "student_001"
):
    
    log_entry = {
        "timestamp": datetime.datetime.now().isoformat(),
        "user_id": user_id,
        "question": question,
        "status": "pending",
        "latency": 0,
        "error": None
    }

    try:
        start = datetime.datetime.now()
        response = llm.invoke(question)
        answer = response.content
        end = datetime.datetime.now()

        log_entry["status"] = "success"
        log_entry["latency"] = round((end - start).total_seconds(), 2)
        log_entry["answer_length"] = len(answer)

        monitoring_log.append(log_entry)
        return answer
    
    except Exception as e:
        log_entry["status"] = "error"
        log_entry["error"] = str(e)
        monitoring_log.append(log_entry)
        return f"Error: {str(e)}"
    
test_calls = [
    ("What is Langchain?", "student_001"),
    ("Explain RAG simply", "student_002"),
    ("What is CrewAI?","student_001"),
]

for question, user in test_calls:
    print(f"\n Call: '{question[:40]}")
    print(f" User: {user}")
    result = monitored_llm_call(question, user)
    print(f" Status: Success")
    time.sleep(10)

print("\n Monitoring Report")
print("-" * 20)

total_calls = len(monitoring_log)
success_calls = sum(
    1 for l in monitoring_log if l["status"] == "success" 
)
avg_lat = sum(
    l["latency"] for l in monitoring_log
) / total_calls

print(f" Total Calls: {total_calls}")
print(f" Success Rate: {success_calls}/{total_calls}")
print(f"Avg Latency: {round(avg_lat, 2)}s")

report = {
    "summary": {
        "total_calls": total_calls,
        "success_rate": f"{success_calls}/{total_calls}",
        "avg_latency": round(avg_lat, 2)
    },
    "logs": monitoring_log
}

with open("part2_report.json", "w") as f:
    json.dump(report, f, indent=2)