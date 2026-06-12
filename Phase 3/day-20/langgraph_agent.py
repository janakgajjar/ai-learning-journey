# ============================================
# Program: LangGraph Stateful Agent
# Topic: Graph-based Agent Workflows
# Phase: 3 | Day: 20
# Concept: Nodes + Edges + State Management
# ============================================

from langgraph.graph import StateGraph, END
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from typing import TypedDict, List
from dotenv import load_dotenv
import os

load_dotenv()

print("-" * 30)
print(" LangGraph Stateful Agent ")
print("-" * 30)

# LLM Setup
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash-lite",
    google_api_key=os.getenv("GEMINI_API_KEY"),
    temperature=0.3
)
parser = StrOutputParser()

# Step 1: Define State
print("\n Step 1: Define State")
print("-" * 20)

class AgentState(TypedDict):
    question: str
    answer: str
    quality_score: int
    iteration: int
    feedback: str
    final_answer: str

print("State defined!!")
print("  Fields: question, answer, quality_score, iteration, feedback, final_answer")

# Step 2: Define Nodes
print("\n Step 2: Define Nodes(steps)")
print("-" * 20)

# Node 1: Generate Answer
def generate_answer(state: AgentState) -> AgentState:
    """Generate initial answer"""
    print(f"\n Node 1: Generating answer....")
    print(f" Iteration: {state['iteration']}")

    prompt = PromptTemplate(
        input_variables=["question", "feedback"],
        template="""Answer this question clearly for MCA studentes.
        
Question: {question}

Previous feedback (if any): {feedback}

Provide a clear, accurate answer:"""
    )
    chain = prompt | llm | parser
    answer = chain.invoke({
        "question": state["question"],
        "feedback": state.get("feedback", "No previous attempt")
    })

    return {
        **state,
        "answer": answer,
        "iteration": state["iteration"] + 1
    }

# Node 2: Evaluate Quality
def evaluate_quality(state: AgentState) -> AgentState:
    """Evaluate answer quality"""
    print(f"\n  Node 2: Evaluating quality....")

    eval_prompt = PromptTemplate(
        input_variables=["question", "answer"],
        template="""Evaluate this answer quality.
        
Question: {question}
Answer: {answer}

Rate the answer from 1-10 and provide feedback.
Respond EXACTLY in this format:
SCORE: [number 1-10]
FEEDBACK: [what is good/missing]"""
    )
    chain = eval_prompt | llm | parser
    evaluation = chain.invoke({
        "question": state["question"],
        "answer": state["answer"]
    })

    ## Parse score
    score = 7 # default
    feedback = evaluation

    for line in evaluation.split('\n'):
        if line.startswith("SCORE:"):
            try: 
                score =int(line.replace("SCORE:", "").strip())
            except:
                score = 7
        elif line.startswith("FEEDBACK:"):
            feedback = line.replace("FEEDBACK:", "").strip()

    print(f" Quality Score: {score}/10")
    print(f" Feedback : {feedback[:80]}...")

    return {
        **state,
        "quality_score": score,
        "feedback": feedback
    }

# Node 3: Finalize Answer
def finalize_answer(state: AgentState) -> AgentState:
    """Finalize the answer"""
    print(f"\n Node 3: Finalizing Answer...")

    final_prompt = PromptTemplate(
        input_variables=["answer"],
        template="""Polish ans formate this answer beautifully:
        
{answer}

Make it clear, well-structured, and student-friendly:"""
    )
    chain = final_prompt | llm | parser
    final = chain.invoke({"answer": state["answer"]})

    return {
        **state,
        "final_answer": final
    }

print(" Nodes defined!")
print(" Node 1: Generate_answer")
print(" Node 2: evaluate_quality")
print(" Node 3: finalize_answer")


## Step 3: Define Routing Logic
print("\n Step 3: Define Routing (EDGES)")
print("-" * 20)

def should_continue(state: AgentState) -> str:
    """Decide : improve or finalize?"""
    score = state.get("quality_score", 0)
    iteration = state.get("iteration", 0)

    if score >= 7:
        print(f" -> Score {score} >= 7: FINALIZE!!")
        return "finalize"
    elif iteration >= 3:
        print(f" -> Max iterations reached: FINALIZE!!")
        return "finalize"
    else:
        print(f" -> Score {score} < 7: IMPROVE!")
        return "improve"

print(" Routing defined!!")
print(" Score >= 7 -> Finalize")
print(" Score < 7 -> Improve (max 3 times)")


## Step 4: Build Graph
print("\n Step 4: Building Graph")
print("-" * 20 )

workflow = StateGraph(AgentState)

#Add Nodes
workflow.add_node("generate", generate_answer)
workflow.add_node("evaluate", evaluate_quality)
workflow.add_node("finalize", finalize_answer)

#Add Edges
workflow.set_entry_point("generate")
workflow.add_edge("generate", "evaluate")
workflow.add_conditional_edges(
    "evaluate",
    should_continue,
    {
        "improve": "generate",
        "finalize": "finalize"
    }
)
workflow.add_edge("finalize", END)

# Compile
app = workflow.compile()
print("Graph complied!!")

# Step 5: Run Agent
print("\n Step 5: Running Agent")
print("-" * 20)

test_questions = [
    "What is Agentic AI and why is is important?",
    "Explain RAG i simple terms with an example"
]

for question in test_questions:
    print(f"\n Question: {question}")
    print("-" * 20)

    initial_state = AgentState(
        question=question,
        answer="",
        quality_score=0,
        iteration=0,
        feedback="",
        final_answer=""
    )

    result = app.invoke(initial_state)

    print(f"\n Final Answer:")
    print(f"{result['final_answer'][:400]}")
    print(f"\n Status:")
    print(f" Iterations: {result['iteration']}")
    print(f" Final Score: {result['quality_score']}/10")
    print("-" * 30)