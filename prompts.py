FACT_CHECK_PROMPT = """
You are an expert fact-checking assistant.

Claim:
{claim}

Evidence:
{context}

Classify the claim into ONLY one of these:

- Verified
- Inaccurate
- False

Rules:

Verified:
The claim is fully supported by reliable evidence.

Inaccurate:
The claim contains outdated data, incorrect numbers, or partially correct information.

False:
The claim is contradicted by reliable evidence.

IMPORTANT:
Keep the response SHORT.

Return EXACTLY in this format:

Verdict:
(one word only)

Explanation:
(Maximum 2 sentences)

Correct Fact:
(One sentence only)

Evidence:
- Source Name: Correct fact
- Source Name: Correct fact

Use ONLY the 2 most reliable sources.
Do NOT copy long paragraphs.
Do NOT include unnecessary details.
Maximum response length: 150 words.
"""
CLAIM_EXTRACTION_PROMPT = """
You are an expert claim extraction assistant.

Extract ONLY factual, verifiable claims from the document.

Include only:
- Statistics
- Dates
- Financial figures
- Technical facts
- Historical facts

Ignore:
- Opinions
- Advertisements
- Greetings
- Marketing language

Return ONLY a valid JSON array.

Example:
[
  "India became independent in 1947.",
  "Python was first released in 1991.",
  "The Earth revolves around the Sun."
]

Document:
{text}
"""
