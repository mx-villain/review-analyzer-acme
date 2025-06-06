from fastapi import FastAPI, Form
import requests

app = FastAPI()

def query_ollama(prompt: str):
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={"model": "mistral", "prompt": prompt, "stream": False}
    )
    return response.json()["response"].strip()

@app.post("/analyze/")
def analyze_review(text: str = Form(...)):
    sentiment_prompt = query_ollama(f"What is the sentiment (Positive, Neutral, Negative)?\n\n{text}")
    topic_prompt = query_ollama(f"What is the main issue/topic discussed in this review?\n\n{text}")
    summary_prompt = query_ollama(f"Summarize the review in one short sentence:\n\n{text}")
    
    sentiment = query_ollama(sentiment_prompt)
    topic = query_ollama(topic_prompt)
    summary = query_ollama(summary_prompt)
    
    return {"sentiment": sentiment, "topic": topic, "summary": summary}
