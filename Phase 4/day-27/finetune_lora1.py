# ============================================
# Program: Fine-tuning + LoRA Demo Part 1
# Topic: Concept + Simulation
# Phase: 4 | Day: 27
# ============================================

import os
import time
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
parser =StrOutputParser()

print("-" * 30)
print(" Fine tuning + LoRA ")
print("-" * 30)

## Demo 1: Fine Tuning Vs RAG 
print("\n Demo 1. Fine Tuning Vs RAG")
print("-" * 20)

def compare_approaches(question: str):
    print(f"\n Question: {question}")

    # Approach 1: Fine Tuned
    finetuned_prompt = f"""You are a specialized AI tutor fine-tuned
    apecifically for MCA Agentic AI students.
    You always:
    - Use simple Gujarati student friendly language
    - Give exactly 3 bullet points
    - End with "Keep learning!!"

    Question: {question}"""
    
    ft_response = llm.invoke(finetuned_prompt)
    ft_answer = ft_response.content

    print(f"\n Fine tuned Style:")
    print(ft_answer[:300])

    time.sleep(10)

    # Approach 2 : RAG
    rag_context = """
    Contect from retrieved documents:
    - Agentic AI system use LLMs + Tools + Memory
    - Langchain provide agent building framework
    - RAG combines search with generation
    - CrewAI enbales multi-agent collaboration
    """

    rag_prompt = f"""Based on this context:
    {rag_context}

    Answer this question clearly:
    {question}"""

    rag_response = llm.invoke(rag_prompt)
    rag_answer = rag_response.content

    print(f"\n RAG Style:")
    print(rag_answer[:300])

    return ft_answer, rag_answer

test_questions = [
    "What is Agentic AI?",
    "How does RAG work?"
]

comparison_results = []

for q in test_questions:
    ft, rag = compare_approaches(q)
    comparison_results.append({
        "question": q,
        "finetuned_length": len(ft),
        "rag_length": len(rag)
    })
    time.sleep(15)


## LoRA Concept
print("\n\n Demo 2: LoRA Concept")
print("-" * 20)

print(""" 
 LoRA Concept Explained:
 
 Original Model (Large):
- Billions of parameters
- Frozen during LoRA training
- Not changed at all!!

LoRA Adapters (small):
- Few million parameters
- Added on top of original
- ONLY these train!!
      
Math Behind LoRA:
- Weight matrix w (large, frozen)
- LoRA adds: W + (A * B)
- A, B = Small matrices (trainable)
- Rank r = How small A, B are
- Lower rank = Fewer parameters
""")

print("Simulating LoRA Adapters:")
print("-" * 20)

#Base model response, No adapter
base_question = "Explain machine lerning"

print(f"\n Question: '{base_question}'")

#Base model
base_prompt = f"Answer thsi question: {base_question}"
base_response = llm.invoke(base_prompt)
base_answer = base_response.content

print(f"\n Base Model :")
print(base_answer[:200])

time.sleep(15)

adapter1_prompt = f"""You are using MCA_Tutor_Adapter_v1.
This adapter makes you:
- Speak like a friendly professor
- Use simple examples from daily life
- Add encouraging words

{base_question}"""

adapter1_response = llm.invoke(adapter1_prompt)
adapter1_answer = adapter1_response.content

print(f"\n With MCA Tutor Adapter:")
print(adapter1_answer[:200])

time.sleep(15)

adapter2_prompt = f"""You are using TechExpert_Adapter_v2.
This adapter makes you:
- Use technical terminology
- Include mathematical concepts
- Reference research papers

{base_question}"""

adapter2_response = llm.invoke(adapter2_prompt)
adapter2_answer = adapter2_response.content

print(f"\n With Tech Expert Adapter:")
print(adapter2_answer[:200])


## Save Results

results = {
    "comparison": comparison_results,
    "lora_demo": {
        "base_length": len(base_answer),
        "adapter1_length": len(adapter1_answer),
        "adapter2_length": len(adapter2_answer)
    }
}

with open("part1_results.json", "w") as f:
    json.dump(results, f, indent=2)