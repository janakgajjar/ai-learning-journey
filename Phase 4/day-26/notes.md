# Day 26 — AI Safety + Prompt Injection

## Attack Types
| Attack | How | Defense |
|--------|-----|---------|
| Direct Override | "Ignore instructions" | Strong system prompt |
| Jailbreaking | "Act as DAN" | Injection detection |
| Role Play | "Pretend you are..." | Pattern matching |
| Indirect | Hidden in docs | Output filtering |

## Guardrail Layers
1. Input Validation → Before LLM call
2. System Prompt → During LLM call
3. Output Filtering → After LLM call

## PII Types
- Email addresses
- Phone numbers
- Credit card numbers
- Aadhaar numbers
- Passwords

## OWASP LLM Top 10
1. Prompt Injection ← Most Important!
2. Insecure Output Handling
3. Training Data Poisoning
4. Model Denial of Service
5. Supply Chain Vulnerabilities
6. Sensitive Info Disclosure
7. Insecure Plugin Design
8. Excessive Agency
9. Overreliance
10. Model Theft

## Security Checklist
✅ Strong system prompt
✅ Input validation
✅ PII detection
✅ Output filtering
✅ Rate limiting
✅ Logging + monitoring

## Key Insight
Security = Multiple layers!
No single protection is enough
Defense in depth = Best practice!