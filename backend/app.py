import os
from flask import Flask, request, jsonify, send_from_directory
from modules.embedding_client import get_embedding
from modules.memory_engine import store_memory, retrieve_memory, save_memory
from modules.prior_occurrence import prior_occurrence_check
from modules.reconstruction_engine import reconstruct_memory
from modules.conversation_engine import normal_chat

# ─── Point Flask to frontend folder ───
BACKEND_DIR = os.path.dirname(os.path.abspath(__file__))
FRONTEND_DIR = os.path.join(BACKEND_DIR, '..', 'frontend')

app = Flask(
    __name__,
    static_folder=FRONTEND_DIR,
    static_url_path=''
)

# ─── Seed default memories once per process (only if memory is empty) ───
def seed_once():
    from modules.memory_engine import index
    if index.ntotal == 0:
        store_memory('User proposed trace-based memory reconstruction.')
        store_memory('User discussed context beyond time and identity.')
        store_memory('User suggested reconstructing memories from residual traces.')
        save_memory()
        print('[App] Seeded initial memories.')
    else:
        print(f'[App] Memory already has {index.ntotal} entries — skipping seed.')


@app.route('/')
def home():
    return send_from_directory(FRONTEND_DIR, 'index.html')


@app.route('/chat', methods=['POST'])
def chat():
    user_msg = request.json.get('message', '').strip()
    if not user_msg:
        return jsonify({'reply': 'Please send a message.', 'mode': 'error'}), 400

    # ─── Prior occurrence check ───
    prior_event, results = prior_occurrence_check(user_msg)
    mode = 'novel interaction'

    if prior_event:
        if len(results) == 1:
            # Only one weak trace — reconstruct
            mode = 'reconstruction'
            response = reconstruct_memory(user_msg, results)
        else:
            # Multiple strong matches — direct recall, but use LLM to respond naturally
            mode = 'direct recall'
            memory_context = '\n'.join(results)
            # Use normal_chat WITH memory context for natural, warm recall response
            response = normal_chat(user_msg, memory_context)
    else:
        # No strong prior match — normal chat with whatever context was retrieved
        recent_context = '\n'.join(results) if results else ''
        response = normal_chat(user_msg, recent_context)

    # ─── Store user message to memory ───
    store_memory(user_msg)
    save_memory()

    return jsonify({
        'reply': response,
        'mode': mode
    })


if __name__ == '__main__':
    seed_once()
    app.run(debug=True)
