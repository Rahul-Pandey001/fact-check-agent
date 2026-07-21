FACT_CHECK_PROMPT = """
You are an expert fact-checking assistant.

Claim:
{claim}

Evidence:
{context}

Instructions:
1. Determine whether the claim is:
   - Verified
   - Inaccurate
   - False

2. Explain why.

3. Cite the evidence.

Return exactly in this format:

Verdict: Verified / Inaccurate / False

Explanation:
...

Evidence:
...
"""

CLAIM_EXTRACTION_PROMPT = """
You are an expert claim extraction assistant.

Extract ONLY factual, verifiable claims from the document.

Ignore:
- opinions
- advertisements
- greetings
- introductions
- conclusions
- marketing language

Return ONLY a valid JSON array.

Example:

[
  "India became independent in 1947.",
  "The Earth revolves around the Sun.",
  "Water boils at 100°C at sea level."
]

Document:
{text}
"""
