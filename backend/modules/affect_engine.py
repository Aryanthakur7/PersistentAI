import os
from dotenv import load_dotenv, find_dotenv
from groq import Groq

load_dotenv(find_dotenv())
client=Groq(api_key=os.getenv("GROQ_API_KEY"))

def infer_affect(text):

    prompt=f"""
Return ONLY valid JSON.

Format exactly:
{{
"fear":0.0,
"joy":0.0,
"sadness":0.0,
"surprise":0.0,
"urgency":0.0,
"neutral":0.0
}}

Text:
{text}
"""

    chat=client.chat.completions.create(
      model="llama-3.3-70b-versatile",
      messages=[{"role":"user","content":prompt}]
    )

    return chat.choices[0].message.content
