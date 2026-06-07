from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
import os

load_dotenv()

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash-lite",
    google_api_key=os.getenv("GEMINI_API_KEY"),
    temperature=0.3
)

parser = StrOutputParser()

print("-" * 30)
print(" Plan Execute Reflextion")
print("-" * 30)

##Demo 1 : Plan Exceuete reflextion

print("\n Demo 1:")
print("-" * 20)

#step 1: Planning

planner_template = PromptTemplate(
    input_variables=["task"],
    template="""You are a planning AI agent.
    
Create a detailed step by step plan for this task :
Task : {task}

Output format:
PLAN :
step 1: [action]
step 2: [action]
step 3: [action]
step 4: [action]
step 5: [action]

Keep each step clear and actionable."""
)

#step 2 : Executing 

executor_template = PromptTemplate(
    input_variables=["task", "plan", "step"],
    template="""You are a execution AI agent.

Original Task : {task}
Full Plan : {plan}
Current step to Execute : {step}

Execute this step and provide detailed output.
Be specific and thorough."""
)

planner_chain = planner_template | llm | parser
executor_chain = executor_template | llm | parser


task = "Create a beginner's guide to Agentic AI for MCA students"

print(f"\n Task : {task}\n")

print("Planning Phase .....")
plan = planner_chain.invoke({"task": task})
print(f"Plan Created :\n{plan}\n")

print("Execution Phase.....")
steps = [line for line in plan.split('\n')
         if line.strip().startswith('Step')][:3]

for i, step in enumerate(steps, 1):
    print(f"\n Executing {step}....")
    result = executor_chain.invoke({
        "task": task,
        "plan": plan,
        "step": step
    })
    print(f"Result: {result[:200]}")


## Demo 2 : Reflextion Pattern 

print("\n\n Demo 2: Reflextion Pattern ")
print("-" * 30)

initial_template = PromptTemplate(
    input_variables=["question"],
    template= "Answer this question clearly : {question}"
)

critique_template = PromptTemplate(
    input_variables=["question", "answer"],
    template="""Review this answer critically :

Question: {question}
Answer: {answer}

Critique:
1. What is missing?
2. what could be clearer?
3. Any errors?
4. How to improve?

Be specific in your critique."""
)

improve_template = PromptTemplate(
    input_variables=["question", "answer", "critique"],
    template="""Improve this answer based on critique:
    
Original Question: {question}
Original Answer: {answer}
Critique: {critique}

Write an improved, comprehensive answer."""
)

initial_chain = initial_template | llm | parser
critique_chain = critique_template | llm | parser
improve_chain = improve_template | llm | parser

question = "What is Agentic AI and why is it important?"

print(f"Question : {question}\n")

print("Round 1: Initial Answer ....")
answer_v1 = initial_chain.invoke({"question": question})
print(f"Answer v1:\n{answer_v1[:300]}\n")

print("Self Critique....")
critique = critique_chain.invoke({
    "question": question,
    "answer": answer_v1
})
print(f"Critique:\n{critique[:300]}\n")

print("Round 2: Improved Answer...")
answer_v2 = improve_chain.invoke({
    "question" : question,
    "answer": answer_v1,
    "critique": critique
})

print(f"Answer v2 (Improved):\n{answer_v2[:400]}")

print("\n Reflextion complete!!")
print("Notice : v2 is better than v1!!")