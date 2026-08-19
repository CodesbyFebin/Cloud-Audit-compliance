"""Core services module"""

from .classifier import ClassificationService, get_classifier
from .prompts import (
    PROMPT_TEMPLATE,
    get_classification_prompt,
    PII_DETECTION_PROMPT,
    CREDENTIAL_DETECTION_PROMPT,
    MODEL_CONFIGS,
    PROMPT_TEST_CASES
)

__all__ = [
    "ClassificationService",
    "get_classifier",
    "PROMPT_TEMPLATE",
    "get_classification_prompt",
    "PII_DETECTION_PROMPT",
    "CREDENTIAL_DETECTION_PROMPT",
    "MODEL_CONFIGS",
    "PROMPT_TEST_CASES"
]