import os
import json
import streamlit as st
from dotenv import load_dotenv
from tavily import TavilyClient
from google import genai
import PyPDF2

from styles import CUSTOM_CSS
from prompts import FACT_CHECK_PROMPT, CLAIM_EXTRACTION_PROMPT

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

st.set_page_config(
    page_title="📰 AI Fact Check Agent",
    
    layout="wide"
)

st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

if not GOOGLE_API_KEY:
    st.error("❌ Missing GOOGLE_API_KEY")
    st.stop()

if not TAVILY_API_KEY:
    st.error("❌ Missing TAVILY_API_KEY")
    st.stop()

client = genai.Client(api_key=GOOGLE_API_KEY)
tavily = TavilyClient(api_key=TAVILY_API_KEY)

st.title("📰 AI Fact Check Agent")
st.caption(
    "Upload a PDF or manually verify a claim using Gemini + Tavily."
)

mode = st.radio(
    "Choose Input",
    [
        "📄 Upload PDF",
        "✍ Manual Claim"
    ]
)

def extract_pdf_text(uploaded_file):
    """
    Extract all readable text from PDF.
    """

    try:
        pdf = PyPDF2.PdfReader(uploaded_file)

        text = ""

        for page in pdf.pages:

            page_text = page.extract_text()

            if page_text:
                text += page_text + "\n"

        return text.strip()

    except Exception as e:

        st.error(f"Error reading PDF: {e}")

        return ""

def show_debug(text):

    with st.expander("🔍 Debug Information"):

        st.write("Characters extracted:", len(text))

        st.text_area(
            "Extracted PDF Text",
            text[:3000],
            height=250
        )

def extract_claims(text):

    if not text.strip():
        st.error("No text found inside the PDF.")
        return []

    prompt = CLAIM_EXTRACTION_PROMPT.format(
        text=text[:20000]
    )

    try:

        response = client.models.generate_content(
    model="gemini-3.5-flash",
    contents=prompt
)

        raw = response.text.strip()

        # Show Gemini response for debugging
        with st.expander("🤖 Gemini Claim Extraction Output"):
            st.code(raw)

        # Remove markdown if Gemini returns JSON
        raw = raw.replace("```json", "")
        raw = raw.replace("```", "").strip()
        try:

            parsed = json.loads(raw)

            if isinstance(parsed, list):

                claims = [
                    str(c).strip()
                    for c in parsed
                    if str(c).strip()
                ]

                return claims

        except Exception:
            pass

        claims = []

        for line in raw.split("\n"):

            line = line.strip()

            if not line:
                continue

            # Bullet list
            if line.startswith("-"):
                claims.append(line[1:].strip())
                continue

            # Numbered list
            if "." in line:

                first = line.split(".", 1)[0]

                if first.isdigit():

                    claims.append(
                        line.split(".", 1)[1].strip()
                    )

                    continue

            # Claim: xxx
            if ":" in line:

                left, right = line.split(":", 1)

                if len(left) < 20:
                    claims.append(right.strip())

        # Remove duplicates

        unique_claims = []

        for c in claims:

            if c not in unique_claims:
                unique_claims.append(c)

        return unique_claims

    except Exception as e:

        st.error(f"Claim extraction failed: {e}")

        return []

def verify_claim(claim):

    try:

        search = tavily.search(
            query=claim,
            search_depth="advanced",
            max_results=3
        )

        results = search.get("results", [])

        context = ""

        for item in results:

            context += f"""

Title:
{item.get('title','')}

Content:
{item.get('content','')}

URL:
{item.get('url','')}

"""
        prompt = FACT_CHECK_PROMPT.format(
            claim=claim,
            context=context
        )

        response = client.models.generate_content(
            model="gemini-3.5-flash",
            contents=prompt
        )

        return response.text, results

    except Exception as e:

        return (
            f"Error while verifying claim:\n\n{e}",
            []
        )

if mode == "✍ Manual Claim":

    st.subheader("Manual Fact Check")

    claim = st.text_area(
        "Enter a claim",
        placeholder="Example: MS Dhoni is a footballer."
    )

    if st.button("Fact Check", use_container_width=True):

        if not claim.strip():
            st.warning("Please enter a claim.")
            st.stop()

        with st.spinner("Searching the web and verifying..."):

            result, evidence = verify_claim(claim)

        st.subheader("Result")
        st.write(result)

        st.subheader("Evidence")

        if evidence:

            for item in evidence:

                st.markdown(
                    f"""
### {item.get('title','No Title')}

{item.get('content','')}

🔗 {item.get('url','')}
"""
                )

        else:
            st.info("No evidence returned.")

else:

    st.subheader("Upload PDF")

    uploaded = st.file_uploader(
        "Choose a PDF",
        type=["pdf"]
    )

    if uploaded:

        if st.button("📄 Analyze PDF", use_container_width=True):

            with st.spinner("Reading PDF..."):

                text = extract_pdf_text(uploaded)

            if not text.strip():

                st.error("No readable text found in this PDF.")

                st.stop()

            show_debug(text)

            with st.spinner("Extracting factual claims..."):

                claims = extract_claims(text)

            if len(claims) == 0:

                st.error("No factual claims found.")

                st.stop()

            st.success(f"✅ Found {len(claims)} claims.")

            progress = st.progress(0)

            for index, claim in enumerate(claims):

                progress.progress((index + 1) / len(claims))

                st.markdown("---")

                st.subheader(f"Claim {index + 1}")

                st.write(claim)

                with st.spinner("Fact checking..."):

                    result, evidence = verify_claim(claim)

                verdict = result.lower()

                if "verified" in verdict or "true" in verdict:

                    st.success("✅ VERIFIED")

                elif "false" in verdict:

                    st.error("❌ FALSE")

                elif "inaccurate" in verdict:

                    st.warning("⚠ INACCURATE")

                else:

                    st.info("ℹ Unable to determine")

                st.write(result)

                with st.expander("Evidence"):

                    if evidence:

                        for item in evidence:

                            st.markdown(
                                f"""
### {item.get('title','No Title')}

{item.get('content','')}

🔗 {item.get('url','')}
"""
                            )

                    else:

                        st.info("No evidence available.")

            progress.empty()

            st.success("🎉 Fact checking completed successfully!")
