# ============================================
# Program: Research Assistant Agent — Part 1
# Topic: Core Agent + Tools + Memory
# ============================================

import os
import time
import json
import datetime
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate

load_dotenv()

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash-lite",
    google_api_key=os.getenv("GEMINI_API_KEY"),
    temperature=0.4
)

parser = StrOutputParser()

print("=" * 55)
print("   Research Assistant Agent — Part 1")
print("   Core Tools + Memory System")
print("=" * 55)

# MEMORY SYSTEM
class AgentMemory:
    def __init__(self):

        self.history = []
        self.session_id = datetime.datetime.now().strftime(
            "%Y%m%d_%H%M%S"
        )
        self.max_history = 5

    def add_interaction(self, topic: str, result: str):
        interaction = {
            "timestamp": datetime.datetime.now().isoformat(),
            "topic": topic,
            "result": result[:200]
        }
        self.history.append(interaction)

        if len(self.history) > self.max_history:
            self.history = self.history[1:]

    def get_context(self) -> str:

        if not self.history:
            return "No previous research done."

        context_lines = [
            f"Previously researched: {h['topic']}"
            for h in self.history
        ]
        return "\n".join(context_lines)

    def save_to_file(self, filename: str = "memory.json"):

        memory_data = {
            "session_id": self.session_id,
            "history": self.history,
            "total_interactions": len(self.history)
        }
        with open(filename, "w") as f:
            json.dump(memory_data, f, indent=2)

        print(f"   💾 Memory saved: {filename}")

memory = AgentMemory()
print(f"Memory System Ready!")
print(f"   Session ID: {memory.session_id}")

# TOOL DEFINITIONS

print("\n Defining Agent Tools...")
print("-" * 40)

def research_tool(topic: str) -> str:

    print(f"\n    Research Tool: '{topic}'")

    research_prompt = PromptTemplate(
        input_variables=["topic", "context"],
        template="""You are an expert AI researcher.

Previous research context:
{context}

Research this topic thoroughly: '{topic}'

Provide structured research:
[2-3 sentence overview]
[5 important points as bullets]
[3 practical examples]
[2-3 latest developments]
[2-3 main challenges]

Be accurate and student-friendly."""
    )

    research_chain = research_prompt | llm | parser

    result = research_chain.invoke({
        "topic": topic,
        "context": memory.get_context()
    })
    memory.add_interaction(topic, result)

    return result

def summary_tool(research_text: str) -> str:

    print(f"\n    Summary Tool: Summarizing...")

    summary_prompt = PromptTemplate(
        input_variables=["text"],
        template="""Summarize this research for MCA students.

Research:
{text}

Create EXACTLY this format:

-> EXECUTIVE SUMMARY (2 sentences max):
[Core message]

-> KEY TAKEAWAYS (5 points):
- [Point 1]
- [Point 2]
- [Point 3]
- [Point 4]
- [Point 5]

-> BOTTOM LINE (1 sentence):
[Most important insight]

Keep under 200 words total."""
    )

    summary_chain = summary_prompt | llm | parser

    result = summary_chain.invoke({
        "text": research_text
    })

    return result

def question_generator_tool(topic: str) -> str:

    print(f"\n    Question Generator: '{topic}'")

    question_prompt = PromptTemplate(
        input_variables=["topic"],
        template="""Generate exam-style questions for: '{topic}'

Create EXACTLY:
-> MCQ QUESTIONS (3):
Q1. [Question]
a) [Option A]  b) [Option B]
c) [Option C]  d) [Option D]
Answer: [Letter]

Q2. [Question]
a) [Option A]  b) [Option B]  
c) [Option C]  d) [Option D]
Answer: [Letter]

Q3. [Question]
a) [Option A]  b) [Option B]
c) [Option C]  d) [Option D]
Answer: [Letter]

-> SHORT ANSWER (2):
Q4. [Question] (Answer in 2-3 lines)
Q5. [Question] (Answer in 2-3 lines)

-> LONG ANSWER (1):
Q6. [Detailed question] (Answer in paragraph)

Suitable for MCA Agentic AI exam."""
    )

    question_chain = question_prompt | llm | parser

    result = question_chain.invoke({"topic": topic})

    return result

TOOLS = {
    "research": research_tool,    
    "summarize": summary_tool,    
    "questions": question_generator_tool 
}

print("Tools Ready:")
for name in TOOLS.keys():
    print(f"   → {name}")

# REACT LOOP IMPLEMENTATION

print("\n  ReAct Loop System Ready")
print("-" * 40)

def run_react_agent(topic: str) -> dict:

    print(f"\n ReAct Agent Starting...")
    print(f"   Topic: '{topic}'")
    print("-" * 40)

    state = {
        "topic": topic,
        "iteration": 0,
        "max_iterations": 3,
        "results": {},
        "complete": False
    }

    plan_prompt = PromptTemplate(
        input_variables=["topic", "tools"],
        template="""You are a ReAct agent.
        
Topic to research: '{topic}'

Available tools: {tools}

Create a plan using EXACTLY this format:
THOUGHT: [What I need to do]
ACTION: [Which tool to use first]
INPUT: [What to pass to tool]
REASON: [Why this tool first]"""
    )

    tools_list = ", ".join(TOOLS.keys())

    plan_chain = plan_prompt | llm | parser
    print("\nTHOUGHT: Planning research...")
    initial_plan = plan_chain.invoke({
        "topic": topic,
        "tools": tools_list
    })
    print(f"   Plan:\n{initial_plan[:200]}")
    time.sleep(8)

    while (
        not state["complete"] and
        state["iteration"] < state["max_iterations"]
    ):
        state["iteration"] += 1
        current_iter = state["iteration"]

        print(f"\n{'='*40}")
        print(f" ITERATION {current_iter}")
        print(f"{'='*40}")

        if current_iter == 1:
            print(" ACTION: Using research tool")
            result = TOOLS["research"](topic)
            state["results"]["research"] = result
            print(f"    Research complete!")
            print(f"   Length: {len(result)} chars")

        elif current_iter == 2:
            print(" ACTION: Using summary tool")

            research = state["results"].get(
                "research", ""
            )
            result = TOOLS["summarize"](research)
            state["results"]["summary"] = result
            print(f"    Summary complete!")

        elif current_iter == 3:
            print(" ACTION: Generating questions")
            result = TOOLS["questions"](topic)
            state["results"]["questions"] = result
            print(f"    Questions generated!")

            state["complete"] = True
            print("\n OBSERVE: All tasks done!")

        if not state["complete"]:
            print(f"    Waiting 15 sec...")
            time.sleep(15)

    final_result = {
        "topic": topic,
        "iterations": state["iteration"],
        "research": state["results"].get("research", ""),
        "summary": state["results"].get("summary", ""),
        "questions": state["results"].get("questions", ""),
        "memory_context": memory.get_context(),
        "timestamp": datetime.datetime.now().isoformat()
    }

    return final_result

# RUN THE AGENT
print("\n Starting Research Agent...")

test_topic = "Agentic AI in Enterprise Applications"
result = run_react_agent(test_topic)

# DISPLAY RESULTS
print("\n" + "=" * 55)
print(" RESEARCH RESULTS")
print("=" * 55)

print(f"\n Topic: {result['topic']}")
print(f" Iterations: {result['iterations']}")

print(f"\n SUMMARY:")
print(result['summary'][:400])

print(f"\n SAMPLE QUESTIONS:")
print(result['questions'][:300])

with open("research_result.json", "w") as f:
    json.dump(result, f, indent=2)

memory.save_to_file("agent_memory.json")

print("\n Files Saved:")
print("   → research_result.json")
print("   → agent_memory.json")
