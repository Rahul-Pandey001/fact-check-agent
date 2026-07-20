import os
import time
import streamlit as st
from dotenv import load_dotenv
from tavily import TavilyClient
from google import genai

from styles import CUSTOM_CSS
from prompts import FACT_CHECK_PROMPT
load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
st.set_page_config(
    page_title="AI Fact Check Agent",
    page_icon="📰",
    layout="centered"
)

st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

if not GOOGLE_API_KEY:
    st.error("❌ GOOGLE_API_KEY not found in .env file.")
    st.stop()

if not TAVILY_API_KEY:
    st.error("❌ TAVILY_API_KEY not found in .env file.")
    st.stop()

client = genai.Client(api_key=GOOGLE_API_KEY)
tavily = TavilyClient(api_key=TAVILY_API_KEY)

st.markdown("""
<h1>📰 AI Fact Check Agent</h1>

<p class="subtitle">
Verify claims using AI-powered evidence analysis
</p>
""", unsafe_allow_html=True)

claim = st.text_area(
    "Enter a claim",
    placeholder="Example: India Gate is situated in Karnataka"
)

if st.button("Fact Check"):

    if not claim.strip():
        st.warning("Please enter a claim.")
        st.stop()
    try:
        with st.spinner("🌐 Searching trusted sources..."):
            search = tavily.search(
                query=claim,
                search_depth="advanced",
                max_results=5
            )

    except Exception:
        st.error("❌ Unable to retrieve web evidence. Please try again.")
        st.stop()

    results = search.get("results", [])

    if not results:
        st.warning("No evidence found for this claim.")
        st.stop()
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
    response = None

    with st.spinner("🤖 Analyzing evidence..."):

        MAX_RETRIES = 3

        for attempt in range(MAX_RETRIES):

            try:

                response = client.models.generate_content(
                    model="gemini-flash-latest",
                    contents=prompt
                )

                break

            except Exception as e:

                error = str(e)

                # Retry only for temporary server errors
                if "503" in error or "UNAVAILABLE" in error:

                    if attempt < MAX_RETRIES - 1:
                        time.sleep(4)
                        continue

                    st.error(
                        "⚠️ Gemini is experiencing high demand.\n\nPlease try again in a minute."
                    )
                    st.stop()

                else:
                    st.error(f"❌ AI Error:\n\n{error}")
                    st.stop()


    st.success("✅ Fact Check Complete")

    st.markdown("<div class='result-card'>", unsafe_allow_html=True)

    result = response.text if response else "No response generated."

    result_lower = result.lower()

    if "false" in result_lower:

        st.markdown("""
        <div class="false-box">
        ❌ FALSE
        </div>
        """, unsafe_allow_html=True)

    elif "true" in result_lower:

        st.markdown("""
        <div class="true-box">
        ✅ TRUE
        </div>
        """, unsafe_allow_html=True)

    else:

        st.warning("⚠️ Verdict could not be determined.")

    st.subheader("🤖 AI Analysis")
    st.write(result)

    st.subheader("🔗 Evidence Sources")

    for item in results:

        st.markdown(f"""
<div class="source-box">

🔗 <b>{item.get('title','No title')}</b><br><br>

<a href="{item.get('url','')}" target="_blank">
{item.get('url','')}
</a>

</div>
""", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)
