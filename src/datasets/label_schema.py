"""
Label schema for insurance email classification.

This file defines:
1. The complete set of allowed email categories
2. Business rules governing label assignment
3. Priority logic for ambiguous cases

IMPORTANT:
- Exactly ONE label must be assigned per email.
- If ambiguity cannot be resolved deterministically, the email
  MUST be routed for human review.
"""

from enum import Enum, unique


@unique
class EmailLabel(Enum):
    """
    Canonical label set for incoming insurance emails.

    The numeric values are stable and must NEVER be reordered,
    as they are used in model training and persisted predictions.
    """

    POLICY_PURCHASE = 0
    CLAIMS = 1
    ACCOUNTS_BILLING = 2
    POLICY_INFORMATION_MARKETING = 3


# -------------------------
# Label Assignment Rules
# -------------------------

LABEL_PRIORITY_RULES = """
Priority rules for labeling emails:

1. CLAIMS has the highest priority.
   If the email mentions accidents, hospitalisation, treatment,
   reimbursement, damage, or claim numbers, it MUST be labeled CLAIMS,
   regardless of any other intent.

2. POLICY_PURCHASE applies to:
   - New policy inquiries
   - Quote requests
   - Enrollment or application intent

3. ACCOUNTS_BILLING applies to:
   - Premium payments
   - Due dates
   - Refunds
   - Billing disputes
   - Invoices or receipts

4. POLICY_INFORMATION_MARKETING applies to:
   - Coverage questions
   - Policy benefits
   - Renewals (non-payment related)
   - Marketing or promotional communication

5. Ambiguous emails:
   - If two or more labels appear equally valid
   - If intent cannot be confidently inferred

   → DO NOT guess.
   → Route to human review.
"""