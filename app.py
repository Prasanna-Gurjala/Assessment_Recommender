import os
os.environ["STREAMLIT_FILE_WATCHER_TYPE"] = "none"
import streamlit as st
from recommender import get_recommendations
import pandas as pd
# Dummy change to force redeploy

st.set_page_config(page_title="SHL Assessment Recommender", layout="centered")

st.title("🧠 SHL Assessment Recommender")
st.markdown("Type in a job description or hiring query below and get the most relevant SHL assessments.")

query = st.text_area("Enter job description or hiring requirement", height=200)

if st.button("🔍 Recommend Assessments") and query.strip():
    with st.spinner("Finding best assessments..."):
        results = get_recommendations(query)

        if results:
            df = pd.DataFrame(results)
            df = df[[
                "Assessment Name", "URL", "Remote Testing Support",
                "Adaptive Support", "Duration", "Test Type"
            ]]
            # Convert assessment names to hyperlinks
            df["Assessment Name"] = df.apply(lambda row: f"[{row['Assessment Name']}]({row['URL']})", axis=1)
            df.drop(columns="URL", inplace=True)

            st.success(f"Top {len(df)} Recommended Assessments:")
            st.write(df.to_markdown(index=False), unsafe_allow_html=True)
        else:
            st.warning("No relevant assessments found. Try a different query.")
