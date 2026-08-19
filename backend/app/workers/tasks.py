"""
Celery worker entry point for AuditCompliance.cloud

Run with: celery -A app.workers.tasks worker --loglevel=info
"""

import asyncio
import os

from celery import Celery

from ..core.classifier import get_classifier

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

celery_app = Celery(
    "auditcompliance",
    broker=REDIS_URL,
    backend=REDIS_URL,
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
)


@celery_app.task(name="scan_payload")
def scan_payload(content: str, api_key: str | None = None) -> dict:
    """
    Classify a payload for compliance violations.
    Zero-retention: content is discarded by the classifier after use.
    """
    classifier = get_classifier(api_key)
    result = asyncio.run(classifier.classify(content))
    return result.model_dump()
