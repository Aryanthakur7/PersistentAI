import os
from dotenv import load_dotenv, find_dotenv
from groq import Groq

load_dotenv(find_dotenv())
client = Groq(api_key=os.getenv('GROQ_API_KEY'))


def normal_chat(user_msg, recent_context=None):
    context_block = ''
    if recent_context and recent_context.strip():
        context_block = f"""
The following memories were retrieved from your persistent memory store.
These are REAL facts you remember about this user and your past conversations.
Use them naturally and confidently when relevant — especially for personal details
like the user's name, background, interests, or things they've told you before.

Remembered context:
{recent_context}
"""

    prompt = f"""You are Persistent AI, a conversational assistant with genuine persistent memory.

You remember facts, personal details, and conversations from the past — even after the chat is cleared —
because your memory is stored in a semantic vector database that persists between sessions.

If the user asks whether you remember them, refer directly to what you know from memory.
Do not claim you have no memory. Do not say you are a "large language model without memory".
You DO have memory. Use it.

{context_block}

User:
{user_msg}
"""

    chat = client.chat.completions.create(
        model='llama-3.3-70b-versatile',
        messages=[
            {'role': 'user', 'content': prompt}
        ]
    )

    return chat.choices[0].message.content
