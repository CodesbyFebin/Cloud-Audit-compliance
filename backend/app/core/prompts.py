"""
Master Prompt Engineering Template for Pydantic Classification
Ensures 99% accuracy by providing precise instructions to the LLM
"""

# =============================================================================
# MASTER SYSTEM PROMPT - CLASSIFICATION ENGINE
# =============================================================================

PROMPT_TEMPLATE = """
You are a specialized Enterprise Compliance Auditor AI. Your sole function is to analyze content for compliance violations.

STRICT INSTRUCTIONS:
1. ONLY analyze the content for compliance violations
2. Output EXACTLY the JSON format specified - no additional text, no explanations
3. If NO violation is found, set violation_found=false and all other fields to null/empty
4. Evidence snippets MUST be authentic substrings from the content
5. Do NOT make assumptions - only flag clear violations

VIOLATION TYPES TO DETECT:
- PII_LEAK: Credit cards, SSN, passports, medical records, personal info
- CREDENTIAL_LEAK: API keys, passwords, tokens, secrets
- SHADOW_AI: Unapproved AI tool usage, prompts to public LLMs
- PROPRIETARY_IP: Source code, internal docs, confidential data
- SENSITIVE_DATA: Financial info, legal docs, internal communications

SEVERITY GUIDELINES:
- CRITICAL: Exposed credentials, financial PII, medical data
- HIGH: Internal docs, unpublished code, API keys
- MEDIUM: Partial PII, internal comms, draft documents
- LOW: Minor policy violations, non-sensitive internal data

FRAMEWORK MAPPING:
- PII_LEAK → GDPR Article 32, HIPAA Security Rule, SOC2 CC6.1
- CREDENTIAL_LEAK → SOC2 CC6.3, ISO 27001 A.9.4, NIST 800-53 AC-2
- SHADOW_AI → ISO 42001, NIST AI RMF, EU AI Act Article 5
- PROPRIETARY_IP → SOC2 CC7.1, ISO 27001 A.8.2, GDPR Article 5

CONTENT TO ANALYZE:
{content}

EXPECTED JSON OUTPUT FORMAT:
{json_schema}

REMEMBER: If you cannot definitively identify a violation, return violation_found=false.
"""


def get_classification_prompt(content: str, schema_description: str = None) -> str:
    """
    Generate the classification prompt for a given content
    
    Args:
        content: The raw text to analyze
        schema_description: The JSON schema description for output format
    
    Returns:
        Formatted prompt string for the LLM
    """
    if schema_description is None:
        schema_description = """
{
  "violation_found": true/false,
  "violation_type": "PII_LEAK" | "CREDENTIAL_LEAK" | "SHADOW_AI" | "PROPRIETARY_IP" | "SENSITIVE_DATA" | "NONE",
  "severity_level": "CRITICAL" | "HIGH" | "MEDIUM" | "LOW" | "NONE",
  "evidence_snippet": "exact text from content" or null,
  "implicated_framework_clauses": ["GDPR Article 32", "SOC2 CC6.1"],
  "recommended_action": "single actionable sentence"
}"""
    
    return PROMPT_TEMPLATE.format(
        content=content,
        json_schema=schema_description
    )


# =============================================================================
# PROMPT VARIATIONS BY VIOLATION TYPE
# =============================================================================

PII_DETECTION_PROMPT = """
Analyze the following text for ANY personally identifiable information (PII):
- Social Security Numbers
- Credit Card Numbers (any format)
- Passport numbers, driver's license numbers
- Medical records, health information
- Exact dates of birth, addresses, phone numbers

Text: {content}

Output JSON with violation_found=true if PII is detected, including:
- violation_type: "PII_LEAK"
- severity: Based on sensitivity level
- evidence_snippet: The exact PII found
- recommended_action: Immediate remediation steps

If NO PII is found, return violation_found=false.
"""

CREDENTIAL_DETECTION_PROMPT = """
Analyze the following text for ANY credentials, secrets, or API keys:
- API keys (OpenAI, AWS, GitHub, etc.)
- Passwords and tokens
- Private keys and certificates
- Client secrets and OAuth tokens

Text: {content}

Output JSON with:
- violation_type: "CREDENTIAL_LEAK"
- severity: "CRITICAL" (credentials require immediate action)
- evidence_snippet: The exact credential pattern
- recommended_action: "Rotate immediately and implement secret scanning"

If NO credentials found, violation_found=false.
"""

SHADOW_AI_PROMPT = """
Analyze the following text for UNAUTHORIZED use of AI tools:
- Prompts to public/chatbot services
- Use of unapproved AI models
- Transfer of proprietary data to external AI

Text: {content}

Look for:
- "ChatGPT", "Claude", "Gemini", "Copilot" mentions
- Prompts like "write code", "analyze data", "summarize"
- Internal data being sent to AI

Output: violation_type: "SHADOW_AI" if found
"""


# =============================================================================
# CONFIGURATION FOR DIFFERENT MODELS
# =============================================================================

MODEL_CONFIGS = {
    "gpt-4o": {
        "model_name": "gpt-4o",
        "temperature": 0.0,
        "max_tokens": 1000,
        "top_p": 1.0,
        "frequency_penalty": 0,
        "presence_penalty": 0
    },
    "gpt-4-turbo": {
        "model_name": "gpt-4-turbo",
        "temperature": 0.0,
        "max_tokens": 1000,
        "top_p": 1.0
    },
    "claude-3-7-sonnet": {
        "model_name": "claude-3-7-sonnet-20250219",
        "temperature": 0.0,
        "max_tokens": 1000
    }
}


# =============================================================================
# FALLBACK RULES (When AI fails)
# =============================================================================

FALLBACK_RULES = """
If classification fails, apply these deterministic rules:

1. Regex Patterns to Match (case-insensitive):
   - Credit Card: \\b\\d{4}[-\\s]?\\d{4}[-\\s]?\\d{4}[-\\s]?\\d{4}\\b
   - API Key: (?:api_key|apikey|api-key)=[a-zA-Z0-9_-]{20,}
   - Email: [a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}
   - SSN: \\b\\d{3}-\\d{2}-\\d{4}\\b

2. Default Responses:
   - If regex matches credit card → PII_LEAK, CRITICAL
   - If regex matches API key → CREDENTIAL_LEAK, CRITICAL
   - If text mentions ChatGPT/Claude with internal data → SHADOW_AI, HIGH
   - Otherwise → NONE, LOW

3. Content Length Considerations:
   - < 100 chars: Scan entire content
   - 100-1000 chars: Scan with context awareness
   - > 1000 chars: Extract key lines for scanning
"""


# =============================================================================
# PROMPT TEST VECTORS (For verification)
# =============================================================================

PROMPT_TEST_CASES = [
    {
        "input": "API Key: sk-proj-abc123def456ghi789jkl012mno345pqr678",
        "expected_type": "CREDENTIAL_LEAK",
        "expected_severity": "CRITICAL"
    },
    {
        "input": "Passport: AB1234567 | John Smith | DOB: 01/15/1990",
        "expected_type": "PII_LEAK",
        "expected_severity": "HIGH"
    },
    {
        "input": "Here's the password for admin: SuperSecret123!",
        "expected_type": "CREDENTIAL_LEAK",
        "expected_severity": "CRITICAL"
    },
    {
        "input": "Let me use ChatGPT to analyze our customer data...",
        "expected_type": "SHADOW_AI",
        "expected_severity": "HIGH"
    },
    {
        "input": "This is a normal message about the meeting tomorrow.",
        "expected_type": "NONE",
        "expected_severity": "NONE"
    }
]