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

Return in this format:

Verdict: Verified / Inaccurate / False

Explanation:
...

Evidence:
...
"""

CLAIM_EXTRACTION_PROMPT = """
You are an expert at extracting factual claims.

From the following document, extract ONLY factual claims that can be verified.

Include:
- Statistics
- Dates
- Financial figures
- Technical facts
- Historical facts

Ignore opinions, advertisements and marketing language.

Return ONLY a bullet list.

Document:
{text}
"""
