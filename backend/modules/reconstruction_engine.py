# current primitive reconstruction
import sys
import os
from dotenv import load_dotenv, find_dotenv
from groq import Groq

load_dotenv(find_dotenv())
client=Groq(api_key=os.getenv("GROQ_API_KEY"))

def reconstruct_memory(query,retrieved_results):

    context="\n".join(retrieved_results)

    prompt=f"""
Direct episodic memory is unavailable.

Using these residual traces:

{context}

Reconstruct the most probable prior memory the user is referring to.

State uncertainty if needed.
"""


    chat=client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
             "role":"user",
             "content":prompt
            }
        ]
    )

    return (
      chat.choices[0]
      .message.content
    )

# future plug-point
# def groq_reconstruct(...):
#     pass
