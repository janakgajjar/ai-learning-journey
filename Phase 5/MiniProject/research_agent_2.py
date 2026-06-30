# ============================================
# Program: Research Assistant Agent — Part 2
# Topic: Evaluation + Error Handling + Report
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
    temperature=0.3
)
parser = StrOutputParser()

print("=" * 55)
print("   Research Agent Part 2")
print("   Evaluation + Error Handling")
print("=" * 55)

# LOAD PART 1 RESULTS
print("\n Loading Part 1 Results...")

try:
    with open("research_result.json", "r") as f:
        research_data = json.load(f)

    print(f" Loaded: {research_data['topic']}")

except FileNotFoundError:
    print(" research_result.json not found!")
    print("   Run research_agent_part1.py first!")

    exit(1)

# EVALUATION SYSTEM
print("\n EVALUATION SYSTEM")
print("-" * 40)

class EvaluationSystem:
    def __init__(self):
        self.scores = {}

    def evaluate_completeness(
        self, research_text: str
    ) -> float:

        expected_keywords = [
            "agent", "llm", "memory",
            "tool", "planning", "autonomous",
            "workflow", "framework"
        ]

        text_lower = research_text.lower()

        found = [
            kw for kw in expected_keywords
            if kw in text_lower
        ]
        score = len(found) / len(expected_keywords) * 10

        return round(score, 1)

    def evaluate_length(
        self, research_text: str
    ) -> float:

        word_count = len(research_text.split())

        if 500 <= word_count <= 2000:
            score = 10.0
        elif 300 <= word_count < 500:
            score = 7.0
        elif 2000 < word_count <= 3000:
            score = 7.0
        elif word_count < 300:
            score = 4.0
        else:
            score = 5.0

        return score

    def evaluate_structure(
        self, research_text: str
    ) -> float:

        expected_sections = [
            "overview",
            "key concepts",
            "applications",
            "trends",
            "challenges"
        ]

        text_lower = research_text.lower()
        found_sections = [
            s for s in expected_sections
            if s in text_lower
        ]

        score = (
            len(found_sections) /
            len(expected_sections) * 10
        )
        return round(score, 1)

    def ai_quality_score(
        self,
        topic: str,
        research: str
    ) -> float:

        eval_prompt = PromptTemplate(
            input_variables=["topic", "research"],
            template="""Rate this research quality.

Topic: {topic}
Research (first 500 chars): {research}

Rate ONLY on:
1. Accuracy (correct info?)
2. Clarity (easy to understand?)
3. Relevance (on topic?)

Respond ONLY with a number 1-10.
Example response: 8
Nothing else, just the number."""
        )

        try:
            chain = eval_prompt | llm | parser
            result = chain.invoke({
                "topic": topic,
                "research": research[:500]
            })

            score = float(result.strip()[:2])

            if 1 <= score <= 10:
                return score
            else:
                return 7.0

        except Exception as e:
            print(f"   AI eval error: {e}")
            return 7.0

    def full_evaluation(
        self,
        topic: str,
        research: str,
        summary: str
    ) -> dict:

        print("\n Running Evaluation...")

        completeness = self.evaluate_completeness(research)
        print(f"   Completeness: {completeness}/10")
        time.sleep(3)

        length_score = self.evaluate_length(research)
        print(f"   Length: {length_score}/10")
        time.sleep(3)

        structure = self.evaluate_structure(research)
        print(f"   Structure: {structure}/10")
        time.sleep(3)

        print("   Getting AI quality score...")
        ai_score = self.ai_quality_score(topic, research)
        print(f"   AI Quality: {ai_score}/10")
        time.sleep(5)

        all_scores = [
            completeness,
            length_score,
            structure,
            ai_score
        ]
        overall = sum(all_scores) / len(all_scores)

        if overall >= 8:
            grade = "A - Excellent! "
        elif overall >= 6:
            grade = "B - Good "
        elif overall >= 4:
            grade = "C - Average "
        else:
            grade = "D - Needs Work "

        return {
            "completeness_score": completeness,
            "length_score": length_score,
            "structure_score": structure,
            "ai_quality_score": ai_score,
            "overall_score": round(overall, 1),
            "grade": grade,
            "word_count": len(research.split())
        }

evaluator = EvaluationSystem()

evaluation = evaluator.full_evaluation(
    topic=research_data["topic"],
    research=research_data.get("research", ""),
    summary=research_data.get("summary", "")
)

print("\n EVALUATION RESULTS:")
print(f"   Completeness:  {evaluation['completeness_score']}/10")
print(f"   Length:        {evaluation['length_score']}/10")
print(f"   Structure:     {evaluation['structure_score']}/10")
print(f"   AI Quality:    {evaluation['ai_quality_score']}/10")
print(f"   Overall:       {evaluation['overall_score']}/10")
print(f"   Grade:         {evaluation['grade']}")
print(f"   Word Count:    {evaluation['word_count']}")

# ERROR HANDLING DEMO
print("\n\n  ERROR HANDLING DEMO")
print("-" * 40)

def safe_agent_call(
    topic: str,
    max_retries: int = 3
) -> str:

    retry_count = 0

    while retry_count < max_retries:

        try:
            prompt = PromptTemplate(
                input_variables=["topic"],
                template="""Briefly explain: '{topic}'
                In 3 bullet points only."""
            )
            chain = prompt | llm | parser
            result = chain.invoke({"topic": topic})
            print(f"    Success on attempt {retry_count + 1}")
            return result

        except Exception as e:
            retry_count += 1
            error_type = type(e).__name__

            print(f"     Attempt {retry_count} failed")
            print(f"   Error: {error_type}")

            if "429" in str(e):
                print(f"   Rate limit! Waiting 60 sec...")
                time.sleep(60)

            elif "503" in str(e):
                print(f"   Server busy! Waiting 10 sec...")
                time.sleep(10)

            else:
                print(f"   Waiting 5 sec...")
                time.sleep(5)

    return f"Could not research '{topic}'. Please try later."

print("Testing error handling with valid topic:")
test_result = safe_agent_call("What is LangChain?")
print(f"Result: {test_result[:150]}...")

# FINAL BRIDGE COURSE REPORT
print("\n\n BRIDGE COURSE SUBMISSION REPORT")
print("=" * 55)

bridge_report = {
    "student": "Janak Gajjar",
    "program": "MCA Semester 3",
    "subject": "Agentic AI Bridge Course",
    "project": "Research Assistant Agent",
    "date": datetime.datetime.now().isoformat(),

    "requirements_met": {

        "react_loop": {
            "status": " Implemented",
            "where": "run_react_agent() in Part 1",
            "description": "Thought → Action → Observe → Repeat"
        },

        "tools_used": {
            "status": " 3 Tools",
            "tools": [
                "research_tool = Gathers information",
                "summary_tool = Creates summary",
                "question_generator_tool = Makes quiz"
            ]
        },

        "memory": {
            "status": "Short-term Memory",
            "type": "AgentMemory class",
            "storage": "In-memory list + JSON file"
        },

        "error_handling": {
            "status": " Implemented",
            "method": "try/except + 3 retry attempts",
            "covers": "Rate limit, Server error, General"
        },

        "prompt_engineering": {
            "status": " Applied",
            "techniques": [
                "Structured output format",
                "Role-based prompts",
                "Context injection",
                "Output constraints"
            ]
        },

        "evaluation_metrics": {
            "status": " 4 Metrics",
            "metrics": [
                "Completeness score",
                "Length score",
                "Structure score",
                "AI quality score"
            ]
        }
    },

    "evaluation": evaluation,

    "tech_stack": {
        "framework": "LangChain",
        "llm": "Google Gemini 2.5 Flash Lite",
        "pattern": "ReAct",
        "memory": "Custom AgentMemory",
        "deployment": "Local + Hugging Face"
    }
}

# Print report
print(f"\nStudent: {bridge_report['student']}")
print(f"Project: {bridge_report['project']}")
print(f"\nRequirements Check:")

for req, details in bridge_report["requirements_met"].items():
    print(f"\n   {details['status']} {req.upper()}")

    if "where" in details:
        print(f"      Where: {details['where']}")
    if "tools" in details:
        for tool in details["tools"]:
            print(f"      → {tool}")
    if "techniques" in details:
        for tech in details["techniques"]:
            print(f"      → {tech}")
    if "metrics" in details:
        for metric in details["metrics"]:
            print(f"      → {metric}")

# Final score
print(f"\n{'='*55}")
print(f" FINAL EVALUATION:")
print(f"   Score: {evaluation['overall_score']}/10")
print(f"   Grade: {evaluation['grade']}")

# Save complete report
with open("bridge_course_report.json", "w") as f:
    json.dump(bridge_report, f, indent=2)
