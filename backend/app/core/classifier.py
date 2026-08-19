"""
Core AI Classification Service
Implements zero-retention, structured output classification
"""

import hashlib
import time
import logging
from typing import Dict, Any, Optional
from datetime import datetime

# Try to import OpenAI, handle if not available
try:
    from openai import AsyncOpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False
    logging.warning("OpenAI package not available. Using mock classification for development.")

from ..models import (
    AIComplianceAuditResult, 
    ViolationType, 
    Severity,
    TelemetryPayload
)
from .prompts import (
    get_classification_prompt,
    MODEL_CONFIGS,
    FALLBACK_RULES,
    PROMPT_TEST_CASES
)

logger = logging.getLogger(__name__)


class ClassificationService:
    """
    Zero-Trust Classification Service
    - Processes data in memory only
    - Outputs structured JSON only
    - Implements fallback rules for safety
    """
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key
        self.client = None
        self.model_name = "gpt-4o"
        
        if OPENAI_AVAILABLE and api_key:
            self.client = AsyncOpenAI(api_key=api_key)
            # Check if we should use a different model
            self.model_name = MODEL_CONFIGS.get(
                api_key.split('-')[0] if api_key else "gpt",
                MODEL_CONFIGS["gpt-4o"]
            )["model_name"]
    
    async def classify(self, content: str) -> AIComplianceAuditResult:
        """
        Main classification entry point.
        Implements zero-retention: content is processed then discarded.
        """
        start_time = time.time()
        content_hash = hashlib.sha256(content.encode()).hexdigest()
        
        try:
            # Attempt LLM classification
            result = await self._llm_classify(content)
        except Exception as e:
            logger.warning(f"LLM classification failed: {e}. Falling back to rules.")
            result = await self._fallback_classify(content)
        
        # Add metadata
        latency = (time.time() - start_time) * 1000
        result.confidence_score = getattr(result, 'confidence_score', 0.95)
        result.model_version = self.model_name if self.client else "fallback-rules"
        
        # DISCARD original content - never store it
        del content
        
        return result
    
    async def _llm_classify(self, content: str) -> AIComplianceAuditResult:
        """
        Use LLM for classification with structured output
        """
        if not self.client:
            raise RuntimeError("LLM client not initialized")
        
        prompt = get_classification_prompt(
            content=content,
            schema_description=self._get_json_schema()
        )
        
        response = await self.client.beta.chat.completions.parse(
            model=self.model_name,
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": content}
            ],
            response_format=AIComplianceAuditResult,
            temperature=0.0,  # Zero temperature for determinism
            max_tokens=500
        )
        
        return response.choices[0].message.parsed
    
    async def _fallback_classify(self, content: str) -> AIComplianceAuditResult:
        """
        Deterministic fallback using regex rules
        Ensures safety when LLM is unavailable
        """
        import re
        
        # Credit Card pattern
        cc_pattern = r'\b\d{4}[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4}\b'
        # API Key pattern
        api_pattern = r'(?:api_key|apikey|api-key|key|token|secret)=(?:[' \
                       r'a-zA-Z0-9_]{20,}|ghp_[a-zA-Z0-9]{36})'
        # Email pattern  
        email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
        
        content_lower = content.lower()
        
        # Check for API keys
        if re.search(api_pattern, content, re.IGNORECASE):
            # Extract snippet
            match = re.search(api_pattern, content, re.IGNORECASE)
            return AIComplianceAuditResult(
                violation_found=True,
                violation_type=ViolationType.CREDENTIAL_LEAK,
                severity_level=Severity.CRITICAL,
                evidence_snippet=match.group(0)[:100] if match else None,
                implicated_framework_clauses=["SOC2 CC6.3", "ISO 27001 A.9.4"],
                recommended_action="Rotate exposed credentials immediately. Implement secret scanning in CI/CD."
            )
        
        # Check for credit cards
        if re.search(cc_pattern, content):
            match = re.search(cc_pattern, content)
            return AIComplianceAuditResult(
                violation_found=True,
                violation_type=ViolationType.PII_LEAK,
                severity_level=Severity.CRITICAL,
                evidence_snippet=match.group(0)[:50] if match else None,
                implicated_framework_clauses=["GDPR Article 32", "PCI DSS 3.4"],
                recommended_action="Immediately redact and report potential data breach."
            )
        
        # Check for emails with potential PII context
        emails = re.findall(email_pattern, content)
        if emails and ('passport' in content_lower or 'ssn' in content_lower or 
                       'driver' in content_lower or 'medical' in content_lower):
            return AIComplianceAuditResult(
                violation_found=True,
                violation_type=ViolationType.PII_LEAK,
                severity_level=Severity.HIGH,
                evidence_snippet=f"Personal information: {', '.join(emails[:3])}",
                implicated_framework_clauses=["GDPR Article 32", "HIPAA Security Rule"],
                recommended_action="Review data handling policies for personal information."
            )
        
        # Check for shadow AI
        ai_tools = ['chatgpt', 'claude', 'gemini', 'copilot', ' Bard', 'openai']
        has_ai = any(tool.lower() in content_lower for tool in ai_tools)
        sensitive_keywords = ['password', 'secret', 'api', 'key', 'token', 'internal', 'confidential']
        has_sensitive = any(kw in content_lower for kw in sensitive_keywords)
        
        if has_ai and has_sensitive:
            return AIComplianceAuditResult(
                violation_found=True,
                violation_type=ViolationType.SHADOW_AI,
                severity_level=Severity.HIGH,
                evidence_snippet="Potential unauthorized AI usage with sensitive data",
                implicated_framework_clauses=["ISO 42001", "NIST AI RMF"],
                recommended_action="Implement approval workflow for AI tool usage."
            )
        
        # No violations found
        return AIComplianceAuditResult(
            violation_found=False,
            violation_type=ViolationType.NONE,
            severity_level=Severity.NONE,
            evidence_snippet=None,
            implicated_framework_clauses=[],
            recommended_action="No compliance violations detected"
        )
    
    def _get_json_schema(self) -> str:
        """Get the JSON schema for output validation"""
        return """
{
    "violation_found": true or false,
    "violation_type": "PII_LEAK" | "CREDENTIAL_LEAK" | "SHADOW_AI" | "PROPRIETARY_IP" | "SENSITIVE_DATA" | "NONE",
    "severity_level": "CRITICAL" | "HIGH" | "MEDIUM" | "LOW" | "NONE",
    "evidence_snippet": "exact text from content" or null,
    "implicated_framework_clauses": ["GDPR Article 32", "SOC2 CC6.1"],
    "recommended_action": "single actionable sentence"
}
"""


# Global service instance
_service_instance: Optional[ClassificationService] = None


def get_classifier(api_key: Optional[str] = None) -> ClassificationService:
    """Get or create the classifier service instance"""
    global _service_instance
    if _service_instance is None and api_key:
        _service_instance = ClassificationService(api_key)
    return _service_instance or ClassificationService(api_key)