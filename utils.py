import streamlit as st

def verdict_color(verdict):

    verdict = verdict.lower()

    if "true" in verdict:
        st.success(verdict)

    elif "false" in verdict:
        st.error(verdict)

    elif "misleading" in verdict:
        st.warning(verdict)

    else:
        st.info(verdict)
