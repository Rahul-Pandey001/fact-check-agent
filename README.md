# 📰 AI Fact Check Agent
An AI-powered web application that automatically extracts factual claims from PDF documents, verifies them against live web data, and classifies each claim as **Verified**, **Inaccurate**, or **False**.
---

# Live demo
https://fact-check-agent-pmb55vdk5dq6gu3prtctvz.streamlit.app/

# Features
*  Upload any PDF document
*  Automatically extract factual claims
*  Verify claims using live web search
*  AI-powered fact checking with Gemini
*  Classify claims as:
  * Verified
  * Inaccurate
  * False
* Display supporting evidence and sources
* Manual claim verification mode
* Simple and responsive Streamlit interface
---

# Tech Stack
* Python
* Streamlit
* Google Gemini API
* Tavily Search API
* PyPDF2
* python-dotenv
---

# Project Structure
```
fact-check-agent/
│── app.py
│── prompts.py
│── styles.py
│── requirements.txt
│── .gitignore
│── README.md
│── utils.py
```
---

# Installation

Clone the repository:

```bash
git clone https://github.com/your-username/fact-check-agent.git
```
Move into the project folder:

```bash
cd fact-check-agent
```

Create a virtual environment:

```bash
python -m venv venv
```

Activate it:
# Windows

```bash
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

##  Environment Variables
Create a '.env' file in the project root.

GOOGLE_API_KEY=your_google_api_key
TAVILY_API_KEY=your_tavily_api_key

---
# Run the Application

```bash
streamlit run app.py
```
---
# How It Works
1. Upload a PDF or enter a manual claim.
2. The application extracts factual claims using Gemini.
3. Each claim is searched against live web sources using Tavily.
4. Gemini analyzes the retrieved evidence.
5. The application returns:

   * Verdict
   * Explanation
   * Correct Fact
   * Supporting Evidence
---
# Sample Output

**Claim**
> India's literacy rate is 65%.

**Verdict**
⚠️ Inaccurate

**Correct Fact**
India's literacy rate is approximately 80.9% according to recent government estimates.

---

# Deployment
The application can be deployed using:

* Streamlit Community Cloud
* Render
* Railway
---

# Author
Rahul Pandey.
Built using Streamlit, Gemini AI, and Tavily Search API.
