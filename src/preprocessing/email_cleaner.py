"""
Email preprocessing utilities.

This module is responsible for:
- Cleaning and normalizing raw email text
- Masking sensitive identifiers (policy numbers, amounts)
- Constructing the final input string fed to the NLP model

IMPORTANT:
- Preprocessing must be deterministic
- The same logic must be used for both training and inference
"""

import re
from typing import Optional


# -------------------------
# Regex patterns
# -------------------------

# Conservative pattern for policy numbers / reference IDs
POLICY_ID_PATTERN = re.compile(r"\b[A-Z0-9]{8,}\b")

# Currency / amount pattern (₹, $, €, plain numbers)
AMOUNT_PATTERN = re.compile(
    r"\b(?:₹|\$|€)?\d+(?:,\d+)*(?:\.\d+)?\b"
)

# Common email signature separators
SIGNATURE_SEPARATORS = [
    "\nregards",
    "\nbest regards",
    "\nthanks",
    "\nthank you",
    "\nsincerely",
    "\n--",
]


# -------------------------
# Core cleaning functions
# -------------------------

def strip_signature(text: str) -> str:
    """
    Remove common email signatures.

    This is a heuristic and intentionally conservative.
    """
    lower_text = text.lower()
    for sep in SIGNATURE_SEPARATORS:
        idx = lower_text.find(sep)
        if idx != -1:
            return text[:idx]
    return text


def mask_sensitive_tokens(text: str) -> str:
    """
    Mask sensitive identifiers to reduce overfitting
    and prevent leakage of PII into the model.
    """
    text = POLICY_ID_PATTERN.sub("[POLICY_ID]", text)
    text = AMOUNT_PATTERN.sub("[AMOUNT]", text)
    return text


def normalize_whitespace(text: str) -> str:
    """
    Normalize whitespace and line breaks.
    """
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def clean_text(text: Optional[str]) -> str:
    """
    Full cleaning pipeline for a single text field.
    """
    if not text:
        return ""

    text = strip_signature(text)
    text = mask_sensitive_tokens(text)
    text = normalize_whitespace(text)
    return text.lower()


# -------------------------
# Model input construction
# -------------------------

def build_model_input(
    subject: Optional[str],
    body: Optional[str],
    sender_domain: Optional[str],
    customer_type: Optional[str],
) -> str:
    """
    Construct the final input string for the classifier.

    The format is intentionally verbose and stable.
    """
    subject = clean_text(subject)
    body = clean_text(body)

    sender_domain = sender_domain or "unknown"
    customer_type = customer_type or "unknown"

    return (
        f"Subject: {subject}\n"
        f"Sender: {sender_domain}\n"
        f"Customer Type: {customer_type}\n\n"
        f"Email Body:\n{body}"
    )