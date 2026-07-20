import os
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
    page_title="AI Fact Check Agent",
    page_icon="📰",
    layout="wide"
)

st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

if not GOOGLE_API_KEY:
    st.error("Missing GOOGLE_API_KEY")
    st.stop()

if not TAVILY_API_KEY:
    st.error("Missing TAVILY_API_KEY")
    st.stop()

client = genai.Client(api_key=GOOGLE_API_KEY)
tavily = TavilyClient(api_key=TAVILY_API_KEY)

st.title("📰 AI Fact Check Agent")
st.caption("Upload a PDF or manually verify a claim.")

mode = st.radio(
    "Choose Input",
    ["📄 Upload PDF", "✍ Manual Claim"]
)


def extract_pdf_text(uploaded_file):
    pdf = PyPDF2.PdfReader(uploaded_file)
    text = ""

    for page in pdf.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"

    return text


def extract_claims(text):

    prompt = CLAIM_EXTRACTION_PROMPT.format(text=text[:15000])

    response = client.models.generate_content(
        model="gemini-flash-latest",
        contents=prompt
    )

    claims = []

    for line in response.text.split("\n"):
        line = line.strip()

        if line.startswith("-"):
            claims.append(line[1:].strip())

        elif line[:2].isdigit():
            claims.append(line.split(".",1)[1].strip())

    return claims


def verify_claim(claim):

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
        model="gemini-flash-latest",
        contents=prompt
    )

    return response.text, results


if mode == "✍ Manual Claim":

    claim = st.text_area(
        "Enter Claim",
        placeholder="MS Dhoni is a footballer."
    )

    if st.button("Fact Check"):

        if claim.strip():

            with st.spinner("Checking..."):
                result, evidence = verify_claim(claim)

            st.subheader("Result")
            st.write(result)

            st.subheader("Sources")

            for e in evidence:
                st.markdown(
                    f"**{e['title']}**\n\n{e['url']}"
                )

else:

    uploaded = st.file_uploader(
        "Upload PDF",
        type=["pdf"]
    )

    if uploaded:

        if st.button("Analyze PDF"):

            with st.spinner("Reading PDF..."):

                text = extract_pdf_text(uploaded)

            with st.spinner("Extracting Claims..."):

                claims = extract_claims(text)

            st.success(f"Found {len(claims)} claims.")

            for i, claim in enumerate(claims,1):

                st.markdown("---")
                st.subheader(f"Claim {i}")

                st.write(claim)

                with st.spinner("Checking claim..."):

                    result, evidence = verify_claim(claim)

                verdict = result.lower()

                if "verified" in verdict or "true" in verdict:

                    st.success("✅ VERIFIED")

                elif "false" in verdict:

                    st.error("❌ FALSE")

                else:

                    st.warning("⚠ INACCURATE")

                st.write(result)

                with st.expander("Evidence"):

                    for e in evidence:

                        st.markdown(
                            f"""
**{e['title']}**

{e['url']}
"""
                        )
