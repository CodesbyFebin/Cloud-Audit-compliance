"""
Pydantic models for Zero-Trust AI Compliance Platform
These models enforce strict schemas to prevent LLM hallucinations
"""

from pydantic import BaseModel, Field
from typing import Literal, Optional, List
from datetime import datetime
from enum import Enum
import hashlib


class ViolationType(str, Enum):
    """Strict violation types - no hallucination possible"""
    PII_LEAK = "PII_LEAK"
    CREDENTIAL_LEAK = "CREDENTIAL_LEAK"
    SHADOW_AI = "SHADOW_AI"
    PROPRIETARY_IP = "PROPRIETARY_IP"
    SENSITIVE_DATA = "SENSITIVE_DATA"
    NONE = "NONE"


class Severity(str, Enum):
    """Predefined severity levels"""
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"
    NONE = "NONE"


class Framework(str, Enum):
    """Compliance frameworks"""
    SOC2 = "SOC2"
    GDPR = "GDPR"
    HIPAA = "HIPAA"
    ISO27001 = "ISO27001"
    ISO42001 = "ISO42001"
    NIST_AI_RMF = "NIST_AI_RMF"
    EU_AI_ACT = "EU_AI_ACT"


class AIComplianceAuditResult(BaseModel):
    """
    STRICT schema for AI compliance classification.
    The LLM MUST output exactly this format - no deviations.
    This prevents hallucinations by constraining output.
    """
    violation_found: bool = Field(
        description="True if a compliance or data leak violation is detected. MUST be False if no violation exists."
    )
    violation_type: Literal['PII_LEAK', 'CREDENTIAL_LEAK', 'SHADOW_AI', 'PROPRIETARY_IP', 'SENSITIVE_DATA', 'NONE'] = Field(
        ...
    )
    severity_level: Literal['CRITICAL', 'HIGH', 'MEDIUM', 'LOW', 'NONE'] = Field(
        ...
    )
    evidence_snippet: Optional[str] = Field(
        default=None,
        description="Exact substring that triggered the violation. MUST be null if violation_found is False."
    )
    implicated_framework_clauses: List[str] = Field(
        default_factory=list,
        description="E.g., ['GDPR Article 32', 'SOC2 CC6.1', 'HIPAA 45 CFR 164.312']"
    )
    recommended_action: str = Field(
        description="One-sentence actionable remediation step for the CISO or organization."
    )
    
    # Additional metadata for audit trail
    confidence_score: Optional[float] = Field(
        default=None,
        ge=0.0,
        le=1.0,
        description="Confidence score of the classification (0.0 to 1.0)"
    )
    model_version: Optional[str] = Field(
        default=None,
        description="Which AI model was used for classification"
    )
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "violation_found": True,
                "violation_type": "PII_LEAK",
                "severity_level": "CRITICAL",
                "evidence_snippet": "Passport: 123456789 | John Doe | DOB: 01/01/1990",
                "implicated_framework_clauses": ["GDPR Article 32", "SOC2 CC6.1"],
                "recommended_action": "Immediately redact and rotate any exposed passport data",
                "confidence_score": 0.98,
                "model_version": "gpt-4o"
            }
        }
    }


class TelemetryPayload(BaseModel):
    """Incoming data payload from integrations"""
    organization_id: str = Field(..., description="UUID of the multi-tenant organization")
    integration_name: str = Field(..., description="e.g., 'slack', 'github', 'google_workspace'")
    employee_identifier: str = Field(..., description="Hashed identifier of the user/email")
    raw_text: str = Field(..., description="The outbound text/code block being scanned")
    source_url: Optional[str] = Field(None, description="Direct URL to message or artifact")
    captured_at: datetime = Field(default_factory=datetime.utcnow)
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "organization_id": "550e8400-e29b-41d4-a716-446655440000",
                "integration_name": "slack",
                "employee_identifier": "hashed_email@example.com",
                "raw_text": "Here's the API key: sk-proj-123456789abcdef",
                "source_url": "https://slack.com/messages/C12345",
                "captured_at": "2024-01-15T10:30:00Z"
            }
        }
    }


class ScanResult(BaseModel):
    """Result from AI classification scan"""
    trace_id: str = Field(..., description="Unique identifier for the scan")
    violation: Optional[AIComplianceAuditResult] = Field(None, description="Classification result if violation found")
    processed_at: datetime = Field(default_factory=datetime.utcnow)
    latency_ms: float = Field(..., description="Processing time in milliseconds")
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "trace_id": "trace-a1b2c3d4e5f6",
                "violation": {
                    "violation_found": True,
                    "violation_type": "CREDENTIAL_LEAK",
                    "severity_level": "CRITICAL",
                    "evidence_snippet": "api_key=sk-proj-123456789abcdef",
                    "implicated_framework_clauses": ["SOC2 CC6.3", "GDPR Article 32"],
                    "recommended_action": "Rotate the exposed API key immediately and implement secret scanning"
                },
                "processed_at": "2024-01-15T10:30:01.500Z",
                "latency_ms": 145.3
            }
        }
    }


class IngestResponse(BaseModel):
    """Response from ingestion endpoint"""
    status: str = Field(..., description="Status of the ingestion")
    message: str = Field(..., description="Human-readable message")
    trace_id: str = Field(..., description="Unique trace ID for tracking")
    scanned: bool = Field(..., description="Whether the payload was scanned")
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "status": "queued",
                "message": "Zero-trust memory buffer loaded. Scan initiated.",
                "trace_id": "trace-a1b2c3d4e5f6",
                "scanned": True
            }
        }
    }