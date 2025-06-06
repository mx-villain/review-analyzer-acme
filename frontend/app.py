import streamlit as st
import pandas as pd
import requests

st.title("🛒 Acme Product Review Analyzer")

uploaded_file = st.file_uploader("Upload CSV file with product reviews", type="csv")

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    results = []

    with st.spinner("Analyzing reviews..."):
        for _, row in df.iterrows():
            review_text = row["review_text"]
            res = requests.post("http://localhost:8000/analyze/", data={"text": review_text})
            data = res.json()
            results.append({
                    "product_name": row["product_name"],
                    "review_text": review_text,
                    **data
                })
            
    result_df = pd.DataFrame(results)
    st.success("Analysis complete!")
    
    st.dataframe(result_df)

    st.download_button(
        "Download Results as CSV",
        data=result_df.to_csv(index=False)
    )


    st.subheader("📊 Sentiment Distribution")
    st.bar_chart(result_df["sentiment"].value_counts())

    st.subheader("📌 Top Topics")
  
