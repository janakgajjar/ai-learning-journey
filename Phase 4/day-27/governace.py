# ============================================
# Program: Governance + Observability 
# Topic: AI Compliance + Monitoring System
# Phase: 4 | Day: 27
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

print("-" * 30)
print(" Governance + Obsevability")
print("-" * 30)

##Part 1: AI Governance Framework
print("\n Part 1: AI Governance Framework")
print("-" * 30)

class AIGovernanceChecker:
    EU_AI_ACT_RISKS = {
        "unacceptable": [
            #banned AI 
            "social scoring",
            "subliminal manipulation",
            "ral-time bimetric",
        ],
        "high_risk": [
            #Needs strict oversight
            "medical diagnosis",
            "credit scoring",
            "hiring sdecisions",
            "education grading",
        ],
        "limited_risk": [
            #needs transparency disclosure
            "chatbot",
            "deepfake",
            "emotion recogntion",
        ],
        "minimal_risk": [
            #freely usable
            "spam filter",
            "recommendation",
            "game ai",
        ]
    }

    def check_compliance(self, use_case: str):
        use_lower = use_case.lower()

        for risk_level, keywords in self.EU_AI_ACT_RISKS.items():
            for keyword in keywords:
                if keyword in use_lower:
                    if risk_level == "unacceptable":
                        return {
                            "use_case": use_case,
                            "risk_level": "UNACCEPTABLE",
                            "eu_act": "BANNED",
                            "action": "Cannot deploy this AI system",
                            "requires":"Complete ban"
                        }
                    elif risk_level == "high_risk":
                        return {
                            "use_case":  use_case,
                            "risk_level": " HIGH RISK",
                            "eu_act": "Heavily Regulated",
                            "action": "Must register + audit",
                            "requires": "Conformity assessment + CE mark"
                        }
                    elif risk_level == "limited_risk":
                        return {
                            "use_case": use_case,
                            "risk_level": " LIMITED RISK",
                            "eu_act": "Transparency Required",
                            "action": "Must disclose AI use",
                            "requires": "User notification"
                        }
                    else:
                        return {
                            "use_case": use_case,
                            "risk_level": " MINIMAL RISK",
                            "eu_act": "Freely usable",
                            "action": "No specific requirements",
                            "requires": "Good practices only"
                        }
                return {
                    "use_case": use_case,
                    "risk_level": "MINIMAL RISK",
                    "eu_act": "Freely usable",
                    "action": "proceed with good practices",
                    "reuires": "Standard documentation"    
                }

checker = AIGovernanceChecker()

ai_use_cases = [
    "PDF chatbot for students",
    "Medical diagnosis AI system",
    "Hiring decisions AI tool",
    "Customer service chatbot",
    "Social scoring citizens",
    "Spam filter for emails",
]

print("\n EU AI Act Compliance Check:")

compliance_results = []

for use_case in ai_use_cases:
    result = checker.check_compliance(use_case)

    print(f"\n Use Case: '{use_case}'")
    print(f" Risk Level: {result['risk_level']}")
    print(f" EU Act : {result['eu_act']}")
    print(f" Action: {result['action']}")

    compliance_results.append(result)


## Part 2: NIST AI Risk Management
print("\n \n Part 2 : NIST AI Risk Management")
print("-" * 30)

print("""
 NIST AI RMF — 4 Core Functions:

1. GOVERN 
   → Policies + procedures establish
   → Leadership accountability
   → Culture of responsible AI
   
2. MAP   
   → AI context understand
   → Risk categories identify
   → Stakeholders map
   
3. MEASURE 
   → Risk quantify
   → Performance metrics
   → Bias testing
   
4. MANAGE 
   → Risk prioritize + treat
   → Respond to incidents
   → Continuous improvement
""")

nist_checklist = {
    "GOVERN": {
        "G1": "AI policy document exists?",
        "G2": "Leadership approves AI use?",
        "G3": "Staff trained on AI risks?",
        "G4": "Ethics review process exists?"
    },
    "MAP": {
        "M1": "Use case documented?",
        "M2": "Data sources identified?",
        "M3": "Stakeholders listed?",
        "M4": "Failure scenarios mapped?"
    },
    "MEASURE": {
        "ME1": "Accuracy metrics defined?",
        "ME2": "Bias testing done?",
        "ME3": "Performance monitored?",
        "ME4": "User feedback collected?"
    },
    "MANAGE": {
        "MG1": "Incident response plan?",
        "MG2": "Model updates process?",
        "MG3": "Rollback procedure?",
        "MG4": "Regular audits scheduled?"
    }
}

print("\n NIST Assessment: PDF RAG Chatbot")
our_answers = {
    "G1": True,
    "G2": True,
    "G3": True,
    "G4": False,
    "M1": True,
    "M2": True,
    "M3": True,
    "M4": False,
    "ME1": True,
    "ME2": False,
    "ME3": True,
    "ME4": False,
    "MG1": False,
    "MG2": True,
    "MG3": True,
    "MG4": False
}

passed = sum(1 for v in our_answers.values() if v)
total = len(our_answers)
nist_score = (passed / total) * 100

print(f"\n Passed: {passed}/{total}")
print(f" NIST Score: {nist_score:.0f}%")

for function, items in nist_checklist.items():
    func_passed = sum(
        1 for k in items.keys()
        if our_answers.get(k, False)
    )
    print(f" {function}: {func_passed}/{len(items)}")

## Part 3: Observability system
print("\n\n Part 3: AI Observability System")
print("-" * 30)

class AIObservabilityLogger:
    def __init__(self):
        #logs list
        self.logs = []

        #metrics dict
        self.metrics = {
            "total_calls": 0,
            "success_calls": 0,
            "error_calls": 0,
            "total_latency": 0,
            "total_tokens": 0,
        }
    
    def log_call(
            self,
            question: str,
            answer: str = "",
            latency: float = 0,
            status: str = "success",
            error_msg: str = None
    ):
        #log entry created isoformat
        log_entry = {
            "id": len(self.logs) + 1,
            "timestamp": datetime.datetime.now().isoformat(),
            "question": question[:100],
            "answer_length": len(answer),
            "latnecy_sec": latency,
            "status": status,
            "error": error_msg,
            "estimated_tokens": int(
                (len(question) + len(answer)) / 4
            )
        }

        self.logs.append(log_entry)
        self.metrics["total_calls"] += 1

        if status == "success":
            self.metrics["success_calls"] += 1
        else:
            self.metrics["error_calls"] +=1

        self.metrics["total_latency"] += latency
        self.metrics["total_tokens"] += log_entry["estimated_tokens"]

    def get_report(self):

        total = self.metrics["total_calls"]
        if total == 0:
            return {"error": "No calls logged"}
    
        avg_latency = self.metrics["total_latency"] / total

        success_rate = (
            self.metrics["success_calls"] / total * 100
        )

        return {
            "total_calls": total,
            "success_rate": f"{success_rate:.1f}%",
            "avg_latency": f"{avg_latency:.2f}s",
            "total_tokens": self.metrics["total_tokens"],
            "error_count": self.metrics["error_calls"]
        }
    
logger = AIObservabilityLogger()

def observed_llm_call(question: str):

    print(f"\n TRACE: Starting call")
    print(f" Input: '{question[:50]}'")

    start = datetime.datetime.now()
    
    try:
        prompt = PromptTemplate(
            input_variables=["q"],
            template="Answer briefly for MCA students: {q}"
        )
        chain = prompt | llm | parser

        answer = chain.invoke({"q": question})
        end = datetime.datetime.now()
        latency = (end - start).total_seconds()

        logger.log_call(
            question=question,
            answer=answer,
            latency=latency,
            status="success"
        )
        print(f" SUCCESS | Latency: {latency:.2f}s")
        return answer
    
    except Exception as e:
        end = datetime.datetime.now()
        latency = (end - start).total_seconds()

        logger.log_call(
            question=question,
            latency=latency,
            status="error",
            error_msg=str(e)
        )
        print(f" ERROR: {str(e)[:50]}")
        return None
    
observed_questions = [
    "What is AI Governance?",
    "Explain NIST AI RMF briefly"
]

for q in observed_questions:
    result = observed_llm_call(q)
    if result:
        print(f" Answer: {result[:100]}...")
    print(" Waiting 15 sec...")
    time.sleep(15)

## Final Report
print("\n\n Final Obervability Report")
print("-" * 30)

report = logger.get_report()


print(f"Total API Calls:  {report['total_calls']}")
print(f"Success Rate:     {report['success_rate']}")
print(f"Avg Latency:      {report['avg_latency']}")
print(f"Tokens Used:      {report['total_tokens']}")
print(f"Errors:           {report['error_count']}")

# All data save
final_report = {
    "compliance": compliance_results,
    "nist_score": f"{nist_score:.0f}%",
    "observability": report,
    "logs": logger.logs
}

with open("governance_report.json", "w") as f:
    json.dump(final_report, f, indent=2)